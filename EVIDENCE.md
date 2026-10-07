# Capstone Evidence

## Behavioral Verification

### 1. Valid submission
A valid submission to the public submission endpoint returned:

- HTTP `201 Created`
- Submission status: `submitted`

### 2. Request validation
Invalid requests were rejected with 4xx responses.

An empty submission returned HTTP `422 Unprocessable Content`.

An oversized message exceeding the 5,000-character boundary returned HTTP `422` with a validation error.

### 3. Rate limiting
The submission endpoint is protected by a `5/minute` rate limit.

The sixth request in a burst returned HTTP `429 Too Many Requests`.

### 4. Honeypot spam protection
A populated honeypot field is rejected with HTTP `400 Bad Request`.

### 5. Idempotency
A submission containing an idempotency key is stored once. Repeating the same request with the same widget and key returns the existing submission instead of creating a duplicate.

### 6. Geographic fallback
The geographic service uses a primary provider and a fallback provider.

When the primary provider was forced to return no result, the fallback provider returned geographic data.

### 7. Both geographic providers unavailable
Both providers were forced down during a test.

The submission still returned HTTP `201 Created` and was stored successfully. Geographic information was allowed to remain unavailable.

### 8. CORS preflight
An `OPTIONS` request with a cross-origin header returned HTTP `200 OK` and included the expected CORS response headers.

### 9. Cross-origin submission
A submission including the origin `http://localhost:5500` returned HTTP `201 Created` and included the corresponding CORS response header.

### 10. Notification failure
A submission tested through the notification-failure path returned HTTP `201 Created`.

This demonstrates that notification failure does not prevent successful database storage.

### 11. Notification retries and failure alert
The notification worker implements retry attempts and logs a critical alert after all configured attempts fail.

### 12. Dashboard statistics
The dashboard statistics endpoint returned aggregated submission counts for the tenant.

Example verified response structure:

```json
{
  "tenant_id": 1,
  "total_submissions": 46,
  "membership_inquiries": 22,
  "general_inquiries": 4
}
