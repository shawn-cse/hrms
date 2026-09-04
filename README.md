# HRMS

A Docker-first **Human Resource Management System** built with Django, PostgreSQL, Redis, Gunicorn, and Nginx.

Repository: https://github.com/shawn-cse/hrms

## Overview

HRMS provides a centralized platform for common human-resource workflows, including employee records, recruitment, onboarding, attendance, leave, payroll, performance, assets, projects, helpdesk, offboarding, reporting, and related administrative tools.

The recommended way to run this repository is with Docker Compose so that the application, PostgreSQL, and Redis use the same reproducible environment on Windows, Linux, and macOS.

## Documentation & Operational Guides

Complete system architecture and operational documentation is available in the [`docs/`](docs/) directory:

- 🌐 **[Interactive HTML Documentation (Complete System Guide)](docs/HRMS_COMPLETE_SYSTEM_DOCUMENTATION.html)** — Modern, searchable, dark/light interactive web manual covering all 24 modules, data models, approval workflows, REST API catalog, and DevOps setup.
- 📄 **[Complete System Markdown Documentation](docs/HRMS_COMPLETE_SYSTEM_DOCUMENTATION.md)** — Exhaustive 24-chapter technical specification and architectural blueprint.
- 📑 **[Executive PDF Documentation](docs/HRMS_Complete_System_Documentation.pdf)** — Formatted printable executive report.

### Default Login Credentials (Demo Environment)

| Role | Username / Email | Password | Access Level |
|---|---|---|---|
| **System Administrator** | `admin` | `admin` | Full superuser access across all companies and modules |
| **HR Manager** | `tanvir.rahman@example.com` | `admin` | HR lifecycle, employee profiles, department policies |
| **Project Manager** | `shakib.khan@example.com` | `admin` | Projects, tasks, timesheet approvals |
| **Standard Employee** | `afif.dutta@example.com` | `admin` | Employee self-service (Check-in/out, leave requests, payslips) |

## Main Features

- Employee management
- Company, department, job-position, and work-information management
- Recruitment and onboarding
- Attendance and time tracking
- Leave management
- Payroll
- Performance management
- Asset management
- Project and task management
- Helpdesk
- Offboarding
- Reports and dashboards
- Role and permission management
- REST API
- Notifications and automation
- Audit and backup utilities
- LDAP integration
- Document management
- Theme support
- WhatsApp-related integration
- Optional biometric, geofencing, face-detection, and meeting integrations

## Technology Stack

- **Backend:** Python 3.12, Django 5.x
- **Database:** PostgreSQL 16
- **Cache / messaging support:** Redis 7
- **Application server:** Gunicorn
- **Reverse proxy:** Nginx
- **Containerization:** Docker + Docker Compose
- **CI:** GitHub Actions

## Project Structure

Important top-level areas include:

```text
hrms/                    Django project package
employee/                Employee management
attendance/              Attendance
leave/                   Leave management
payroll/                 Payroll
recruitment/             Recruitment
onboarding/              Onboarding
offboarding/             Offboarding
asset/                   Asset management
project/                 Project management
helpdesk/                Helpdesk
pms/                     Performance management
report/                  Reporting
hrms_api/                API
hrms_auth/               Authentication
hrms_audit/              Audit functionality
hrms_automations/        Automation functionality
hrms_backup/             Backup functionality
hrms_documents/          Document functionality
hrms_ldap/               LDAP functionality
hrms_theme/              Theme / branding
whatsapp/                WhatsApp-related functionality
static/                  Static assets
templates/               Shared templates
docker/                  Docker / Nginx support files
.github/workflows/       GitHub Actions workflows
```

## Requirements

### Recommended

- Git
- Docker Desktop on Windows/macOS, or Docker Engine on Linux
- Docker Compose v2

> On Windows, Docker Desktop must be running in the background before starting the project.

## Quick Start

Clone the repository:

```bash
git clone https://github.com/shawn-cse/hrms.git
cd hrms
```

Build and start the development stack:

```bash
docker compose up -d --build
```

Check service status:

```bash
docker compose ps
```

Wait until the `db`, `redis`, and `web` services are running and the `web` service becomes healthy.

Then open:

```text
http://127.0.0.1:8080
```

`127.0.0.1` is recommended on Windows because some systems resolve `localhost` to IPv6 (`::1`), which may not work with the local Docker port binding.

## First-Time Setup

On a fresh database, HRMS opens the database-initialization/setup flow.

You can either:

1. configure a new workspace/company manually, or
2. load the demo database for testing.

The initialization password comes from the `DB_INIT_PASSWORD` environment variable configured for the running environment.

Do not expose or reuse the development initialization password in production.

After initialization, create or use an administrator account and continue with:

- Company
- Department
- Job Position
- Employee
- Work Information
- Roles and permissions

## Demo Data

If you choose **Load Demo Database**, the setup process may take several minutes because it creates database records and assigns demo roles.

Monitor the application if necessary:

```bash
docker compose logs -f web
```

Stop following logs with `Ctrl+C`. This does **not** stop the container.

## Login

Administrators and employees use the same HRMS authentication system.

Open:

```text
http://127.0.0.1:8080
```

Employee credentials must correspond to an active user/employee record.

For local testing, an administrator can reset a user's password from the container:

```bash
docker compose exec web python manage.py changepassword <username>
```

Example:

```bash
docker compose exec web python manage.py changepassword user@example.com
```

Do not document real employee passwords in this repository.

## Start and Stop

### Stop HRMS without deleting data

```bash
docker compose down
```

### Start it again later

Make sure Docker is running, then:

```bash
docker compose up -d
```

Open:

```text
http://127.0.0.1:8080
```

### Check status

```bash
docker compose ps
```

## After Changing Code

The development Compose configuration bind-mounts the project into the `web` container.

For normal Python/template/static source changes, restart the web service:

```bash
docker compose restart web
```

If you changed dependencies, the Dockerfile, system packages, or container startup configuration, rebuild:

```bash
docker compose up -d --build
```

For a completely clean image rebuild:

```bash
docker compose build --no-cache web
docker compose up -d
```

## Database

The Docker development database uses:

```text
Database: hrms_db
User:     hrms_user
Host:     db
Port:     5432
```

PostgreSQL data is stored in the named Docker volume:

```text
hrms-app_postgres_data
```

### Reset the Database

**Warning: this permanently deletes all local PostgreSQL data for this HRMS Docker project.**

```bash
docker compose down && docker volume rm hrms-app_postgres_data && docker compose up -d
```

After the new database is created, open:

```text
http://127.0.0.1:8080
```

The first-time setup flow should appear again.

Do not use `docker compose down -v` unless you intentionally want to remove all Compose-managed named volumes, not only PostgreSQL data.

## Useful Docker Commands

```bash
# Start
docker compose up -d

# Start and rebuild
docker compose up -d --build

# Status
docker compose ps

# Web logs
docker compose logs --tail=200 web

# Follow web logs
docker compose logs -f web

# Django checks
docker compose exec web python manage.py check

# Show migrations
docker compose exec web python manage.py showmigrations

# Apply migrations
docker compose exec web python manage.py migrate

# Create a superuser
docker compose exec web python manage.py createsuperuser

# Open Django shell
docker compose exec web python manage.py shell

# Stop without deleting data
docker compose down
```

## Health Checks

The application exposes health endpoints used by Docker and CI.

Inside the container, the web service listens on port `8000`.

The development host mapping is:

```text
127.0.0.1:8080 -> container:8000
```

Check Docker status:

```bash
docker compose ps
```

A healthy local stack should show the database, Redis, and web services running successfully.

## Troubleshooting

### `localhost refused to connect`

Use:

```text
http://127.0.0.1:8080
```

Then verify:

```bash
docker compose ps
```

### Web container is `health: starting`

Wait for migrations, static-file collection, and Gunicorn startup to finish, then run:

```bash
docker compose ps
```

### Web container is unhealthy or restarting

Inspect logs:

```bash
docker compose logs --tail=200 web
```

### Port 8080 is already in use

Stop the process using the port or change the host side of the Compose port mapping.

For example:

```yaml
ports:
  - "8081:8000"
```

Then open:

```text
http://127.0.0.1:8081
```

### Database volume cannot be removed

A volume cannot be removed while a container is using it.

Stop the stack first:

```bash
docker compose down
```

Then remove the PostgreSQL volume:

```bash
docker volume rm hrms-app_postgres_data
```

## Development Without Docker

Docker is the supported and recommended setup for this repository.

A native setup is possible, but you must install and configure Python 3.12, PostgreSQL, Redis, system libraries, environment variables, migrations, and static assets yourself. Because native dependencies vary by operating system, use Docker unless you specifically need a non-container development environment.

## Production

The development Compose configuration contains local-development settings and must not be used unchanged on a public server.

Before production deployment:

- set `DEBUG=0`
- use a strong unique `SECRET_KEY`
- use strong PostgreSQL and Redis credentials
- use a strong `DB_INIT_PASSWORD`
- configure `ALLOWED_HOSTS`
- configure `CSRF_TRUSTED_ORIGINS`
- use HTTPS
- protect database and media backups
- do not commit `.env` or real secrets
- review reverse-proxy and firewall configuration
- run migrations and health checks before routing production traffic

If the repository includes `docker-compose.prod.yml`, create a production `.env` based on the provided environment template and run the production overlay only after all secrets and hostnames have been configured.

## Tests and CI

The repository contains GitHub Actions workflows for automated quality, unit/smoke, and Docker checks.

Useful local checks include:

```bash
docker compose exec web python manage.py check
docker compose exec web python manage.py makemigrations --check --dry-run
```

Run the test suite appropriate to the change before opening a pull request.

A failing GitHub Actions check does not prevent Git from cloning the repository, but CI failures should be investigated before treating a release as verified.

## Security

Never commit:

- `.env`
- passwords
- API tokens
- private keys
- database dumps containing personal data
- production secrets
- employee personal data exported from a live system

See [SECURITY.md](SECURITY.md) for vulnerability-reporting and deployment guidance.

## Contributing

Contributions should follow [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Branding

Current project identity:

```text
Product name: HRMS
Django package: hrms
Primary color: #2563EB
```

## Licensing and Attribution

This repository is derived from open-source software. Before redistribution or production use, review and comply with all applicable upstream licensing, copyright, attribution, and source-distribution obligations.

Removing a license or notice file from a working tree does not by itself remove obligations that apply to code obtained under an open-source license.
