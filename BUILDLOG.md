# FlyRank Capstone — Build Log

## 2026-09-23 — Widget CRUD API

### Completed
- Implemented widget CRUD management API.
- Added widget database model and service layer.
- Added API schemas for widget creation and updates.
- Verified API through Swagger UI.
- Verified widget creation with HTTP 201.
- Verified widget retrieval with HTTP 200.
- Verified widget update with HTTP 200.
- Verified widget deletion with HTTP 204.
- Added automated widget API tests.
- Test result: 1 passed.

### API Endpoints Verified
- POST /api/widgets
- GET /api/widgets
- GET /api/widgets/{widget_id}
- PUT /api/widgets/{widget_id}
- DELETE /api/widgets/{widget_id}

### Git
Latest commit:
test: add widget API tests

Working tree:
clean

### Notes
Pytest currently reports two dependency deprecation warnings. The test itself passes successfully.
