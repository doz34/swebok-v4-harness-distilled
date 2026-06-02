# Authentication Recipe
> Compiled from 20+ canonical works (OWASP ASVS, NIST 800-63, OAuth 2.0 RFCs, WebAuthn spec)

## When to use
Implementing any user authentication system. Modern best practices only.

## Architecture: Token-based with refresh

```
User → Client (browser/app)
         │
         ├─ POST /auth/login (email, password) ──→ Server
         │                                         │
         │   ← { access_token, refresh_token } ←───┤
         │                                         │
         ├─ API request with Authorization: Bearer <access_token>
         │                                         │
         │   ← 401 if access_token expired ─────────┤
         │                                         │
         ├─ POST /auth/refresh (refresh_token) ───→ Server
         │   ← { new access_token, new refresh_token } ←┤
         └─ Retry the API request
```

## Password storage

**Use Argon2id** (winner of the Password Hashing Competition). Parameters:
- `time_cost`: 2-4 iterations
- `memory_cost`: 64-256 MiB
- `parallelism`: 1-4 (match CPU cores)
- `salt`: random per password, 16+ bytes

```python
import argon2
ph = argon2.PasswordHasher(
    time_cost=3,
    memory_cost=65536,  # 64 MiB
    parallelism=4,
    hash_len=32,
    salt_len=16,
)
hash = ph.hash(password)
ph.verify(hash, password)  # raises if wrong
```

Alternatives (in order of preference):
- Argon2id > Argon2i > Argon2d
- bcrypt (still acceptable, cost >= 12)
- scrypt (acceptable)
- PBKDF2 (acceptable, but more iterations needed)
- ❌ MD5, SHA1, SHA256, SHA512 (NEVER for passwords — too fast)

## Password policy (NIST 800-63B)

Modern NIST guidance: **DON'T enforce complexity rules**. Instead:
- Minimum length: 8 characters (12+ preferred)
- Maximum length: at least 64 characters (allow passphrases)
- Allow all printable characters including spaces and Unicode
- Check against breach databases (HaveIBeenPwned API)
- No composition rules (must have uppercase + number + symbol)
- No forced rotation unless breach suspected

## Multi-factor authentication

**Always offer TOTP at minimum.** Better: WebAuthn / passkeys.

### TOTP (Time-based One-Time Password)
- RFC 6238 standard
- 6-digit code, 30-second window, ±1 step tolerance
- Shared secret generated on enrollment, shown as QR code (otpauth URI)
- Server stores secret encrypted (it's a long-lived credential)

### WebAuthn / Passkeys (preferred)
- Public-key cryptography, no shared secret
- Resistant to phishing (origin-bound)
- Biometric or device PIN
- Use SimpleWebAuthn library, webauthn.io for testing

### SMS (avoid if possible)
- Vulnerable to SIM swap attacks
- SS7 vulnerabilities
- Use only as last resort, with rate limits

## Session management

For server-rendered apps (cookies, not tokens):
- `HttpOnly` cookies (no JS access)
- `Secure` cookies (HTTPS only)
- `SameSite=Lax` or `Strict` (CSRF protection)
- Session ID: cryptographically random, 128+ bits
- Regenerate session ID on login (prevent fixation)
- Idle timeout: 15-30 min for sensitive apps
- Absolute timeout: 8-24 hours, re-auth required after

## OAuth 2.0 (third-party auth)

**Use OpenID Connect for "log in with X" flows.** Don't roll your own.

Common flows:
- **Authorization Code + PKCE**: for all client types (web, mobile, SPA)
- **Client Credentials**: for service-to-service
- ❌ **Implicit flow**: deprecated, don't use
- ❌ **Resource Owner Password Credentials**: only for trusted first-party apps

Scopes: be granular. `openid email profile` minimum, add app-specific.

## JWT (if using)

- **Access tokens**: short-lived (15 min - 1 hour), stateless, signed (RS256 preferred over HS256 for distributed verification)
- **Refresh tokens**: long-lived (days/weeks), stored securely (HttpOnly cookie or secure storage)
- Always validate: signature, issuer, audience, expiration, not-before
- Use a library (don't roll your own)
- Consider JWT size — they're not free (every request carries them)

## Common mistakes to avoid

- **Storing passwords in plaintext or reversible encryption**: just don't
- **Using the same salt for all passwords**: defeats per-user cracking limits
- **Logging credentials**: scrub logs for password fields
- **Returning the password hash in API responses**: never
- **Using GET for logout**: CSRF risk, log pollution
- **Forgetting to invalidate sessions on password change**
- **Trusting client-side auth checks**: always re-check on server
- **Rate limiting on the wrong path**: rate-limit by IP AND by user
- **Insecure password reset**: don't send the password; send a one-time token
- **No brute-force protection**: rate-limit + lockout + captcha

## Verification checklist

- [ ] Passwords hashed with Argon2id (or bcrypt cost >= 12)
- [ ] Per-user salt (handled by Argon2/bcrypt automatically)
- [ ] No password complexity rules; minimum 12 chars
- [ ] MFA available (TOTP or WebAuthn)
- [ ] Session/cookie flags: HttpOnly, Secure, SameSite
- [ ] Session ID regenerated on login
- [ ] Access tokens short-lived, refresh tokens long-lived
- [ ] Rate limiting on auth endpoints
- [ ] All credentials scrubbed from logs
- [ ] Account lockout / captcha after N failed attempts
- [ ] Password reset uses one-time tokens, never sends password
- [ ] Security headers (CSP, HSTS, X-Frame-Options, X-Content-Type-Options)
- [ ] Tested for: SQLi, XSS, CSRF, clickjacking, session fixation, IDOR
- [ ] Tested with OWASP ZAP or Burp Suite

## Related
- See `risks/security-risks.md` for the threat catalog
- See `checklists/p5-construction.md` for secure coding checks
