# 🚀 Viraja

### AI-Powered Career Intelligence Platform

**Viraja** is an AI-powered career intelligence platform designed to help students and job seekers understand their career readiness, analyze resumes, compare profiles against job descriptions, identify skill gaps, prepare for interviews, and track job applications — all in one place.

Instead of providing generic career advice, Viraja aims to connect a user's **resume, skills, target roles, learning roadmap, interview preparation, and job-search activity** into a single career intelligence system.

> **Status:** 🟢 Live & Continuously Improving
> **Deployment:** Render
> **AI:** Google Gemini
> **Backend:** FastAPI
> **Database:** PostgreSQL

---

## 🌐 Live Demo

### 🚀 Try Viraja

**Live Application:**
https://viraja.onrender.com

**GitHub Repository:**
https://github.com/Shrikrishna2003/Viraja

> The application is currently deployed on Render's free infrastructure and may take some time to wake up after periods of inactivity.

---

# 🎯 What is Viraja?

Finding the right career path can be difficult when you don't know:

* Which skills a target job actually requires
* How closely your resume matches a job description
* Which skills you're missing
* What you should learn next
* Whether your resume is strong enough
* What interview questions you should prepare for
* How your job applications are progressing

Viraja brings these activities together into one platform.

The current platform focuses on:

**Resume Analysis → Job Matching → Skill Gap Analysis → Learning Roadmap → Interview Preparation → AI Career Coaching → Application Tracking**

---

# ✨ Core Features

## 📄 Resume Analysis

Viraja analyzes resume content and identifies important career information such as:

* Resume sections
* Technical skills
* Education
* Experience
* Projects
* Certifications
* Contact information
* Resume weaknesses
* Weak bullet-point openings

Viraja can also identify weak resume bullets and suggest stronger, more action-oriented wording.

---

## 🎯 Resume & Job Description Matching

Compare a resume against a specific job description to understand how closely the candidate matches the opportunity.

Viraja provides information such as:

* Match score
* Matched skills
* Missing skills
* Required skills
* Preferred skills
* Required experience
* Skill-level gaps

The goal is to help users understand **why** they match or don't match a particular role rather than simply providing a score.

---

## 📊 Skill Gap Intelligence

Viraja extracts skills from job descriptions and compares them against the user's resume.

Skills can be categorized as:

* **Required**
* **Preferred**
* **Matched**
* **Missing**

The system uses weighted requirements to calculate a more meaningful job-match score.

This allows users to identify the most important areas they need to improve before applying or interviewing.

---

## 📚 Personalized Skill Roadmap

When Viraja identifies a missing skill, it can provide a practical learning direction.

Examples:

| Skill           | Suggested Direction                               |
| --------------- | ------------------------------------------------- |
| Docker          | Containerize an existing application              |
| AWS             | Deploy an application and learn core AWS services |
| FastAPI         | Rebuild an existing API using FastAPI             |
| Kubernetes      | Practice pods, deployments, and services          |
| Redis           | Add caching or rate limiting                      |
| CI/CD           | Build a GitHub Actions workflow                   |
| Testing         | Add automated tests to an existing project        |
| React           | Build a CRUD application                          |
| PostgreSQL      | Practice migrations, joins, and indexes           |
| Data Structures | Practice problems topic-by-topic                  |

The long-term goal is to turn skill gaps into **actionable learning plans**.

---

# 🎤 Interview Preparation

Viraja generates interview questions based on skills detected from:

* The user's resume
* The target job description
* Missing skills
* Technical requirements

Current interview preparation covers areas such as:

* Python
* Flask
* Django
* FastAPI
* SQL
* MySQL
* PostgreSQL
* Git
* Docker
* JavaScript
* React
* REST APIs
* OOP
* HTML
* CSS

Viraja can also generate questions around missing skills so users can prepare for technologies requested by the target role.

---

# 🤖 Krish — AI Career Coach

Viraja includes **Krish**, an AI-powered career coaching component.

Krish can use career-related context such as:

* Resume analysis
* Job-description analysis
* Resume/JD match results
* Matched skills
* Missing skills
* Resume weaknesses
* Learning recommendations
* Job applications
* Interview preparation

This allows career conversations to be based on the user's actual career data instead of completely generic advice.

### Powered by Google Gemini

Viraja currently supports Gemini as its AI provider.

AI functionality requires the appropriate API configuration.

---

# 💼 Job Application Tracking

Users can save and manage their job applications.

Application information can include:

* Company
* Job role
* Match score
* Job-description skills
* Skill gaps
* Application status

Applications can be updated as they move through the recruitment process.

Example workflow:

```text
Applied
   ↓
Shortlisted
   ↓
Interview
   ↓
Offer
```

---

# 📈 Application Analytics

Viraja provides an overview of the user's job-search activity.

Analytics include information such as:

* Total applications
* Application status counts
* Response rate
* Average match score
* Top skills
* Top skill gaps

This helps users understand patterns in their job search and identify areas that may need improvement.

---

# 🔐 Authentication & Security

Viraja includes authentication and access-control functionality such as:

* User registration
* Login
* Logout
* Session-based authentication
* Password reset flow
* Protected application data
* User-specific application access
* Login rate limiting

Session cookies are configured with security-oriented settings including:

* `HttpOnly`
* `SameSite=Lax`

Sensitive configuration such as API keys, database credentials, and secret keys is handled through environment variables rather than being committed to the repository.

> Viraja is an evolving project and should undergo additional security review before being considered production-ready for sensitive or large-scale usage.

---

# 🧠 Skill Intelligence Engine

Viraja contains a broad skill dictionary covering multiple areas of software development and technology.

Examples include:

```text
Python
Java
JavaScript
TypeScript
C++
C#
Go

HTML
CSS
React
Angular
Vue
Node.js

Flask
Django
FastAPI
Spring Boot

SQL
MySQL
PostgreSQL
MongoDB
Redis
SQLite

REST APIs
GraphQL

Git
Docker
Kubernetes

AWS
Azure
GCP
Linux
CI/CD

Testing
Data Structures
OOP

Pandas
NumPy
Machine Learning

Microservices
Kafka
Jira

LLMs
LangChain
RAG
NLP
Deep Learning

Power BI
Tableau
Spark
Airflow

System Design
Design Patterns
```

The skill engine is designed to recognize different variations and aliases of technologies.

---

# 🏗️ Architecture

At a high level, Viraja follows a simple web application architecture:

```text
                   ┌─────────────────────┐
                   │      User / Browser  │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │   HTML / CSS / JS   │
                   │     Frontend        │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │       FastAPI       │
                   │      Backend        │
                   └──────┬──────┬───────┘
                          │      │
              ┌───────────┘      └────────────┐
              ▼                               ▼
     ┌─────────────────┐             ┌─────────────────┐
     │ PostgreSQL      │             │  Gemini AI      │
     │ Database        │             │  AI Services    │
     └─────────────────┘             └─────────────────┘
```

---

# 🛠️ Technology Stack

## Backend

* Python
* FastAPI
* Uvicorn
* SQLAlchemy
* PostgreSQL

## Frontend

* HTML
* CSS
* JavaScript

## AI

* Google Gemini API

## Data & Intelligence

* Resume text analysis
* Skill extraction
* Job-description analysis
* Weighted skill matching
* Skill-gap detection
* Interview question generation
* Career recommendations

## Authentication & Security

* Session-based authentication
* Secure cookies
* Password hashing
* Rate limiting
* Environment-based secrets

## Development & Deployment

* Git
* GitHub
* VS Code
* Render
* Neon PostgreSQL

---

# 📁 Project Structure

```text
Viraja/
│
├── main.py                  # FastAPI application
├── skills.py                # Skill dictionary and skill intelligence
├── smoke_test.py            # End-to-end application tests
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
├── INTERVIEW_NOTES.md       # Interview preparation notes
├── README.md                # Project documentation
│
└── public/
    └── index.html           # Frontend application
```

---

# ⚙️ Getting Started

## 1. Clone the repository

```bash
git clone https://github.com/Shrikrishna2003/Viraja.git
```

## 2. Enter the project directory

```bash
cd Viraja
```

## 3. Create a virtual environment

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

---

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Configure environment variables

Create a `.env` file based on `.env.example`.

Example configuration structure:

```env
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key

AI_PROVIDER=gemini
AI_API_KEY=your_gemini_api_key
```

Use your own values for each variable.

### ⚠️ Important

Never commit:

```text
.env
API keys
Database passwords
Secret keys
Authentication tokens
```

to GitHub.

The repository should contain `.env.example`, not your real `.env`.

---

# ▶️ Running Viraja Locally

Start the application with:

```bash
uvicorn main:app --reload
```

Then open the local URL shown by Uvicorn, normally:

```text
http://127.0.0.1:8000
```

---

# 🧪 Testing

Viraja includes an end-to-end smoke test for important application functionality.

Run:

```bash
python smoke_test.py
```

The test covers areas including:

* User signup
* Duplicate signup protection
* Login
* Secure session cookies
* Authenticated sessions
* Unauthorized access protection
* Incorrect password handling
* Login rate limiting
* Job application creation
* Application ownership
* Application status updates
* Application statistics
* Krish career coaching
* Forgot-password flow
* Invalid reset-token handling
* Logout/session clearing

A successful test run ends with:

```text
ALL PASSED
```

---

# 🚀 Deployment

Viraja is currently deployed using:

### Application Hosting

**Render**

### Database

**Neon PostgreSQL**

### AI Provider

**Google Gemini**

### Source Control

**GitHub**

### Production Start Command

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Production Build Command

```bash
pip install -r requirements.txt
```

### Live Application

https://viraja.onrender.com

---

# 🗺️ Roadmap

## Phase 1 — Core Career Intelligence

* [x] Resume analysis
* [x] Job description analysis
* [x] Skill extraction
* [x] Resume/JD matching
* [x] Skill-gap analysis
* [x] Skill learning roadmap
* [x] Interview question generation
* [x] Job application tracking
* [x] Application statistics
* [x] Authentication
* [x] Krish AI career coaching
* [x] Cloud deployment

---

## Phase 2 — Advanced Career Intelligence

* [ ] Advanced AI career recommendations
* [ ] Multi-role career comparison
* [ ] Personalized career roadmaps
* [ ] Improved skill-gap intelligence
* [ ] More advanced interview preparation
* [ ] Better resume improvement recommendations
* [ ] Deeper career-readiness analysis

---

## Phase 3 — Career Platform

* [ ] Job-role recommendation engine
* [ ] Job matching
* [ ] Personalized learning resources
* [ ] Career progress tracking
* [ ] Advanced interview simulator
* [ ] User dashboard improvements
* [ ] Career opportunity discovery

---

## Phase 4 — Career Intelligence Ecosystem

* [ ] Real-time job intelligence
* [ ] Personalized opportunity recommendations
* [ ] Intelligent application prioritization
* [ ] Advanced career analytics
* [ ] Learning-resource integration
* [ ] Career progression tracking
* [ ] Mobile experience
* [ ] Scalable infrastructure
* [ ] Advanced observability and monitoring

---

# 🔮 Vision

The long-term vision of Viraja is to make career development more **personalized, practical, measurable, and data-driven**.

Instead of simply telling users:

> "Learn Python."

Viraja aims to answer:

```text
Where am I now?
        ↓
What role am I targeting?
        ↓
What does that role require?
        ↓
How well does my profile match?
        ↓
What skills am I missing?
        ↓
What should I learn first?
        ↓
How can I improve my resume?
        ↓
How should I prepare for the interview?
        ↓
Which opportunities should I pursue?
        ↓
How is my career progress changing?
```

The goal is to continuously connect:

**Skills + Resume + Career Goals + Learning + Interview Preparation + Job Applications**

into one intelligent career platform.

---

# 🌱 Why Viraja?

Most career tools focus on only one part of the journey.

```text
Resume Tools
      │
      ├── Resume building
      │
Job Platforms
      │
      ├── Job discovery
      │
Learning Platforms
      │
      ├── Skill development
      │
Interview Platforms
      │
      └── Interview preparation
```

Viraja aims to connect these stages into a single career intelligence workflow:

```text
                 ┌───────────────┐
                 │     RESUME    │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │  TARGET ROLE  │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │ MATCH ANALYSIS│
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │   SKILL GAP   │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │ LEARNING PATH │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │  INTERVIEW    │
                 │ PREPARATION   │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │ APPLICATIONS  │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │ CAREER DATA   │
                 └───────────────┘
```

This is the direction Viraja is being built toward.

---

# 📊 Project Status

```text
🟢 Core Features        Available
🟢 AI Career Coach      Available
🟢 Authentication       Available
🟢 Application Tracker Available
🟢 PostgreSQL Database  Connected
🟢 Cloud Deployment     Live
🟢 GitHub Repository    Available
🟡 Advanced Features    In Development
🟡 Career Platform      Planned
```

Viraja is an evolving project. The architecture, features, and roadmap may continue to change as the platform develops.

---

# 👨‍💻 Developer

## Shrikrishna Tippanna Mokhashi

Computer Science Engineering

Python Full Stack Developer • Software Developer Aspirant

### GitHub

https://github.com/Shrikrishna2003

### Project

https://github.com/Shrikrishna2003/Viraja

---

# ⭐ Support the Project

If you find Viraja interesting or useful:

* ⭐ Star the repository
* 🍴 Fork the project
* 🐛 Report issues
* 💡 Suggest features
* 🔧 Contribute improvements

---

# 📄 License

License information will be added as the project approaches its public release.

---

## 🚀 Built with curiosity, AI, and a goal to make career development smarter.

**Viraja — From skills to opportunities.**
