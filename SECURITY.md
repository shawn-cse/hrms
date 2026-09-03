# Security Policy

## Supported version

The deployed HRMS version should track the current maintained branch of this repository.

## Reporting vulnerabilities

Do not publish credentials, tokens, personal data, or exploit details in a public issue. Use the repository host's private security-advisory channel or the organization's internal security process.

## Deployment requirements

- Keep `DEBUG=False` in production.
- Use unique strong values for Django, PostgreSQL, Redis, and database-initialization secrets.
- Restrict `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`.
- Terminate TLS at the reverse proxy/load balancer.
- Back up PostgreSQL and uploaded media.
- Apply dependency and container security updates.
