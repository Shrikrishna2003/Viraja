# VIRAJA

Match your resume to any job, see the skill gaps, and track every application. **Krish** is the built-in career coach.

## Run locally
    pip install -r requirements.txt
    python -m uvicorn main:app --reload
Open http://127.0.0.1:8000

## Settings (.env)
Copy `.env.example` to `.env` and fill it in. Restart the server after changing it.

| Name | Purpose |
|---|---|
| `SECRET_KEY` | Random 32+ character string that signs sessions. Required in production. Generate: `python -c "import secrets;print(secrets.token_urlsafe(48))"` |
| `DATABASE_URL` | Postgres URL (Neon/Supabase). SQLite is used if unset. Required on Vercel. |
| `BASE_URL` | Public site URL, used in reset links (e.g. https://your-app.vercel.app). |
| `SMTP_HOST` `SMTP_PORT` `SMTP_USER` `SMTP_PASS` `SMTP_FROM` | Sends reset emails (587 STARTTLS or 465 SSL). |
| `AI_PROVIDER` `AI_API_KEY` `AI_MODEL` | Free AI for Krish: `gemini`, `groq`, `openrouter` or `ollama`. |
| `ANTHROPIC_API_KEY` | Alternative: Claude for Krish's AI mode. |

Without SMTP settings, running locally shows the reset link on screen instead of emailing it.

## Krish
Basic coaching (red/amber/green summary, recommendations, 7-day focus) needs no key. With an AI provider set, the AI button runs a tool-calling loop (`get_match_analysis`, `get_application_history`, `get_learning_resource`, `get_interview_questions`), then writes bullet rewrites and a 7-day plan.

## Security
- Argon2id password hashing; older hashes upgrade at next login.
- Session in an `HttpOnly`, `SameSite=Lax` cookie (`Secure` in production), never in `localStorage`.
- Login and reset-request rate limiting (in memory; use Redis for multi-instance production).
- Every query is scoped to the signed-in user.
- The app refuses to start in production without a 32+ character `SECRET_KEY`.
- Never commit `.env`. If a key or password is ever shared, rotate it.
- Not built: email verification, CSRF tokens, OCR for scanned PDFs (paste the text instead).

## Test
    python smoke_test.py                        # local server
    python smoke_test.py https://your-site      # deployed site
Covers signup, cookie flags, login, rate limiting, user isolation, tracker, stats, Krish, reset and logout. It does not upload a PDF.

## Deploy on Vercel
1. Create a free Postgres on Neon or Supabase and copy its connection string.
2. Push this folder to GitHub and import it on vercel.com. Vercel detects `main.py` and serves `public/index.html`.
3. Add the environment variables above (`DATABASE_URL`, `SECRET_KEY`, `BASE_URL`, SMTP, AI settings).
4. Deploy, then run the smoke test against your URL. Krish's AI mode can take 10 to 30 seconds, so check your function timeout.
