# 🚀 FastAPI User Management System

This project implements a secure and robust REST API using FastAPI and PostgreSQL, designed for managing users with full CRUD operations, role-based access control (RBAC), and OAuth2 authentication.

Through this assignment, I gained a deeper understanding of FastAPI, Pydantic models, OAuth2 with the password flow, and writing effective unit tests using Pytest and async fixtures. I learned how to isolate bugs quickly, particularly with token-based authentication, field validation, and schema interactions like model_dump vs model_validate.

One of the more challenging aspects was ensuring compatibility between Pydantic V2 models and raw SQLAlchemy ORM models, especially when combining HATEOAS-style responses. Writing comprehensive tests and mocking external services (like SMTP for email) pushed me to think like a QA engineer and build for edge cases.

This project also helped me practice clean GitHub collaboration, documenting issues, and using pull requests to break work into manageable pieces. Overall, I’m leaving this experience with sharper debugging, validation, and test coverage skills — and a better appreciation for structured API development.
---

## 🛠️ Closed Issues

1. [#1: Fix incorrect email or password message using OAuth2 login](https://github.com/your-username/your-repo/issues/1)
2. [#2: Ensure URL fields validate properly in User schemas](https://github.com/your-username/your-repo/issues/2)
3. [#3: Prevent update when no fields provided (UserUpdate schema)](https://github.com/your-username/your-repo/issues/3)
4. [#4: Instructor demo bug - `model_dump` usage on ORM models](https://github.com/your-username/your-repo/issues/4)
5. [#5: Enforce role-based access for admin/manager endpoints](https://github.com/your-username/your-repo/issues/5)

All issues are resolved through PRs and merged into `main` following GitHub flow. Each includes:
- A clear problem statement
- Linked test case(s)
- Application-level changes
- Final outcome with success criteria

---

## 🐳 Docker Image

Deployed on DockerHub:  
👉 [https://hub.docker.com/r/your-username/your-image-name](https://hub.docker.com/r/your-username/your-image-name)

To run locally:

```bash
docker compose up --build

