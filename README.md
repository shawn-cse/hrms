# HRMS

A production-oriented Human Resource Management System built with Django, PostgreSQL, Redis, Gunicorn, Nginx, and Docker Compose.

## Features

- Employee management
- Recruitment and onboarding
- Attendance and time tracking
- Leave management
- Payroll management
- Performance management
- Asset management
- Project management
- Helpdesk
- Offboarding
- REST API
- Reports and dashboards
- Role and permission management
- Audit logging
- Backup and automation tools
- LDAP integration
- Document management
- Theme support
- Biometric, geofencing, face-detection, and meeting-related integrations

## Technology Stack

- Python 3.12
- Django 5.x
- PostgreSQL 16
- Redis 7
- Gunicorn
- Nginx
- Docker
- Docker Compose

## Project Identity

- Application name: `HRMS`
- Django project package: `hrms`
- Default PostgreSQL database: `hrms_db`
- Default PostgreSQL user: `hrms_user`
- Default primary color: `#2563EB`
- Default timezone template: `Asia/Dhaka`

## Requirements

Recommended deployment method:

- Docker Engine
- Docker Compose v2.24+

For manual local development:

- Python 3.12
- PostgreSQL
- Redis

## Quick Start with Docker

From the project root:

```bash
docker compose up --build
```

The application will be available at:

```text
http://localhost:8000
```

Check container status:

```bash
docker compose ps
```

View application logs:

```bash
docker compose logs -f web
```

Run the Django system check:

```bash
docker compose exec web python manage.py check
```

Check migrations:

```bash
docker compose exec web python manage.py showmigrations
```

## Makefile Commands

The repository includes common development and deployment commands.

```bash
make help
make dev
make build
make status
make logs
make logs-web
make shell
make db-shell
make restart
make stop
```

`make clean` removes Docker volumes and permanently deletes the local Docker database and Redis data.

## Production Configuration

Create the production environment file:

```bash
cp .env.dist .env
```

Edit `.env` before deployment.

At minimum, configure strong values for:

```env
SECRET_KEY=
ALLOWED_HOSTS=
CSRF_TRUSTED_ORIGINS=
POSTGRES_PASSWORD=
DATABASE_URL=
DB_INIT_PASSWORD=
REDIS_PASSWORD=
REDIS_URL=
```

Do not use the development passwords in production.

Example production hostname configuration:

```env
ALLOWED_HOSTS=hrms.example.com
CSRF_TRUSTED_ORIGINS=https://hrms.example.com
```

## Production Deployment

Start the production stack:

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d
```

Or use:

```bash
make prod
```

Check services:

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml ps
```

Check application health:

```bash
curl -f http://localhost:8000/health/
```

Check readiness:

```bash
curl -f http://localhost:8000/ready/
```

## Database

The default Docker development database configuration is:

```text
Database: hrms_db
User:     hrms_user
Host:     db
Port:     5432
```

For this HRMS distribution, initialize a fresh database when deploying the application for the first time.

Do not connect an existing database that was created using different Django application labels or model namespaces unless a dedicated and tested schema/data migration has been prepared first.

Open a PostgreSQL shell inside Docker:

```bash
make db-shell
```

## Django Management

Open the application container:

```bash
make shell
```

Common commands:

```bash
python manage.py check
python manage.py showmigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

## Testing and Validation

Run the Django validation checks:

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
```

Run the smoke test suite:

```bash
make test-smoke
```

Run unit tests:

```bash
make test-unit
```

Run coverage checks:

```bash
make test-cov
```

When dependencies are installed only inside Docker, execute Django commands inside the `web` container.

## Static and Media Files

Production static files are collected into the Docker `staticfiles` volume.

Media files are handled by the application and are not exposed directly through the Nginx static-file mapping.

## Branding

The default application branding is configured as:

- Product name: `HRMS`
- Primary color: `#2563EB`
- HRMS logos and favicons under the project static assets

Company-specific branding can be applied by replacing the HRMS logo/favicon assets and updating the configured theme values while preserving the expected filenames and paths used by templates.

## Security Checklist

Before production deployment:

- Set `DEBUG=False`
- Use a long random `SECRET_KEY`
- Use strong PostgreSQL and Redis passwords
- Configure the exact production hostname
- Configure HTTPS
- Keep `SECURE_SSL_REDIRECT=1` when HTTPS termination is correctly configured
- Restrict database and Redis access to the internal Docker network
- Back up PostgreSQL and uploaded media regularly
- Review administrator accounts and permissions
- Run `python manage.py check --deploy` in the production configuration

## Backup

Example PostgreSQL backup:

```bash
docker compose exec -T db pg_dump -U hrms_user hrms_db > hrms_backup.sql
```

Example restore into a fresh database:

```bash
cat hrms_backup.sql | docker compose exec -T db psql -U hrms_user -d hrms_db
```

Test backup and restore procedures before relying on them in production.

## Useful Paths

```text
manage.py                  Django management entry point
hrms/                      Main Django project package
docker-compose.yml         Development/default Docker stack
docker-compose.prod.yml    Production Docker overlay
.env.dist                  Environment configuration template
Dockerfile                 Application container definition
docker/                    Docker and Nginx configuration
static/                    Static assets
templates/                 Shared templates
media/                     Application-uploaded media when used locally
```
