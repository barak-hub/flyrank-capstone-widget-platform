# FlyRank Backend AI Engineering Capstone
## Embeddable Widget & Lead-Capture Platform

### 1. Problem

Build an embeddable lead-capture platform for a hotel gym. The widget will allow visitors to submit gym membership enquiries, general enquiries, and hotel-guest requests.

The hotel gym provides access to the gym, sauna, steam room, and swimming pool. Hotel guests must provide their room number and present their physical room key/card to gym staff for verification.

The platform will validate submissions, reduce spam, enrich submissions with approximate geographic information, store them safely, and provide dashboard statistics to authorized staff.

### 2. Actors and Use Cases

- Hotel/gym staff: authenticate and manage widgets and view dashboard statistics.
- Existing gym member: submit an enquiry using membership ID and email/phone.
- Prospective member: submit a membership enquiry using contact information.
- General visitor: submit a general enquiry.
- Hotel guest: submit a request with a required room number. Physical key/card verification remains with gym staff.

### 3. Data Model

#### Tenant
- id
- name
- created_at

#### Widget
- id
- tenant_id
- name
- widget_type
- status
- version
- created_at
- updated_at

Indexes:
- tenant_id

#### Submission
- id
- tenant_id
- widget_id
- request_type
- visitor_name
- email
- phone
- membership_id
- room_number
- message
- ip_address
- geo_country
- idempotency_key
- created_at

Indexes:
- tenant_id
- widget_id
- created_at
- unique constraint on (widget_id, idempotency_key)

Every widget belongs to one tenant. Every submission belongs to both a tenant and widget.

### 4. API Surface

#### Authenticated Management API

POST   /api/widgets
GET    /api/widgets
GET    /api/widgets/{widget_id}
PUT    /api/widgets/{widget_id}
DELETE /api/widgets/{widget_id}

#### Public Widget Delivery

GET /api/public/widgets/{widget_id}/config
GET /widget/{version}/widget.js

#### Public Submission API

OPTIONS /api/public/widgets/{widget_id}/submissions
POST    /api/public/widgets/{widget_id}/submissions

The public submission endpoint will perform CORS handling, boundary validation, rate limiting, spam prevention, geo enrichment, persistence, and asynchronous notification.

#### Dashboard API

GET /api/dashboard/widgets/{widget_id}/stats

### 5. Architecture

Customer Website
       |
       v
Embeddable Widget
       |
       +----> Public Config API
       |
       +----> Public Submission API
                    |
                    v
             CORS + Validation
                    |
                    v
          Rate Limit + Spam Check
                    |
                    v
             Geo Provider A
                    |
              fallback
                    v
             Geo Provider B
                    |
                    v
             PostgreSQL
                    |
                    v
          Background Notification
             /             \
          success        failure
                          |
                        retry
                          |
                    failure alert

Hotel/Gym Staff
       |
       v
Authenticated Management API
       |
       v
Tenant-Isolated Service Layer
       |
       v
PostgreSQL

Hotel/Gym Staff
       |
       v
Dashboard API
       |
       v
Submission Statistics

### 6. Validation, Security and Reliability

- Authenticated management endpoints will enforce tenant isolation.
- Public endpoints will validate input at the API boundary.
- Malformed and oversized requests will receive appropriate 4xx responses.
- CORS will support the second-origin customer website and OPTIONS preflight.
- Rate limiting will return HTTP 429 when limits are exceeded.
- A spam-control mechanism will include a honeypot field.
- Submission requests will support idempotency keys so retries do not create duplicate submissions.
- Geo enrichment will use provider A with provider B as a fallback.
- If both geo providers fail, the submission will still be stored.
- Notification/email or webhook failure will not prevent successful persistence.
- Notification processing will run as a background job with retries and failure alerting.
- Secrets will be stored in environment variables and never committed to Git.

### 7. Embed Flow

An authenticated hotel/gym staff member creates a widget.

The platform generates an embed snippet containing the widget identifier.

A customer website loads the versioned widget JavaScript.

The JavaScript retrieves public widget configuration and renders the widget.

Visitors submit enquiries through the public submission API.

### 8. Explicit Non-Goal

The platform will not integrate with hotel door-lock systems or fingerprint/biometric hardware, and it will not store raw biometric data. Physical room-key/card verification and any fingerprint verification will remain outside the platform.

### 9. Technology Stack

- Python
- FastAPI
- PostgreSQL
- Docker
- SQLAlchemy
- Pydantic
- Git/GitHub

### 10. Design Goal

The core goal is to demonstrate a secure, tenant-isolated, persistent, embeddable lead-capture platform that handles validation, abuse protection, failure recovery, asynchronous side effects, and dashboard reporting.
