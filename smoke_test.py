"""End-to-end check. Usage: python smoke_test.py [base_url]"""
import http.cookiejar, json, sys, time, urllib.error, urllib.request

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000").rstrip("/")
failed = []


def browser():
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))


def call(op, method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, method=method, data=data, headers={"Content-Type": "application/json"})
    try:
        with op.open(req, timeout=30) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")


def check(name, cond):
    print("PASS" if cond else "FAIL", name)
    if not cond:
        failed.append(name)


n = int(time.time())
ea, eb, ec = f"a{n}@test.dev", f"b{n}@test.dev", f"c{n}@test.dev"
A, B, anon = browser(), browser(), browser()

s, d = call(A, "POST", "/api/signup", {"name": "A", "email": ea, "password": "password-one"})
check("signup A (no token in body)", s == 200 and "token" not in d)
check("signup B", call(B, "POST", "/api/signup", {"name": "B", "email": eb, "password": "password-two"})[0] == 200)
check("duplicate signup rejected", call(anon, "POST", "/api/signup", {"email": ea, "password": "password-one"})[0] == 409)

raw = urllib.request.urlopen(urllib.request.Request(
    BASE + "/api/login", method="POST", data=json.dumps({"email": ea, "password": "password-one"}).encode(),
    headers={"Content-Type": "application/json"}))
cookie = " ".join(raw.headers.get_all("Set-Cookie") or []).lower()
check("session cookie is HttpOnly + SameSite", "httponly" in cookie and "samesite=lax" in cookie)

check("session works (/api/me)", call(A, "GET", "/api/me")[1].get("email") == ea)
check("no cookie rejected", call(anon, "GET", "/api/applications")[0] == 401)
check("wrong password rejected", call(anon, "POST", "/api/login", {"email": ea, "password": "wrong-pass"})[0] == 401)

codes = [call(anon, "POST", "/api/login", {"email": ec, "password": "bad-guess-%d" % i})[0] for i in range(6)]
check("login rate limit (5 failures, then 429)", codes[:5] == [401] * 5 and codes[5] == 429)

s, app_ = call(A, "POST", "/api/applications", {"company": "Acme", "role": "Dev", "match_score": 70,
                                                 "jd_skills": ["python", "docker"], "gaps": ["docker"]})
check("save application", s == 200 and app_.get("id"))
check("A sees own application", len(call(A, "GET", "/api/applications")[1]) == 1)
check("B cannot see A's application", call(B, "GET", "/api/applications")[1] == [])
check("B cannot edit A's application", call(B, "PATCH", f"/api/applications/{app_['id']}", {"status": "Offer"})[0] == 404)
call(B, "DELETE", f"/api/applications/{app_['id']}")
check("B cannot delete A's application", len(call(A, "GET", "/api/applications")[1]) == 1)
check("A can update status", call(A, "PATCH", f"/api/applications/{app_['id']}", {"status": "Interview"})[0] == 200)
s, st = call(A, "GET", "/api/stats")
check("stats", s == 200 and st["total"] == 1 and st["counts"]["Interview"] == 1)
s, k = call(A, "POST", "/api/krish", {"score": 60, "matched": ["python"], "missing": ["docker"], "weak": ["Worked on a project"]})
check("Krish coaching", s == 200 and k["items"] and k["recommendations"])
check("forgot password responds", call(anon, "POST", "/api/forgot", {"email": ea})[0] == 200)
check("bad reset token rejected", call(anon, "POST", "/api/reset", {"token": "x.y", "password": "password-new"})[0] == 400)
call(A, "POST", "/api/logout")
check("logout clears session", call(A, "GET", "/api/me")[0] == 401)
print("\nALL PASSED" if not failed else "\nFAILED: " + ", ".join(failed))
sys.exit(1 if failed else 0)
