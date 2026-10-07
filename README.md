# Embeddable Widget & Lead-Capture Platform

A FastAPI-based embeddable widget platform for collecting gym membership inquiries, hotel guest inquiries, and general fitness-related leads.

## Features

- Widget CRUD management
- Tenant isolation
- Public embeddable JavaScript widget
- Submission API
- Request validation
- CORS and OPTIONS preflight support
- Rate limiting
- Honeypot spam protection
- Idempotency protection
- Geographic lookup with provider fallback
- Graceful storage when geo providers fail
- Notification processing with retries
- Failure alert logging
- Dashboard submission statistics
- PostgreSQL/SQLAlchemy persistence

## Architecture

The application is organized into:

- `app/api/` — HTTP API routes
- `app/models/` — SQLAlchemy database models
- `app/schemas/` — Pydantic validation schemas
- `app/services/` — business services such as geo lookup and notifications
- `app/workers/` — background/retry processing
- `frontend/` — embeddable widget files

## Run locally

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
