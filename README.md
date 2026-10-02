# 🚀 Viraja

### AI-Powered Career Intelligence Platform

Viraja is a career intelligence platform designed to help students and job seekers **analyze their skills, compare resumes with job descriptions, identify skill gaps, improve career readiness, prepare for interviews, and track job applications**.

> **Status:** 🚧 In Development
> **Deployment:** Coming Soon

---

## 🎯 What is Viraja?

Finding the right career path is difficult when you don't know:

* Which skills a job actually requires
* How well your resume matches a job description
* Which skills you're missing
* What you should learn next
* Whether your resume is strong enough
* What interview questions you should prepare for
* How to keep track of your job applications

Viraja brings these activities together into one platform.

The current system focuses on **resume analysis, job-description matching, skill-gap identification, interview preparation, career guidance, and application tracking**.

---

## ✨ Current Features

### 📄 Resume Analysis

Analyze a resume and identify important information such as:

* Resume sections
* Skills
* Education
* Experience
* Projects
* Certifications
* Missing contact information
* Weak resume bullet points

Viraja also identifies weak bullet-point openings and suggests improving them with stronger action-oriented language.

---

### 🎯 Resume & Job Description Matching

Compare your resume against a job description and generate:

* Match score
* Matched skills
* Missing skills
* Required skills
* Preferred skills
* Required years of experience

This helps users understand how closely their current profile matches a specific opportunity.

---

### 📊 Skill Gap Analysis

Viraja identifies skills requested by a job description that are not present in the resume.

The system categorizes job-description skills as:

* **Required**
* **Preferred**

and calculates a weighted match score based on those requirements.

---

### 📚 Personalized Skill Roadmap

When a skill is missing, Viraja can provide a learning direction for that skill.

Examples include:

* Docker → Containerize an existing application
* AWS → Deploy an application and learn basic AWS services
* FastAPI → Rebuild a Flask API using FastAPI
* Kubernetes → Practice pods, deployments and services
* Redis → Add caching or rate limiting
* CI/CD → Create a GitHub Actions workflow
* Testing → Add automated tests
* React → Build a CRUD frontend
* PostgreSQL → Practice migration, joins and indexes
* Data Structures → Practice problems by topic

---

### 🎤 Interview Preparation

Viraja generates interview questions based on skills detected from the resume and job description.

The current system includes questions for technologies and concepts such as:

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

It can also generate questions around missing skills to help users prepare for technologies requested by the job.

---

### 🤖 Krish Career Coach

Viraja includes **Krish**, an AI-powered career coaching component.

Krish can work with career-related information such as:

* Resume/JD match results
* Matched skills
* Missing skills
* Resume weaknesses
* Job applications
* Learning recommendations
* Interview preparation

> AI-powered functionality requires the appropriate API configuration.

---

### 💼 Job Application Tracking

Users can save and manage job applications with information such as:

* Company
* Job role
* Match score
* Job-description skills
* Skill gaps
* Application status

Application statuses can be updated as the recruitment process progresses.

---

### 📈 Application Statistics

Viraja provides application statistics including information such as:

* Total applications
* Application status counts
* Response rate
* Average match score
* Top skills
* Top skill gaps

This gives users a simple overview of their job-search activity.

---

### 🔐 Authentication & Security

Viraja includes user authentication features such as:

* User registration
* Login
* Logout
* Session-based authentication
* Password reset flow
* Protected application data
* User-specific application access

The application also includes login rate limiting and secure session-cookie configuration.

---

## 🛠️ Technology Stack

### Backend

* Python
* Flask

### Frontend

* HTML
* CSS
* JavaScript

### AI

* Anthropic API integration
* AI-powered career coaching

### Data & Analysis

* Resume text extraction
* Skill detection
* Job-description analysis
* Weighted skill matching

### Development

* Git
* GitHub
* VS Code

---

## 🧠 Skill Intelligence

Viraja contains a broad skill dictionary covering areas including:

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

The skill engine can recognize multiple variations and aliases of technologies.

---

## 📁 Project Structure

```text
Viraja/
│
├── main.py
├── skills.py
├── smoke_test.py
├── requirements.txt
├── .env.example
├── INTERVIEW_NOTES.md
├── README.md
│
└── public/
    └── index.html
```

---

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Shrikrishna2003/Viraja.git
```

### 2. Enter the project directory

```bash
cd Viraja
```

### 3. Create a virtual environment

#### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

---

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 5. Configure environment variables

Create a `.env` file using `.env.example` as your reference.

```text
.env.example
```

Add the required configuration for the services used by your local environment.

**Never upload API keys, passwords, tokens, or other secrets to GitHub.**

---

### 6. Run Viraja locally

```bash
python main.py
```

Then open the local URL provided by the application in your browser.

---

## 🧪 Testing

Viraja includes an end-to-end smoke test covering important application functionality.

Run:

```bash
python smoke_test.py
```

The test checks areas including:

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

A successful run ends with:

```text
ALL PASSED
```

---

## 🔒 Security Considerations

Viraja is designed with basic application security controls including:

* Password-based authentication
* Session-based access control
* HttpOnly session cookies
* SameSite cookie protection
* Login rate limiting
* User-specific application access
* Protected API endpoints
* Environment-variable based secret configuration

This project is still under development and should undergo additional security review before production use.

---

## 🗺️ Roadmap

### Phase 1 — Core Career Intelligence

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
* [x] Krish career coaching

### Phase 2 — Advanced Career Intelligence

* [ ] Advanced AI career recommendations
* [ ] Multi-role career comparison
* [ ] Personalized career roadmaps
* [ ] Improved skill-gap intelligence
* [ ] More advanced interview preparation
* [ ] Better resume improvement recommendations

### Phase 3 — Career Platform

* [ ] Job-role recommendation engine
* [ ] Job matching
* [ ] Personalized learning resources
* [ ] Career progress tracking
* [ ] Advanced interview simulator
* [ ] User dashboard improvements

### Phase 4 — Production Platform

* [ ] Production deployment
* [ ] Production database
* [ ] Scalable infrastructure
* [ ] Mobile optimization
* [ ] Improved observability and monitoring

---

## 🌐 Deployment

Viraja is **currently not deployed**.

The application is being developed and tested locally before production deployment.

> **Live Application:** Coming Soon 🚀

---

## 🔮 Vision

The long-term vision of Viraja is to make career development more **personalized, practical, and data-driven**.

Instead of giving users generic career advice, Viraja aims to help answer:

```text
Where am I now?
        ↓
What does my target role require?
        ↓
What skills am I missing?
        ↓
What should I learn next?
        ↓
How ready am I?
        ↓
How should I prepare?
        ↓
What opportunities should I pursue?
```

The goal is to continuously connect a user's **skills, resume, career goals, learning path, interview preparation, and job applications** in one platform.

---

## 👨‍💻 Developer

### Shrikrishna Tippanna Mokhashi

Computer Science Engineering
Python Full Stack Developer • Software Developer Aspirant

GitHub:

https://github.com/Shrikrishna2003

---

## 📌 Project Status

```text
🟡 Development
🧪 Testing
🚧 Deployment Pending
🔬 Continuous Improvement
```

Viraja is an evolving project. Features, architecture, and roadmap items may change as development continues.

---

## 📄 License

License information will be added as the project approaches its public release.
