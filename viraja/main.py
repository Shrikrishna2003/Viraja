import base64, hashlib, hmac, io, json, os, secrets, smtplib, time, urllib.error, urllib.request
from collections import Counter
from datetime import date, timedelta
from email.message import EmailMessage
from pathlib import Path
from typing import List, Optional

from fastapi import Depends, FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from argon2 import PasswordHasher
from pypdf import PdfReader
from sqlalchemy import Column, Date, Float, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from skills import QUESTIONS, ROADMAP, analyze

_env = Path(__file__).parent / ".env"
if _env.exists():
    for _l in _env.read_text().splitlines():
        if "=" in _l and not _l.strip().startswith("#"):
            _k, _v = _l.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip().strip('"'))
if os.getenv("VERCEL") and not os.getenv("DATABASE_URL"):
    raise RuntimeError("Set DATABASE_URL to a hosted Postgres (Neon/Supabase). Vercel's filesystem is read-only.")
DB_URL = os.getenv("DATABASE_URL", "sqlite:///viraja.db").replace("postgres://", "postgresql://", 1)
engine = create_engine(DB_URL, connect_args={"check_same_thread": False} if DB_URL.startswith("sqlite") else {})
Session = sessionmaker(engine)
Base = declarative_base()
STATUSES = ["Applied", "OA", "Interview", "Offer", "Rejected"]
SECRET = os.getenv("SECRET_KEY", "")
_prod = bool(os.getenv("VERCEL")) or not os.getenv("BASE_URL", "http://127.0.0.1:8000").startswith(("http://127.0.0.1", "http://localhost"))
if _prod and len(SECRET) < 32:
    raise RuntimeError("Set SECRET_KEY to a random string of at least 32 characters in production.")
if not SECRET:
    _sf = Path(__file__).parent / ".dev_secret"  # local-only key that survives restarts
    if not _sf.exists():
        _sf.write_text(secrets.token_hex(32))
    SECRET = _sf.read_text().strip()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(200), unique=True, nullable=False)
    name = Column(String(100), default="")
    pw = Column(String(200), nullable=False)


class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True, nullable=False)
    company = Column(String(120), nullable=False)
    role = Column(String(120), nullable=False)
    status = Column(String(20), default="Applied")
    applied_on = Column(Date, default=date.today)
    match_score = Column(Float, nullable=True)
    jd_skills = Column(Text, default="[]")
    gaps = Column(Text, default="[]")


Base.metadata.create_all(engine)
app = FastAPI(title="VIRAJA")


# ---------- auth helpers ----------
def sign(data, ttl):
    p = base64.urlsafe_b64encode(json.dumps({**data, "exp": int(time.time()) + ttl}).encode()).decode()
    return p + "." + hmac.new(SECRET.encode(), p.encode(), hashlib.sha256).hexdigest()


def unsign(tok):
    try:
        p, sig = tok.rsplit(".", 1)
        if not hmac.compare_digest(sig, hmac.new(SECRET.encode(), p.encode(), hashlib.sha256).hexdigest()):
            return None
        d = json.loads(base64.urlsafe_b64decode(p))
        return d if d["exp"] > time.time() else None
    except Exception:
        return None


PH = PasswordHasher()  # Argon2id


def hpw(p):
    return PH.hash(p)


def vpw(p, stored):
    if stored.startswith("$argon2"):
        try:
            return PH.verify(stored, p)
        except Exception:
            return False
    salt = stored.split("$")[0]  # legacy PBKDF2 hashes from earlier versions: salt$hash
    old = salt + "$" + hashlib.pbkdf2_hmac("sha256", p.encode(), salt.encode(), 200_000).hex()
    return hmac.compare_digest(old, stored)


COOKIE = "viraja_session"


def uid(request: Request):
    d = unsign(request.cookies.get(COOKIE, ""))
    if not d or d.get("t") != "a":
        raise HTTPException(401, "Please sign in.")
    return d["u"]


def check(email, pw):
    if "@" not in email or "." not in email.split("@")[-1]:
        raise HTTPException(422, "Enter a valid email address.")
    if len(pw) < 8:
        raise HTTPException(422, "Use at least 8 characters for your password.")


def session_for(u):
    r = JSONResponse({"name": u.name, "email": u.email})
    r.set_cookie(COOKIE, sign({"u": u.id, "t": "a"}, 7 * 86400), max_age=7 * 86400,
                 httponly=True, samesite="lax", secure=_prod, path="/")
    return r


class Creds(BaseModel):
    name: str = ""
    email: str
    password: str


class Forgot(BaseModel):
    email: str


class Reset(BaseModel):
    token: str
    password: str


@app.post("/api/signup")
def signup(b: Creds):
    email = b.email.strip().lower()
    check(email, b.password)
    with Session() as s:
        if s.query(User).filter_by(email=email).first():
            raise HTTPException(409, "An account with this email already exists. Sign in instead.")
        u = User(email=email, name=b.name.strip()[:100], pw=hpw(b.password))
        s.add(u)
        s.commit()
        return session_for(u)


ATTEMPTS = {}  # in-memory failure log per server instance; use Redis/Upstash for multi-instance production


def ip_of(r):
    return (r.headers.get("x-forwarded-for") or (r.client.host if r.client else "?")).split(",")[0].strip()


def throttled(key, limit=5, window=900):
    now = time.time()
    ATTEMPTS[key] = [t for t in ATTEMPTS.get(key, []) if now - t < window]
    return len(ATTEMPTS[key]) >= limit


@app.post("/api/login")
def login(b: Creds, request: Request):
    email = b.email.strip().lower()
    key = f"login|{ip_of(request)}|{email}"
    if throttled(key):
        raise HTTPException(429, "Too many failed attempts. Try again in 15 minutes.")
    with Session() as s:
        u = s.query(User).filter_by(email=email).first()
        if not u or not vpw(b.password, u.pw):
            ATTEMPTS.setdefault(key, []).append(time.time())
            raise HTTPException(401, "Email or password is incorrect.")
        ATTEMPTS.pop(key, None)
        if not u.pw.startswith("$argon2"):  # upgrade old hashes on login
            u.pw = hpw(b.password)
            s.commit()
        return session_for(u)


@app.post("/api/logout")
def logout():
    r = JSONResponse({"ok": True})
    r.delete_cookie(COOKIE, path="/")
    return r


@app.get("/api/me")
def me(user=Depends(uid)):
    with Session() as s:
        u = s.get(User, user)
        if not u:
            raise HTTPException(401, "Please sign in.")
        return {"name": u.name, "email": u.email}


LOCAL = os.getenv("BASE_URL", "http://127.0.0.1:8000").startswith(("http://127.0.0.1", "http://localhost"))


def send_mail(to, link):
    host = os.getenv("SMTP_HOST")
    if not host:
        print(f"\n[VIRAJA] SMTP not configured. Reset link for {to}:\n{link}\n")
        return False
    m = EmailMessage()
    m["Subject"], m["To"] = "Reset your VIRAJA password", to
    m["From"] = os.getenv("SMTP_FROM") or os.getenv("SMTP_USER", "")
    m.set_content(f"Open this link within 30 minutes to choose a new password:\n{link}\n\nIf you didn't ask for this, ignore this email.")
    port = int(os.getenv("SMTP_PORT", "587"))
    with (smtplib.SMTP_SSL(host, port, timeout=20) if port == 465 else smtplib.SMTP(host, port, timeout=20)) as c:
        if port != 465:
            c.starttls()
        c.login(os.getenv("SMTP_USER", ""), os.getenv("SMTP_PASS", ""))
        c.send_message(m)
    return True


@app.post("/api/forgot")
def forgot(b: Forgot, request: Request):
    k = f"forgot|{ip_of(request)}"
    if throttled(k):
        raise HTTPException(429, "Too many reset requests. Try again in 15 minutes.")
    ATTEMPTS.setdefault(k, []).append(time.time())
    with Session() as s:
        u = s.query(User).filter_by(email=b.email.strip().lower()).first()
    out = {"ok": True}
    if not u:
        if LOCAL:
            out["dev_note"] = "No account exists with that email. Check the spelling, or sign up first."
        return out
    base = os.getenv("BASE_URL") or str(request.base_url).rstrip("/")
    link = f"{base}/#reset={sign({'u': u.id, 't': 'r', 'k': u.pw[-8:]}, 1800)}"
    try:
        if not send_mail(u.email, link) and LOCAL:
            out["dev_link"] = link
    except Exception as e:
        print("[VIRAJA] reset email failed:", e)
        if LOCAL:
            out.update(dev_link=link, dev_error=f"{type(e).__name__}: {str(e)[:160]}")
    return out


@app.post("/api/reset")
def reset(b: Reset):
    if len(b.password) < 8:
        raise HTTPException(422, "Use at least 8 characters for your password.")
    d = unsign(b.token)
    with Session() as s:
        u = s.get(User, d["u"]) if d and d.get("t") == "r" else None
        if not u or u.pw[-8:] != d["k"]:
            raise HTTPException(400, "This reset link is invalid or has expired. Request a new one.")
        u.pw = hpw(b.password)
        s.commit()
    return {"ok": True}


# ---------- app ----------
@app.get("/")
def index():
    return FileResponse(Path(__file__).parent / "public" / "index.html", headers={"Cache-Control": "no-store"})


@app.get("/__info")
def info():
    if not LOCAL:
        raise HTTPException(404, "Not found.")
    p = Path(__file__).parent / "public" / "index.html"
    return {"folder": str(p.parent.parent), "index_html_found": p.exists(),
            "page_has_VIRAJA_logo": p.exists() and "VIRA<b>JA</b>" in p.read_text(encoding="utf-8"),
            "env_file_found": (p.parent.parent / ".env").exists(),
            "smtp_configured": bool(os.getenv("SMTP_HOST")), "ai_provider": os.getenv("AI_PROVIDER") or None}


@app.post("/api/analyze")
async def analyze_endpoint(resume: Optional[UploadFile] = File(None), resume_text: str = Form(""),
                           jd: str = Form(...), user=Depends(uid)):
    if len(jd.strip()) < 30:
        raise HTTPException(422, "Paste the full job description.")
    text = resume_text.strip()
    if resume is not None and resume.filename:
        data = await resume.read()
        if len(data) > 5_000_000:
            raise HTTPException(413, "That PDF is over 5 MB. Export a smaller one.")
        try:
            text = "\n".join(p.extract_text() or "" for p in PdfReader(io.BytesIO(data)).pages)
        except Exception:
            raise HTTPException(422, "That file isn't a readable PDF.")
    if len(text.strip()) < 50:
        raise HTTPException(422, "No readable text found. If your PDF is a scan, paste your resume text instead.")
    return analyze(text[:60000], jd[:20000])


class AppIn(BaseModel):
    company: str
    role: str
    status: str = "Applied"
    match_score: Optional[float] = None
    jd_skills: List[str] = []
    gaps: List[str] = []


class StatusIn(BaseModel):
    status: str


def row(a):
    return {"id": a.id, "company": a.company, "role": a.role, "status": a.status,
            "applied_on": a.applied_on.isoformat(), "match_score": a.match_score}


@app.get("/api/applications")
def list_apps(user=Depends(uid)):
    with Session() as s:
        return [row(a) for a in s.query(Application).filter_by(user_id=user).order_by(Application.id.desc())]


@app.post("/api/applications")
def add_app(b: AppIn, user=Depends(uid)):
    if b.status not in STATUSES:
        raise HTTPException(422, "Unknown status.")
    with Session() as s:
        a = Application(user_id=user, company=b.company.strip()[:120], role=b.role.strip()[:120], status=b.status,
                        match_score=b.match_score, jd_skills=json.dumps(b.jd_skills), gaps=json.dumps(b.gaps))
        s.add(a)
        s.commit()
        return row(a)


@app.patch("/api/applications/{app_id}")
def set_status(app_id: int, b: StatusIn, user=Depends(uid)):
    if b.status not in STATUSES:
        raise HTTPException(422, "Unknown status.")
    with Session() as s:
        a = s.get(Application, app_id)
        if not a or a.user_id != user:
            raise HTTPException(404, "Not found.")
        a.status = b.status
        s.commit()
        return row(a)


@app.delete("/api/applications/{app_id}")
def delete_app(app_id: int, user=Depends(uid)):
    with Session() as s:
        a = s.get(Application, app_id)
        if a and a.user_id == user:
            s.delete(a)
            s.commit()
    return {"ok": True}


@app.get("/api/stats")
def stats(user=Depends(uid)):
    with Session() as s:
        rows = s.query(Application).filter_by(user_id=user).all()
    counts = Counter(r.status for r in rows)
    responded = sum(counts[k] for k in ("OA", "Interview", "Offer", "Rejected"))
    scores = [r.match_score for r in rows if r.match_score is not None]
    per = Counter(r.applied_on for r in rows)
    days = [date.today() - timedelta(d) for d in range(13, -1, -1)]
    return {
        "total": len(rows), "counts": {k: counts[k] for k in STATUSES},
        "response_rate": round(100 * responded / len(rows)) if rows else 0,
        "avg_score": round(sum(scores) / len(scores)) if scores else None,
        "top_skills": Counter(k for r in rows for k in json.loads(r.jd_skills or "[]")).most_common(6),
        "top_gaps": Counter(k for r in rows for k in json.loads(r.gaps or "[]")).most_common(6),
        "by_day": [[d.strftime("%d %b"), per[d]] for d in days],
    }


# ---------- Krish, the career coach ----------
class Coach(BaseModel):
    score: int = 0
    weak: List[str] = []
    matched: List[str] = []
    missing: List[str] = []
    ai: bool = False


# Tool 1: skill gaps that keep recurring across the user's saved applications
def tool_history(user):
    with Session() as s:
        rows = s.query(Application).filter_by(user_id=user).all()
    return len(rows), Counter(k for r in rows for k in json.loads(r.gaps or "[]")).most_common(3)


API = "https://api.anthropic.com/v1/messages"
TOOLS = [
    {"name": "get_match_analysis", "description": "The current resume-vs-job result: score, matched skills, missing skills, weak resume bullets.",
     "input_schema": {"type": "object", "properties": {}}},
    {"name": "get_application_history", "description": "How many applications the user saved and which skill gaps keep recurring.",
     "input_schema": {"type": "object", "properties": {}}},
    {"name": "get_learning_resource", "description": "A concrete practice task for learning one skill.",
     "input_schema": {"type": "object", "properties": {"skill": {"type": "string"}}, "required": ["skill"]}},
    {"name": "get_interview_questions", "description": "A sample interview question for one skill.",
     "input_schema": {"type": "object", "properties": {"skill": {"type": "string"}}, "required": ["skill"]}},
]


def run_tool(name, args, b, user):
    skill = str(args.get("skill", "")).lower()
    if name == "get_match_analysis":
        return {"score": b.score, "matched": b.matched, "missing": b.missing, "weak_bullets": b.weak[:5]}
    if name == "get_application_history":
        n, rec = tool_history(user)
        return {"saved_applications": n, "recurring_gaps": rec}
    if name == "get_learning_resource":
        return ROADMAP.get(skill, "No curated resource. Suggest one small project using the skill.")
    if name == "get_interview_questions":
        return QUESTIONS.get(skill, "No stored question. Write one practical question.")
    return "Unknown tool."


# Tool-calling loop: the model decides which tools to call, we run them, and it continues until it answers.
def agent_anthropic(b, user):
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        raise HTTPException(503, "Krish's AI mode is off. Set ANTHROPIC_API_KEY on the server to turn it on.")
    system = ("You are Krish, a career coach for a fresher software developer. Call the tools you need, then reply with ONLY JSON: "
              '{"rewrites":[{"original":"...","improved":"..."}],"plan":["Day 1: ...","Day 2: ..."]}. '
              "Rewrite each weak bullet with an action verb and impact; never invent numbers, use [X] placeholders. "
              "The plan has 7 short items grounded in the tool results.")
    msgs = [{"role": "user", "content": "Coach this candidate for the job they just analyzed."}]
    used = []
    try:
        for _ in range(6):
            req = urllib.request.Request(
                API, headers={"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
                data=json.dumps({"model": os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5-5"), "max_tokens": 1500,
                                 "system": system, "tools": TOOLS, "messages": msgs}).encode())
            r = json.load(urllib.request.urlopen(req, timeout=60))
            msgs.append({"role": "assistant", "content": r["content"]})
            calls = [c for c in r["content"] if c["type"] == "tool_use"]
            if not calls:
                txt = "".join(c.get("text", "") for c in r["content"] if c["type"] == "text")
                out = json.loads(txt[txt.index("{"): txt.rindex("}") + 1])
                out["tools_used"] = used
                return out
            results = []
            for c in calls:
                used.append(c["name"] + (f"({c['input']['skill']})" if c["input"].get("skill") else ""))
                results.append({"type": "tool_result", "tool_use_id": c["id"],
                                "content": json.dumps(run_tool(c["name"], c["input"], b, user))})
            msgs.append({"role": "user", "content": results})
    except Exception:
        raise HTTPException(502, "Krish couldn't finish. Check your API key and try again.")
    raise HTTPException(502, "Krish took too many steps. Try again.")


@app.post("/api/krish")
def krish(b: Coach, user=Depends(uid)):
    n, recurring = tool_history(user)
    top = b.missing[:3]
    items = []
    if top:
        items.append({"level": "red", "text": f"You're missing {', '.join(top)}."})
    if b.weak:
        items.append({"level": "amber", "text": f"{len(b.weak)} of your bullets don't show clear, measurable results."})
    if b.matched:
        items.append({"level": "green", "text": f"{', '.join(b.matched[:3])} match this role well."})
    recs = [f"Add {s} to your preparation plan." for s in top[:2]]
    if b.weak:
        recs.append(f'Rewrite this bullet first: "{b.weak[0][:90]}"')
    if b.matched:
        recs.append(f"Prepare the {b.matched[0]} interview questions below.")
    if top:
        recs.append(f"Spend the next 7 days on {' + '.join(top[:2])}.")
    if n > 1 and recurring:
        recs.append(f"Across your {n} saved applications, {recurring[0][0]} is your most common gap.")
    return {"headline": f"Your match is {b.score}%.", "items": items, "recommendations": recs,
            "ai": agent(b, user) if b.ai else None}


# ---------- free / other providers (OpenAI-compatible tool calling) ----------
PRESETS = {
    "gemini": ("https://generativelanguage.googleapis.com/v1beta/openai", "gemini-3.5-flash-lite"),
    "groq": ("https://api.groq.com/openai/v1", "llama-3.3-70b-versatile"),
    "openrouter": ("https://openrouter.ai/api/v1", "meta-llama/llama-3.3-70b-instruct:free"),
    "ollama": ("http://localhost:11434/v1", "llama3.1"),
}
KRISH_SYSTEM = ("You are Krish, a career coach for a fresher software developer. Call the tools you need, then reply with ONLY JSON: "
                '{"rewrites":[{"original":"...","improved":"..."}],"plan":["Day 1: ...","Day 2: ..."]}. '
                "Rewrite each weak bullet with an action verb and impact; never invent numbers, use [X] placeholders. "
                "The plan has 7 short items grounded in the tool results.")


def agent_openai(b, user, prov):
    base, model = PRESETS[prov]
    base, model = os.getenv("AI_BASE_URL", base).rstrip("/"), os.getenv("AI_MODEL", model)
    key = os.getenv("AI_API_KEY", "")
    if not key and prov != "ollama":
        raise HTTPException(503, f"Set AI_API_KEY for {prov} in your .env file, then restart the server.")
    tools = [{"type": "function", "function": {"name": t["name"], "description": t["description"], "parameters": t["input_schema"]}} for t in TOOLS]
    msgs = [{"role": "system", "content": KRISH_SYSTEM}, {"role": "user", "content": "Coach this candidate for the job they just analyzed."}]
    used = []
    try:
        for _ in range(6):
            req = urllib.request.Request(
                base + "/chat/completions", headers={"Authorization": "Bearer " + (key or "ollama"), "Content-Type": "application/json"},
                data=json.dumps({"model": model, "messages": msgs, "tools": tools, "max_tokens": 1500}).encode())
            msg = json.load(urllib.request.urlopen(req, timeout=90))["choices"][0]["message"]
            msgs.append({k: v for k, v in msg.items() if k in ("role", "content", "tool_calls")})
            calls = msg.get("tool_calls") or []
            if not calls:
                txt = msg.get("content") or ""
                out = json.loads(txt[txt.index("{"): txt.rindex("}") + 1])
                out["tools_used"] = used
                return out
            for c in calls:
                name, args = c["function"]["name"], json.loads(c["function"].get("arguments") or "{}")
                used.append(name + (f"({args['skill']})" if args.get("skill") else ""))
                msgs.append({"role": "tool", "tool_call_id": c["id"], "content": json.dumps(run_tool(name, args, b, user))})
    except urllib.error.HTTPError as e:
        raise HTTPException(502, f"AI provider error {e.code}: " + e.read().decode(errors="replace")[:160])
    except Exception:
        raise HTTPException(502, "Krish couldn't finish. Check your AI settings and try again.")
    raise HTTPException(502, "Krish took too many steps. Try again.")


def agent(b, user):
    prov = os.getenv("AI_PROVIDER", "").strip().lower()
    if prov in PRESETS:
        return agent_openai(b, user, prov)
    if os.getenv("ANTHROPIC_API_KEY"):
        return agent_anthropic(b, user)
    raise HTTPException(503, "Krish's AI mode is off. Set AI_PROVIDER=gemini (free) and AI_API_KEY in your .env file, then restart the server.")
