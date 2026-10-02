import re

SKILLS = {
    "python": ["python"], "java": ["java"], "javascript": ["javascript", "js", "es6"],
    "typescript": ["typescript"], "c++": ["c++"], "c#": ["c#"], "go": ["golang"],
    "html": ["html", "html5"], "css": ["css", "css3"], "react": ["react", "reactjs", "react.js"],
    "angular": ["angular"], "vue": ["vue", "vuejs"], "node.js": ["node.js", "nodejs", "node"],
    "flask": ["flask"], "django": ["django"], "fastapi": ["fastapi"], "spring boot": ["spring boot", "springboot"],
    "sql": ["sql"], "mysql": ["mysql"], "postgresql": ["postgresql", "postgres"], "mongodb": ["mongodb", "mongo"],
    "redis": ["redis"], "sqlite": ["sqlite"], "rest api": ["rest api", "rest apis", "restful", "rest services"],
    "graphql": ["graphql"], "git": ["git", "github", "gitlab", "version control"], "docker": ["docker", "containers"],
    "kubernetes": ["kubernetes", "k8s"], "aws": ["aws", "amazon web services"], "azure": ["azure"],
    "gcp": ["gcp", "google cloud"], "linux": ["linux", "unix"], "ci/cd": ["ci/cd", "cicd", "jenkins", "github actions"],
    "testing": ["pytest", "unit testing", "unittest", "junit", "test automation"], "data structures": ["data structures", "dsa", "algorithms"],
    "oop": ["oop", "object oriented", "object-oriented"], "agile": ["agile", "scrum"],
    "pandas": ["pandas"], "numpy": ["numpy"], "machine learning": ["machine learning", "ml"],
    "microservices": ["microservices"], "celery": ["celery"], "kafka": ["kafka"], "jira": ["jira"],
}

EXTRA = {
    "rust": ["rust"], "php": ["php"], "ruby": ["ruby", "ruby on rails"], "kotlin": ["kotlin"], "swift": ["swiftui", "swift programming"], "scala": ["scala"],
    "bash": ["bash", "shell scripting"], "powershell": ["powershell"], ".net": [".net", "dotnet", "asp.net"], "laravel": ["laravel"],
    "next.js": ["next.js", "nextjs"], "express": ["express.js", "expressjs"], "nestjs": ["nestjs", "nest.js"], "tailwind": ["tailwind", "tailwindcss"],
    "bootstrap": ["bootstrap"], "sass": ["sass", "scss"], "redux": ["redux"], "jquery": ["jquery"], "webpack": ["webpack"], "figma": ["figma"],
    "hibernate": ["hibernate"], "orm": ["orm", "sqlalchemy"], "pydantic": ["pydantic"], "asyncio": ["asyncio", "async programming"],
    "drf": ["drf", "django rest framework"], "mvc": ["mvc"],
    "oracle": ["oracle db", "oracle database", "pl/sql"], "sql server": ["sql server", "mssql", "t-sql"], "dynamodb": ["dynamodb"],
    "elasticsearch": ["elasticsearch"], "cassandra": ["cassandra"], "firebase": ["firebase"], "supabase": ["supabase"], "nosql": ["nosql"],
    "rabbitmq": ["rabbitmq"], "nginx": ["nginx"], "terraform": ["terraform"], "ansible": ["ansible"], "helm": ["helm"],
    "prometheus": ["prometheus"], "grafana": ["grafana"], "ec2": ["ec2"], "s3": ["s3"], "serverless": ["serverless", "aws lambda"],
    "jwt": ["jwt", "json web token"], "oauth": ["oauth", "oauth2"], "authentication": ["authentication", "authorization"],
    "api design": ["api design", "api development"], "websockets": ["websocket", "websockets"], "grpc": ["grpc"],
    "selenium": ["selenium"], "postman": ["postman"], "tdd": ["tdd", "test driven", "test-driven"], "playwright": ["playwright"], "cypress": ["cypress"],
    "scikit-learn": ["scikit-learn", "sklearn"], "tensorflow": ["tensorflow"], "pytorch": ["pytorch"], "nlp": ["nlp", "natural language processing"],
    "deep learning": ["deep learning"], "llm": ["llm", "llms", "large language model", "large language models"], "langchain": ["langchain"],
    "rag": ["rag", "retrieval augmented generation", "retrieval-augmented generation"], "prompt engineering": ["prompt engineering"],
    "data analysis": ["data analysis", "data analytics"], "power bi": ["power bi", "powerbi"], "tableau": ["tableau"],
    "excel": ["microsoft excel", "ms excel", "advanced excel"], "etl": ["etl"], "spark": ["apache spark", "pyspark"], "airflow": ["airflow"],
    "system design": ["system design", "low level design", "high level design"], "design patterns": ["design patterns"],
    "multithreading": ["multithreading", "concurrency"], "problem solving": ["problem solving", "problem-solving"],
    "communication": ["communication skills"], "teamwork": ["teamwork", "team player"],
}
SKILLS.update(EXTRA)

_PATS = {
    skill: [re.compile(r"(?<![a-z0-9+#.])" + re.escape(t) + r"(?![a-z0-9+#])") for t in terms]
    for skill, terms in SKILLS.items()
}


def extract_skills(text):
    text = text.lower()
    return {s for s, pats in _PATS.items() if any(p.search(text) for p in pats)}


def jd_skills(jd):
    """Skill -> weight. 2 = required, 1 = preferred / nice to have."""
    out = {}
    for line in re.split(r"[\n;]|\.\s", jd.lower()):
        w = 1 if re.search(r"preferred|nice to have|plus|bonus|good to have|optional", line) else 2
        for s in extract_skills(line):
            out[s] = max(out.get(s, 0), w)
    return out


def required_years(jd):
    m = re.findall(r"(\d+)\s*\+?\s*(?:-\s*\d+\s*)?(?:years|yrs)", jd.lower())
    return max(map(int, m)) if m else None


HEADINGS = {
    "summary": r"summary|objective|profile", "education": r"education|academic",
    "experience": r"experience|internship|employment", "projects": r"projects?",
    "skills": r"skills|technologies|tech stack", "certifications": r"certifications?|courses|achievements",
}
WEAK = ("responsible for", "worked on", "helped", "involved in", "assisted", "participated", "duties")


def analyze_resume(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    found = {k for l in lines if len(l) < 35 and not re.search(r"\d", l)
             for k, p in HEADINGS.items() if re.search(r"\b(" + p + r")\b", l.lower())}
    contact_missing = []
    if not re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", text): contact_missing.append("email")
    if not re.search(r"(\+?\d[\d\s-]{8,}\d)", text): contact_missing.append("phone")
    if "linkedin" not in text.lower(): contact_missing.append("LinkedIn")
    if "github" not in text.lower(): contact_missing.append("GitHub")
    weak = []
    for l in lines:
        body = re.sub(r"^[•\-*▪●◦·]\s*", "", l)
        bulleted = body != l
        if len(body.split()) < 5: continue
        low = body.lower()
        if low.startswith(WEAK):
            weak.append({"line": body[:140], "reason": "Weak opener. Start with an action verb (Built, Reduced, Designed)."})
        elif bulleted and not re.search(r"\d", body):
            weak.append({"line": body[:140], "reason": "No number or result. Add scale, speed, or users."})
    return {
        "sections_found": sorted(found),
        "missing_sections": [k for k in ("summary", "education", "experience", "projects", "skills") if k not in found],
        "contact_missing": contact_missing, "weak_bullets": weak[:6],
    }


ROADMAP = {
    "docker": "Containerize one of your Flask/FastAPI apps and write a docker-compose with its database.",
    "aws": "Deploy an app on EC2 or Elastic Beanstalk, store files in S3, and learn IAM basics.",
    "fastapi": "Rebuild one Flask API in FastAPI; learn Pydantic models and async endpoints.",
    "kubernetes": "Run a small app on minikube: pods, deployments, services.",
    "redis": "Add Redis caching or rate limiting to an existing project.",
    "ci/cd": "Add a GitHub Actions workflow that runs tests and deploys on push.",
    "testing": "Write pytest tests for your API routes and aim for the core logic first.",
    "react": "Build a small CRUD front end with components, state, and fetch calls.",
    "postgresql": "Move a project from SQLite/MySQL to Postgres; practice joins and indexes.",
    "data structures": "Solve 2 problems a day by topic: arrays, hashing, trees, graphs.",
}

QUESTIONS = {
    "flask": "Explain how Flask routing works and how blueprints help structure a larger app.",
    "fastapi": "How does FastAPI use type hints and Pydantic for validation, and when would you use async endpoints?",
    "django": "Explain Django's request-response cycle and what the ORM does for you.",
    "python": "What is the difference between a list, tuple, set and dict, and when do you pick each?",
    "sql": "Write a query to find the second highest salary. What are the types of joins?",
    "mysql": "What is an index, and how can it slow down writes?",
    "postgresql": "What is the difference between a transaction and a lock, and how do you avoid dirty reads?",
    "git": "What is the difference between merge and rebase? How do you resolve a conflict?",
    "docker": "What is the difference between an image and a container?",
    "javascript": "Explain closures and how the event loop handles async code.",
    "react": "What is the difference between state and props, and when does a component re-render?",
    "rest api": "What makes an API RESTful? Explain PUT vs PATCH and common status codes.",
    "oop": "Explain the four OOP pillars with an example from one of your projects.",
    "html": "What are semantic HTML elements and why do they matter?",
    "css": "Explain the box model and the difference between flexbox and grid.",
}


def analyze(resume_text, jd):
    have = extract_skills(resume_text)
    req = jd_skills(jd)
    matched = sorted(s for s in req if s in have)
    missing = sorted((s for s in req if s not in have), key=lambda s: -req[s])
    total = sum(req.values())
    score = round(100 * sum(req[s] for s in matched) / total) if total else 0
    qs = [f"You list {s} on your resume. {QUESTIONS.get(s, 'Where did you use it, and what trade-off did you face?')}" for s in matched]
    qs += [f"The job asks for {s}, which isn't on your resume. How would you get productive with it in two weeks?" for s in missing[:3]]
    return {
        "score": score, "matched": matched, "missing": missing,
        "required": {s: ("required" if w == 2 else "preferred") for s, w in req.items()},
        "required_years": required_years(jd), "resume": analyze_resume(resume_text),
        "roadmap": [{"skill": s, "hint": ROADMAP.get(s, f"Build one small project with {s} and add it to your resume.")} for s in missing],
        "questions": qs[:10], "resume_skills": sorted(have),
    }
