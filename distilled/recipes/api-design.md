# API Design Recipe
> Compiled from 25+ canonical API design references (O'Reilly, Apigee, Google, Microsoft)

## When to use
Designing any HTTP API. Steps apply to REST, GraphQL, gRPC — the principles overlap.

## Steps

### 1. Identify resources (nouns, not verbs)
- Resources = things in your domain (User, Order, Product)
- Actions = HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Wrong: `POST /createUser`, `GET /getUsers`
- Right: `POST /users`, `GET /users`

### 2. Choose URI design pattern
- Plural nouns: `/users`, `/users/{id}`, `/users/{id}/orders`
- Avoid verbs in URIs (use HTTP methods instead)
- Hierarchical relationships: `/users/{id}/orders/{orderId}`
- For complex queries: `/users?role=admin&status=active` (filter, not path)

### 3. HTTP methods — what each means
- `GET` — safe, idempotent, cacheable. No side effects.
- `POST` — create new resource. Returns 201 + Location header.
- `PUT` — full update or create. Idempotent. Replaces entire resource.
- `PATCH` — partial update. NOT idempotent by default (depends on JSON Patch / Merge Patch).
- `DELETE` — idempotent. Returns 204 or 200 with body.
- `HEAD` — like GET but no body. For checking existence.
- `OPTIONS` — CORS preflight + capability discovery.

### 4. Status codes
- `200` — OK (with body)
- `201` — Created (with Location header for new resource)
- `204` — No Content (success, no body)
- `301` — Moved Permanently
- `304` — Not Modified (use with ETag/If-Modified-Since)
- `400` — Bad Request (malformed)
- `401` — Unauthorized (not authenticated)
- `403` — Forbidden (authenticated but not allowed)
- `404` — Not Found
- `409` — Conflict (concurrent modification, business rule violation)
- `410` — Gone (permanently removed)
- `422` — Unprocessable Entity (well-formed but semantically wrong)
- `429` — Too Many Requests (rate limiting)
- `500` — Internal Server Error (your bug)
- `502/503/504` — Upstream/gateway/timeout issues

### 5. Versioning
Pick one and stick with it:
- **URI versioning**: `/v1/users` — simple, cacheable, visible
- **Header versioning**: `Accept: application/vnd.myapi.v1+json` — cleaner URIs
- **Media type**: best REST, harder to debug
- **No versioning**: only for internal APIs with single consumer
Recommendation: **URI versioning for external APIs** (it's visible, debuggable, cache-friendly). For internal APIs, header versioning is fine.

### 6. Pagination
- **Offset pagination**: `?offset=20&limit=10` — simple, but slow for large offsets, inconsistent under writes
- **Cursor pagination**: `?after=xyz&limit=10` — stable, fast, no skipping records, but no random access
- **Keyset pagination**: `?after_id=42&after_created_at=2024-01-01` — efficient for indexed columns
- Default: cursor pagination. Use offset only for admin/back-office UIs.

### 7. Filtering, sorting, search
- Filtering: `?status=active&role=admin` (AND by default, document OR semantics if needed)
- Sorting: `?sort=-created_at,name` (prefix `-` for DESC)
- Search: `?q=keyword` (full-text search; consider dedicated search endpoint for complex queries)
- Field selection (sparse fieldsets): `?fields=id,name,email` (return only requested fields)

### 8. Error responses — ALWAYS consistent
```json
{
  "error": {
    "code": "user_not_found",
    "message": "The user with id 42 was not found",
    "details": { "user_id": 42 },
    "request_id": "abc-123",
    "documentation_url": "https://docs.example.com/errors/user_not_found"
  }
}
```
- `code` — machine-readable, stable across versions
- `message` — human-readable, may change
- `details` — structured context
- `request_id` — for support correlation
- `documentation_url` — link to fix instructions

### 9. Authentication & authorization
- Use `Authorization: Bearer <token>` header (not cookies for APIs unless same-origin)
- Tokens: short-lived access + long-lived refresh
- Authorization: scopes/permissions IN the token, enforced at the edge
- Document the auth scheme in OpenAPI

### 10. Rate limiting
- Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`
- Status: `429 Too Many Requests` with `Retry-After`
- Be liberal: 1000 req/hour is a starting point for most APIs
- Different limits per endpoint class (read vs write)

### 11. Caching
- `Cache-Control: max-age=...` for safe-to-cache responses
- `ETag` + `If-None-Match` for conditional requests → 304 Not Modified
- `Vary: Accept-Encoding, Authorization` for content-negotiated responses

### 12. Documentation
- **OpenAPI 3.1** (formerly Swagger) — the de facto standard
- Generate client SDKs from the spec (openapi-generator, fern, speakeasy)
- Host interactive docs (Redoc, Swagger UI, Stoplight)
- Include examples for every endpoint
- Document errors, not just happy paths

## Anti-patterns to avoid
- **Verbs in URIs** (`/getUser`, `/createOrder`)
- **Mixing singular/plural** (`/user/{id}` next to `/orders`)
- **Hiding errors behind 200** (return 200 with `{"success": false}`)
- **Returning all data, always** (no pagination, no field selection)
- **No versioning** (breaking changes break clients)
- **HTML in JSON responses** (or vice versa)
- **Different error formats per endpoint** (inconsistency is hell)
- **Custom auth schemes** (roll your own crypto)
- **Exposing internal IDs** (leak information about scale)

## Verification checklist
- [ ] Resources are nouns, methods are HTTP verbs
- [ ] Plural noun URIs consistently
- [ ] Status codes follow HTTP semantics
- [ ] Versioning strategy documented and applied
- [ ] Pagination implemented and documented
- [ ] Error responses use a single, consistent format
- [ ] Rate limiting in place
- [ ] Authentication scheme documented
- [ ] Caching headers where applicable
- [ ] OpenAPI spec generated and published
- [ ] No business logic in the API layer (delegate to domain)

## Related
- See `checklists/p5-construction.md` for API implementation checks
- See `checklists/p6-verification.md` for API testing strategy
- See `comparisons/rest-vs-graphql.json` for protocol choice
