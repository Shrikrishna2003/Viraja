# VIRAJA: how to explain it

**Auth flow.** Signup hashes the password with Argon2id. Login verifies it and sets a signed session cookie (HMAC-SHA256 over a JSON payload with an expiry, 7 days) that is `HttpOnly`, `SameSite=Lax` and `Secure` in production, so page scripts cannot read it. The `uid` dependency verifies it on every protected route. Password reset uses a separate 30-minute token tied to the current password hash, so it stops working once the password changes.

**Why FastAPI.** Pydantic validates request bodies, dependency injection makes auth one reusable function, and it is light enough for serverless.

**Why PostgreSQL.** Safe concurrent writes and a hosted free tier. SQLAlchemy lets the same code run on SQLite locally and Postgres in production through `DATABASE_URL`.

**Matching algorithm.** A curated skills dictionary with synonyms and word-boundary regex (so `js` is JavaScript but `node.js` is not mistaken for `js`). JD lines containing "preferred" or "nice to have" weigh 1, everything else weighs 2. Score = matched weight / total weight. It is deterministic, so the same inputs always give the same score and every number can be explained.

**Why not an LLM for the score.** LLM scores vary between runs and can't be justified. The LLM is used where language matters: rewriting bullets and writing the plan.

**How Krish uses tools.** The server sends the model four tool definitions. The model replies with tool calls, the server runs them (match analysis, application history, learning resource, interview question), sends results back, and repeats until the model returns final JSON. Maximum 6 rounds. Every tool reads data scoped to the signed-in user.

**User isolation.** Every query filters on the `user_id` from the verified token, and update/delete check ownership. `smoke_test.py` proves user B cannot read, edit or delete user A's application.

**Rate limiting.** Five failed logins per IP and email, and five reset requests per IP, within 15 minutes, then HTTP 429. It is in memory, so it resets on restart and is per instance. Production would use Redis.

**Scanned PDFs.** Text is extracted with pypdf. If a PDF has no text layer the user can paste their resume text instead. Real OCR (Tesseract) needs system binaries, so it is not built.

**Honest limitations (say these first).** No CSRF token (SameSite=Lax cookies cover the common cases). Existing sessions stay valid for 7 days after a password reset. The skills list is about 150 entries with synonyms, so matching is keyword-based, not semantic. Free AI tiers have daily request limits.
