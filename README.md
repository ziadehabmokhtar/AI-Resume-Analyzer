# AI Resume Analyzer


**Author:** Zyad  
**Specialization:** Information Systems & AI

A modular web application implementing the supplied SRS: authentication, PDF/DOCX resume upload and analysis, job management/search, job matching, resume improvement, three AI agents, local RAG, REST API documentation, demo data, tests and an ER diagram.

## SRS coverage
The implementation follows the supplied SRS. The source specifies Python/FastAPI, SQLite, HTML/CSS/Vanilla JavaScript, FR-1 through FR-7, three AI agents, RAG knowledge categories, non-functional requirements, deliverables and a 100-mark evaluation split.

## Technologies
- Python 3.11+ recommended
- FastAPI + Uvicorn
- SQLite + SQLAlchemy
- Pydantic
- PyJWT + bcrypt/passlib
- pypdf + python-docx
- scikit-learn TF-IDF vector retrieval for a local, dependency-light RAG implementation
- HTML, CSS, Vanilla JavaScript
- Optional OpenAI-compatible LLM API through environment variables

## Project structure
```text
AI-Resume-Analyzer/
├── backend/
│   ├── main.py
│   ├── database/ session.py
│   ├── models/ entities.py
│   ├── schemas/ schemas.py
│   ├── routers/ auth.py resumes.py jobs.py matching.py career.py
│   ├── services/ ai_client.py file_parser.py resume_service.py
│   ├── agents/ resume_analyzer.py job_matching.py career_advisor.py
│   ├── rag/ retriever.py service.py
│   └── utils/ config.py security.py
├── frontend/ (HTML/CSS/Vanilla JS)
├── data/knowledge_base/
├── docs/ER_DIAGRAM.md
├── tests/
├── uploads/
├── requirements.txt
├── .env.example
└── README.md
```

## Installation
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```
If PowerShell blocks activation, use the process-scoped execution-policy workaround appropriate for your machine, then activate the environment again.

## Environment variables
`.env` should contain:
```env
JWT_SECRET_KEY=your-long-random-secret
AI_API_KEY=your-provider-key
AI_BASE_URL=https://api.openai.com/v1
AI_MODEL=gpt-4o-mini
```
`AI_API_KEY` is optional for local demo operation. Without it, the agent classes use deterministic local fallbacks. With it, they call the configured OpenAI-compatible model. Never commit `.env`.

## Database
SQLite is created automatically as `resume_analyzer.db` on first run. Tables are created from SQLAlchemy models and demo jobs are seeded if the jobs table is empty.

## Run
```powershell
uvicorn backend.main:app --reload
```
Open `http://127.0.0.1:8000/` for the UI and `http://127.0.0.1:8000/docs` for Swagger/OpenAPI.

## Authentication
Registration and login return a JWT. Passwords are protected with salted PBKDF2-HMAC-SHA256 hashing. Protected endpoints require `Authorization: Bearer <token>`. Logout is client-side token removal because JWTs are stateless.

## Resume pipeline
Upload → extension/size/empty validation → file storage → PDF/DOCX extraction → text cleaning → Resume Analyzer Agent → structured fields stored in SQLite.

## AI agents
1. **Resume Analyzer Agent**: extracts contact details, education, experience, technical/soft skills and summary.
2. **Job Matching Agent**: compares resume and job, computes an explainable score and returns matching/missing skills.
3. **Career Advisor Agent**: asks the RAG layer for retrieved knowledge and generates career guidance when an AI key is configured.

## Matching algorithm
The deterministic score is deliberately explainable:
- Skills: 60%
- Experience: 25%
- Education: 15%

`score = 0.60 * skills_score + 0.25 * experience_score + 0.15 * education_score`, then multiplied by 100. Skills are exact normalized intersections with required skills. Experience and education use conservative evidence-based heuristics. The AI layer can explain the result but does not replace the numeric formula.

## RAG
The knowledge base contains sample job descriptions, skill descriptions, career roadmaps, learning resources and resume-writing guidelines. These are explicitly fictional/sample content unless otherwise stated.

At startup, `KnowledgeBase` loads `.md/.txt/.json` files, splits them into chunks, builds a TF-IDF vector matrix, retrieves the top relevant chunks with cosine similarity, and passes only those retrieved chunks plus the query/resume context to the Career Advisor. This is a real retrieval-then-generation flow; it is intentionally local so the project can run without a hosted vector database.

## API documentation
FastAPI automatically publishes OpenAPI and Swagger UI at `/docs` and ReDoc at `/redoc`. Main route groups: `/api/auth`, `/api/resumes`, `/api/jobs`, `/api/matching`, `/api/career`.

## Frontend demo flow
1. Register.
2. Login.
3. Upload a PDF/DOCX resume.
4. Review structured analysis.
5. Search/browse sample jobs.
6. Click **Match Resume** to see score, matching/missing skills and improvement guidance.
7. Ask a career question in Career Advisor; retrieved source names are shown.

## Testing
```powershell
pytest -q
```
AI calls are optional in tests; local fallback behavior makes the suite deterministic and avoids requiring an external API key.

## Error handling and security
The application validates credentials, duplicate emails, authorization, file extension, size and readable content; uses meaningful HTTP errors; hashes passwords; reads secrets from environment variables; and avoids returning stack traces to normal API consumers.

## ER diagram
See `docs/ER_DIAGRAM.md`. It documents Users → Resumes and Match Results relationships plus Jobs. The current matching endpoint computes results on demand; the `match_results` table is retained as the logical persistence point for future/audit use.

## Known scope decision
The SRS does not define an external data provider, exact LLM vendor, exact scoring weights, or an administrator role. This implementation chooses a local sample knowledge base, an OpenAI-compatible optional provider, a documented 60/25/15 matching formula, and authenticated job CRUD to keep the project simple and aligned with the stated requirements.

## Evaluation alignment
The project structure directly addresses Backend, Frontend, SQLite Database, Resume Analysis, AI Agents, RAG, Code Quality/Error Handling and Documentation criteria listed in the SRS.
