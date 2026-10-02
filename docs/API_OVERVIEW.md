# API Overview

Swagger: `/docs`

- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET /api/auth/me`
- `POST /api/resumes/upload`
- `GET /api/resumes`
- `GET /api/resumes/{resume_id}`
- `POST /api/jobs`
- `GET /api/jobs?q=&title=&skills=&location=&experience_level=`
- `GET /api/jobs/{job_id}`
- `PUT /api/jobs/{job_id}`
- `DELETE /api/jobs/{job_id}`
- `POST /api/matching/resume/{resume_id}/job/{job_id}`
- `GET /api/matching/resume/{resume_id}/recommendations`
- `GET /api/matching/resume/{resume_id}/improvement?job_id=`
- `POST /api/career/ask`
