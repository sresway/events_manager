# FastAPI User Management System

This project implements a secure and robust REST API using FastAPI and PostgreSQL, designed for managing users with full CRUD operations, role-based access control (RBAC), and OAuth2 authentication.

Through this assignment, I gained a deeper understanding of:
- FastAPI
- Pydantic v2
- OAuth2 password flow
- Writing robust unit and integration tests using Pytest and `pytest-asyncio`
- Schema validation strategies and `model_dump` vs `model_validate`
- Token-based authentication edge cases
- HATEOAS-style API response links

One of the more challenging aspects was aligning raw SQLAlchemy ORM objects with Pydantic V2 models, especially when creating structured `UserResponse` outputs. I also became much more comfortable debugging token parsing issues, field mismatches, and role-based access control logic.

This project helped me build cleaner test coverage (90%+), structure tests with reusable fixtures, and mock complex components like email verification using `mock_smtp`. I also learned to manage Docker services and CI coverage more fluently.

---

## 🚀 New Feature: Upgrade User to Professional

We added a secure endpoint that allows **Admins and Managers** to upgrade any user to a professional account:

**Route:** `POST /users/{user_id}/upgrade`  
**Logic:** 
- Only users with `ADMIN` or `MANAGER` roles may invoke this
- Internally uses `UserService.upgrade_to_professional()`
- Includes full test coverage for success, insufficient role, and non-existent user edge cases

✅ This feature was tested via:
- `test_upgrade_user_to_professional_success`
- `test_upgrade_user_to_professional_forbidden`
- `test_upgrade_to_professional_user_not_found`
- `test_upgrade_to_professional_insufficient_role`

---

## ✅ Closed GitHub Issues

| Issue | Description |
|-------|-------------|
| [#1](https://github.com/sresway/events_manager/issues/1) | Schema URL field validation |
| [#2](https://github.com/sresway/events_manager/issues/2) | JWT login fails for locked or unverified users |
| [#3](https://github.com/sresway/events_manager/issues/3) | Alembic migrations not running in Docker |
| [#4](https://github.com/sresway/events_manager/issues/4) | Profile, LinkedIn, GitHub URL validation in schema |
| [#5](https://github.com/sresway/events_manager/issues/5) | Role-based access control (RBAC) on user endpoints |
| [#6](https://github.com/sresway/events_manager/issues/6) | Add `upgrade_to_professional()` route and service |
| [#7](https://github.com/sresway/events_manager/issues/7) | Fix Pydantic model validation errors in upgrade route |
| [#8](https://github.com/sresway/events_manager/issues/8) | Add missing tests for professional upgrade scenarios |

Each issue was resolved through a pull request with:
- A descriptive summary
- Linked test case(s)
- CI/CD validation through GitHub Actions

---

## 🧪 Coverage

- ✅ 100% coverage on models and schemas
- ✅ Over 30 tests written with `pytest-asyncio`
- ✅ All services tested including login, registration, RBAC, and professional upgrades
- ✅ Final test run: **98 passed, 1 skipped, 0 failed**

---

## 📦 Docker Deployment

**DockerHub Repo:**  
[https://hub.docker.com/repository/docker/sre25/event_manager/general](https://hub.docker.com/repository/docker/sre25/event_manager/general)

**Run locally:**

```bash
docker compose up --build
