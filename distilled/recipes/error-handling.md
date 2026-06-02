# Error Handling Recipe
> Compiled from 15+ canonical works (Pragmatic Programmer, Clean Code, Effective Java, Release It!)

## When to use
Implementing error handling for any non-trivial system. Applies to all phases.

## Principles

### 1. Fail fast, fail loud
- Detect errors at the earliest point
- Throw immediately, don't accumulate
- Silent failures are worse than crashes
- Log with full context (request ID, user ID, input shape)

### 2. Use exceptions for exceptional conditions
- Don't use exceptions for control flow
- Don't use return codes (use exceptions or Result types)
- Don't use null/nil as a "valid" return value
- Don't use sentinel values (-1, empty string)

### 3. Exceptions should carry actionable information
- Type that identifies the kind
- Message that describes what happened (in user terms)
- Cause chain (don't lose the original exception)
- Context (what was the system trying to do?)

### 4. Handle errors at the right level
- Don't catch what you can't handle
- Don't let exceptions bubble up unhandled to the user
- Log at the boundary, then translate to a user-friendly message

## Layered approach

### Layer 1: At the source
```python
def withdraw(account, amount):
    if amount <= 0:
        raise ValueError(f"amount must be positive, got {amount}")
    if amount > account.balance:
        raise InsufficientFundsError(account.id, amount, account.balance)
    # ... do the withdrawal
```

### Layer 2: At the service boundary
```python
class TransferService:
    def transfer(self, from_id, to_id, amount):
        try:
            with self.db.transaction():
                self.accounts.withdraw(from_id, amount)
                self.accounts.deposit(to_id, amount)
        except InsufficientFundsError as e:
            # Log, maybe re-throw with service-level context
            self.logger.warning(f"Transfer failed: {e}")
            raise TransferFailed(from_id, to_id, amount, reason="insufficient_funds")
        except DatabaseError as e:
            self.logger.error(f"DB error during transfer: {e}")
            raise  # let the global handler decide
```

### Layer 3: At the API edge
```python
@app.exception_handler(TransferFailed)
async def handle_transfer_failed(request, exc):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "transfer_failed",
                "message": str(exc),
                "details": {"reason": exc.reason}
            }
        }
    )
```

## Specific error categories

### Validation errors (400 / 422)
- Input doesn't match expected schema
- User-facing message: clear about which field, what's wrong
- Example: "email field: 'foo' is not a valid email address"

### Authentication errors (401)
- "Authentication required" — no detail about what's wrong
- Don't reveal whether email exists (timing attack)
- Generic message: "Invalid credentials"

### Authorization errors (403)
- "You don't have permission to perform this action"
- Don't reveal whether the resource exists (404 vs 403 trade-off)
- Log the attempt for security audit

### Not found (404)
- Generic "Resource not found"
- Or use 403 if you want to hide existence

### Conflict (409)
- "Resource already exists" (duplicate email)
- "Concurrent modification" (optimistic locking failure)
- Include retry guidance

### Rate limit (429)
- "Too many requests"
- Include `Retry-After` header
- Include rate limit headers (`X-RateLimit-*`)

### Server errors (5xx)
- Generic "Something went wrong. Please try again."
- Log the full exception with request_id for support
- NEVER expose stack traces to users in production

## Logging strategy

### What to log
- Request ID, user ID, action
- Time, duration
- Inputs (sanitized — no passwords, no PII)
- Outcome (success/failure with reason)
- Stack trace for errors (with redacted secrets)

### What NOT to log
- Passwords (even hashed)
- Credit card numbers
- Social security numbers
- API keys, tokens
- PII unless required (use structured fields for redaction)

### Log levels
- **ERROR**: requires immediate attention (production failures, security events)
- **WARN**: unexpected but recoverable (retry, fallback, deprecated)
- **INFO**: significant events (user actions, state changes, lifecycle)
- **DEBUG**: verbose for development (function entry/exit, intermediate values)

### Structured logging
- Always use structured logs (JSON, key-value)
- Include request_id in every log message
- Use a logger library that supports this out of the box
- Don't log in tight loops (use sampling or rate limiting)

## Retry strategy

### When to retry
- Network errors (timeout, connection reset, 503)
- Rate limit responses (429 with Retry-After)
- Transient DB errors (deadlock, lock timeout)

### When NOT to retry
- 4xx client errors (your bug, retrying won't help)
- Authentication errors (refresh the token first)
- Business rule violations (409 conflict)

### Retry with exponential backoff
```
attempt 1: try
attempt 2: wait 100ms, try
attempt 3: wait 200ms, try
attempt 4: wait 400ms, try
attempt 5: wait 800ms, try
attempt 6: give up, fail
```
- Add jitter (random factor) to avoid thundering herd
- Cap total time (e.g., 30 seconds max)
- Use a library (e.g., tenacity for Python, resilience4j for Java)

## Circuit breaker pattern

When calling an unreliable external service:
- **Closed**: requests flow normally
- **Open**: requests fail fast (don't call the broken service)
- **Half-open**: try a few requests to see if it recovered

Use a library (Hystrix-style). Don't roll your own.

## Bulkhead pattern

Isolate failures: separate thread pools / connection pools for different external dependencies.
If one goes down, only its pool is exhausted, others continue.

## Verification checklist

- [ ] All exceptions carry actionable context
- [ ] No silent catches (try/except that just logs and continues)
- [ ] Errors logged with request_id and full context
- [ ] No secrets or PII in logs
- [ ] User-facing errors are friendly, not technical
- [ ] Server errors return generic message, full detail in logs
- [ ] Retries use exponential backoff with jitter
- [ ] Circuit breakers for external dependencies
- [ ] Bulkheads isolate failure domains
- [ ] Test the error paths, not just the happy paths
- [ ] Test with realistic failure injection (kill a service, return 500s, etc.)

## Anti-patterns to avoid

- **Empty catch blocks**: `try { ... } catch (e) {}`
- **Catch generic Exception**: catches everything including programmer errors
- **Return null on error**: forces every caller to null-check
- **Log and rethrow**: same error logged twice
- **Swallow in async code**: errors vanish in fire-and-forget
- **Tight coupling to exception types**: catch by interface, not concrete class
- **Error message with implementation details**: "NullPointerException at UserService.java:42"

## Related
- See `risks/reliability-risks.md` for the failure modes
- See `checklists/p6-verification.md` for chaos engineering / failure injection tests
