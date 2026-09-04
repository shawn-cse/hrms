# -*- coding: utf-8 -*-
"""
Master HRMS Documentation & PDF Generator
Generates comprehensive Markdown, Print-Optimized HTML, and compiles an Executive PDF.
"""

import os
import sys
import subprocess
import datetime
import html

BASE_DIR = r"d:\2026__LO\Coding\hrms"
DOCS_DIR = os.path.join(BASE_DIR, "docs")
os.makedirs(DOCS_DIR, exist_ok=True)

MD_PATH = os.path.join(DOCS_DIR, "HRMS_COMPLETE_SYSTEM_DOCUMENTATION.md")
HTML_PATH = os.path.join(DOCS_DIR, "HRMS_Documentation_Print.html")
PDF_PATH = os.path.join(DOCS_DIR, "HRMS_Complete_System_Documentation.pdf")

print("Building Chapter Contents...")

CHAPTERS = []

# ==============================================================================
# CHAPTER 1: SYSTEM OVERVIEW & ARCHITECTURE
# ==============================================================================
CHAPTERS.append({
    "num": 1,
    "id": "system-overview",
    "title": "System Overview & Architectural Blueprint",
    "subtitle": "High-level architecture, technology stack, directory structure, and modular design patterns.",
    "content_md": """
## 1.1 Executive Summary

HRMS is an enterprise-grade, Docker-first Human Resource Management System built on Python 3.12, Django 5.x, PostgreSQL 16, Redis 7, Gunicorn, and Nginx. The system provides an end-to-end digital workplace platform governing every stage of the human capital lifecycle—from talent requisition, applicant tracking, and onboarding, to daily attendance, biometric synchronization, multi-tier leave workflows, automated payroll execution, performance appraisals (PMS), asset custody, project task tracking, internal helpdesk support, dynamic document generation, and formal offboarding clearance.

Designed around principles of modularity, data security, and multi-tenant organizational hierarchy, HRMS features fine-grained Role-Based Access Control (RBAC), multi-company isolation, two-factor authentication (2FA), continuous audit logging, event-driven email automations, scheduled background tasks, and a full-featured REST API with interactive Swagger/OpenAPI documentation.

---

## 1.2 Technology Stack

| Layer | Technology | Version | Key Responsibilities |
|---|---|---|---|
| **Core Framework** | Django / Python | 5.x / 3.12+ | Web application framework, ORM, security middleware, authentication |
| **Primary Database** | PostgreSQL | 16.x | Relational database, ACID transactions, relational integrity, JSONB fields |
| **Cache & In-Memory** | Redis | 7.x | Session caching, application state, rate-limiting, message broker |
| **Application Server** | Gunicorn | 21.x+ | Production WSGI HTTP server with multi-worker concurrent request execution |
| **Reverse Proxy / SSL** | Nginx | Stable / Alpine | Reverse proxy, static asset caching, SSL/TLS termination, request buffering |
| **Background Scheduler** | Django APScheduler | 0.3.0+ | Cron tasks, automated payroll runs, daily attendance summaries, email queues |
| **REST API Engine** | Django REST Framework (DRF) | 3.14+ | RESTful API endpoints, SimpleJWT authentication, Swagger UI (`drf_yasg`) |
| **Audit & History** | Django Auditlog / Simple History | Current | Comprehensive changelog tracking, user action audits, field-level diffs |
| **Containerization** | Docker & Docker Compose | v2+ | Multi-stage container builds, reproducible development and production stacks |
| **Continuous Integration** | GitHub Actions | Standard | Automated linting, test validation, security checks, Docker packaging |

---

## 1.3 Architectural Design Patterns

### 1. Pluggable Dynamic App Discovery
HRMS implements a modular, pluggable application architecture. Rather than hardcoding dozens of URL includes inside the central `hrms/urls.py`, individual domain apps register their own routing and metadata dynamically via the Django `AppConfig.ready()` lifecycle hook:

```python
# Example from leave/apps.py
class LeaveConfig(AppConfig):
    name = "leave"

    def ready(self):
        from django.urls import include, path
        from hrms.urls import urlpatterns
        
        settings.APPS.append("leave")
        urlpatterns.append(
            path("leave/", include("leave.urls")),
        )
        super().ready()
```

This pattern ensures that modules can be cleanly activated, deactivated, or decoupled for white-label or customer-specific deployments without modifying the core project engine.

### 2. Multi-Company Organizational Hierarchy
At the foundation of the data architecture lies the `base.Company` model. Organizational components (Departments, Job Positions, Work Types, Shifts, and Policies) and operational records (Employees, Attendances, Leave Requests, and Payslips) are mapped either directly or transitively to a Company entity. Custom middleware (`base.middleware.CompanyMiddleware`) resolves the active company context from the user's session or request headers, ensuring strict data isolation across multi-entity corporations.

### 3. Unified Request-and-Approve Engine
Workflows requiring managerial oversight—including Leave Requests, Attendance Regularizations, Shift Changes, Work Type Modifications, Reimbursements, and Asset Requests—route through a standardized `MultipleApprovalCondition` engine. Organizations can construct complex approval hierarchies (e.g., Immediate Supervisor -> Department Head -> HR Manager -> Finance Director) with custom conditions based on duration, expense value, or organizational rank.

---

## 1.4 Directory Layout

The repository is structured into modular domain packages, operational directories, and container configurations:

```text
d:\\2026__LO\\Coding\\hrms\\
├── hrms/                 # Core Django project configuration, settings, base URLs, WSGI/ASGI
├── base/                 # Master organizational hierarchy, shifts, work types, companies, ESS
├── employee/             # Employee profiles, bank info, emergency contacts, policies, notes
├── attendance/           # Clock in/out, late/early calculation, overtime, work records
├── biometric/            # Hardware integration (ZKTeco, Matrix COSEC, biometric devices)
├── facedetection/        # Facial recognition attendance capture and verification
├── geofencing/           # GPS location geofencing boundaries and perimeter validation
├── leave/                # Leave types, accrual rules, requests, multi-tier approvals, holidays
├── payroll/              # Salary contracts, allowances, deductions, tax slabs, batch payslips
├── pms/                  # Performance Management System: OKRs, KPIs, 360 feedback, reviews
├── asset/                # Hardware/software inventory, asset allocation, return condition photos
├── recruitment/          # Requisitions, pipeline stages, resume parsing, interview scoring
├── onboarding/           # Pre-boarding portal, document collection, departmental checklists
├── offboarding/          # Resignations, clearance workflows (IT, HR, Finance), exit interviews
├── project/              # Projects, milestones, Kanban task boards, billable timesheets
├── helpdesk/             # Internal support ticketing, category routing, SLA tracking, FAQs
├── report/               # BI reporting engine, custom filters, scheduled exports (CSV/Excel/PDF)
├── hrms_api/             # RESTful APIs, SimpleJWT auth, Swagger OpenAPI documentation
├── hrms_auth/            # Custom HRMSUser model, authentication backends, permission groups
├── hrms_audit/           # Audit trail logging, field diff tracking, account lock/unlock history
├── hrms_automations/     # Event triggers, scheduled cron jobs, automated mail actions
├── notifications/        # In-app notification drawer, broadcast announcements, email dispatches
├── hrms_documents/       # Dynamic document generation, certificate requests, PDF outputs
├── hrms_dbtemplate/      # Database-driven rich text templates with dynamic merge tags
├── hrms_backup/          # PostgreSQL automated backups, local archives, Google Drive sync
├── hrms_ldap/            # Enterprise Active Directory / OpenLDAP directory synchronization
├── hrms_meet/            # Google Meet video conference room integration for interviews
├── hrms_theme/           # Dynamic white-label CSS theme engine and branding customizer
├── hrms_tour/            # Interactive guided UI product tours (tourController.js)
├── hrms_views/           # Dynamic view filters, saved queries, toggleable table columns
├── hrms_widgets/         # Dashboard widget framework and metrics visualizers
├── whatsapp/             # Meta WhatsApp Business API integration for alerts and messaging
├── dynamic_fields/       # Runtime custom fields on models without database migrations
├── accessibility/        # WCAG compliance features: high contrast, dyslexic font, text resizing
├── static/               # Source static assets (JavaScript, CSS, vendor libraries, icons)
├── staticfiles/          # Collected static files for production deployment via WhiteNoise/Nginx
├── templates/            # Global HTML templates, authentication views, base master layouts
├── docker/               # Dockerfile, Nginx configurations, container entrypoint scripts
└── docs/                 # System documentation, HTML print assets, generated executive PDF
```
""",
    "content_html": """
<div class="chapter-content">
  <div class="callout callout-info">
    <h4>Executive Overview</h4>
    <p>HRMS is a full-featured, enterprise-ready Human Resource Management System engineered on Django 5.x and PostgreSQL 16. It automates the entire employee lifecycle across 30+ specialized applications, ensuring compliance, operational efficiency, and real-time organizational transparency.</p>
  </div>

  <h3>High-Level Architectural Blueprint</h3>
  <div class="arch-diagram">
    <div class="arch-col">
      <div class="arch-box box-primary">
        <strong>Client Presentation Layer</strong>
        <span>Responsive Web UI (Vanilla CSS + HTMX)</span>
        <span>Interactive Dashboards & ESS Portals</span>
        <span>Accessibility & Theme Engine (WCAG)</span>
        <span>Guided Interactive Product Tours</span>
      </div>
    </div>
    <div class="arch-arrow">➔</div>
    <div class="arch-col">
      <div class="arch-box box-accent">
        <strong>Security & API Gateway Layer</strong>
        <span>Nginx Reverse Proxy + WhiteNoise Cache</span>
        <span>JWT Bearer Auth & Django Session Gate</span>
        <span>2FA TOTP Verification Middleware</span>
        <span>SVG Sanitizer & XSS Security Middlewares</span>
        <span>DRF REST API & Interactive Swagger UI</span>
      </div>
    </div>
    <div class="arch-arrow">➔</div>
    <div class="arch-col">
      <div class="arch-box box-dark">
        <strong>Domain Application Services</strong>
        <span>Core Base & Multi-Company Tenancy</span>
        <span>Employee, Onboarding & Offboarding</span>
        <span>Attendance, Biometrics & Geofencing</span>
        <span>Leave & Multi-Tier Approval Chain</span>
        <span>Payroll Engine, Tax Brackets & Payslips</span>
        <span>PMS, OKRs, 360 Feedback & Assets</span>
      </div>
    </div>
    <div class="arch-arrow">➔</div>
    <div class="arch-col">
      <div class="arch-box box-success">
        <strong>Persistence & Background Tier</strong>
        <span>PostgreSQL 16 Relational Storage</span>
        <span>Redis 7 In-Memory Cache & Broker</span>
        <span>Django APScheduler Background Cron</span>
        <span>Automated Backups & Cloud Sync</span>
      </div>
    </div>
  </div>

  <h3>Global Technology Stack Specifications</h3>
  <table class="data-table">
    <thead>
      <tr><th>Component</th><th>Technology</th><th>Version</th><th>Functionality</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>Backend Framework</strong></td><td>Django / Python</td><td>5.x / 3.12+</td><td>Application logic, ORM, authentication, admin engine</td></tr>
      <tr><td><strong>Database</strong></td><td>PostgreSQL</td><td>16.x</td><td>ACID relational data, transactional reliability, JSONB</td></tr>
      <tr><td><strong>In-Memory Cache</strong></td><td>Redis</td><td>7.x</td><td>Session store, performance caching, rate-limiting</td></tr>
      <tr><td><strong>App Server</strong></td><td>Gunicorn</td><td>21.x</td><td>WSGI server with multiple pre-forked worker processes</td></tr>
      <tr><td><strong>Web Proxy</strong></td><td>Nginx</td><td>Alpine</td><td>Reverse proxy, TLS termination, static asset buffering</td></tr>
      <tr><td><strong>Background Worker</strong></td><td>APScheduler</td><td>0.3.0+</td><td>Scheduled jobs, automated payslips, attendance aggregation</td></tr>
      <tr><td><strong>REST API</strong></td><td>Django REST Framework</td><td>3.14+</td><td>RESTful endpoints, SimpleJWT bearer tokens, Swagger UI</td></tr>
      <tr><td><strong>Audit Engine</strong></td><td>Django Auditlog</td><td>Current</td><td>Complete entity history, audit diffs, change tracking</td></tr>
      <tr><td><strong>Containerization</strong></td><td>Docker Compose</td><td>v2+</td><td>Reproducible multi-container orchestration</td></tr>
    </tbody>
  </table>
</div>
"""
})

# ==============================================================================
# CHAPTER 2: BASE & CORE FOUNDATION
# ==============================================================================
CHAPTERS.append({
    "num": 2,
    "id": "base-core-foundation",
    "title": "Core Architecture, Multi-Tenancy & Base Configuration (`base`)",
    "subtitle": "Organizational structure, multi-company hierarchy, shifts, work types, approval chains, and system middlewares.",
    "content_md": """
## 2.1 Overview & Responsibilities

The `base` application represents the architectural spine of the HRMS platform. It houses the foundational data models and services that dictate company structure, organizational hierarchies, operational working shifts, rotating schedules, holiday calendars, public announcements, and the unified request-and-approval engine.

In addition to core organizational data, `base` implements mission-critical system middlewares enforcing tenant scoping, password rotation, two-factor authentication, and HTTP request sanitization.

---

## 2.2 Database Models Specification

The `base` module defines over 45 relational models governing corporate operations:

| Model Name | Purpose | Primary Attributes & Relationships |
|---|---|---|
| `Company` | Root multi-tenancy entity representing legal corporate bodies. | `company_name`, `registration_number`, `email`, `phone`, `website`, `address`, `country`, `currency`, `logo`, `timezone`, `is_active` |
| `CompanyGroupAssignment` | Assigns security permission groups and roles on a per-company basis. | `company` (FK), `group` (FK to auth.Group), `assigned_by` |
| `Department` | Functional divisions within a company. | `department_name`, `company` (FK), `department_manager` (FK to Employee), `parent_department` (self-referential FK for sub-departments) |
| `JobPosition` | Standardized job titles and organizational roles. | `job_position_name`, `department` (FK), `company` (FK), `job_description`, `maximum_headcount` |
| `JobRole` | Granular responsibilities, duties, and qualifications tied to job positions. | `job_role_name`, `job_position` (FK), `responsibilities`, `qualifications` |
| `WorkType` | Core work arrangements (e.g. Regular Office, Remote, Hybrid, Flexi). | `work_type_name`, `company` (FK), `is_remote`, `requires_approval` |
| `RotatingWorkType` | Multi-week rotating work arrangements (e.g. 2 weeks on-site, 1 week remote). | `name`, `company` (FK), `cycle_frequency_days`, `is_active` |
| `RotatingWorkTypeAssign` | Assignment of rotating work schedules to individual employees. | `employee` (FK), `rotating_work_type` (FK), `start_date`, `end_date` |
| `EmployeeType` | Employment classifications (e.g. Permanent, Probationary, Contract, Intern). | `employee_type_name`, `company` (FK), `benefits_eligible` |
| `EmployeeShift` | Standard operational work timings for employees. | `shift_name`, `company` (FK), `start_time`, `end_time`, `grace_time_minutes`, `break_duration_minutes`, `working_days` |
| `EmployeeShiftSchedule` | Daily schedule exceptions and specific shift assignments per date. | `employee` (FK), `shift` (FK), `schedule_date`, `notes` |
| `RotatingShift` | Recurring rotational shift patterns (e.g. Morning -> Evening -> Night). | `name`, `company` (FK), `rotation_frequency_days`, `shifts` (M2M) |
| `RotatingShiftAssign` | Links an employee to an automated recurring shift rotation. | `employee` (FK), `rotating_shift` (FK), `effective_from`, `active` |
| `Roster` | Master published weekly/monthly duty roster for staff allocations. | `employee` (FK), `shift` (FK), `date`, `published_by`, `status` |
| `RosterPublishLog` | Audit log tracking when rosters are published and notices dispatched. | `roster` (FK), `published_at`, `published_by`, `recipients_count` |
| `WorkTypeRequest` | Employee self-service request to alter work type arrangement. | `employee` (FK), `requested_work_type` (FK), `start_date`, `end_date`, `reason`, `status` |
| `ShiftRequest` | Employee self-service request for temporary shift swap or change. | `employee` (FK), `requested_shift` (FK), `effective_date`, `reason`, `status` |
| `MultipleApprovalCondition`| Configurable approval chains based on roles, departments, or limits. | `workflow_type`, `step_number`, `approver_role`, `approver_user` (FK), `is_mandatory` |
| `Holidays` | Official calendar of national, regional, and company holidays. | `holiday_name`, `holiday_date`, `company` (FK), `is_recurring`, `description` |
| `CompanyLeaves` | Mandatory company shutdown periods or seasonal collective leaves. | `name`, `start_date`, `end_date`, `company` (FK), `deduct_from_leave_balance` |
| `HRMSMailTemplate` | Reusable email notification templates with dynamic placeholder variables. | `title`, `subject`, `body_html`, `mail_type`, `available_variables` |
| `MailLog` | Historical transmission log of all outbound emails dispatched by the system. | `template` (FK), `recipient_email`, `subject`, `sent_at`, `delivery_status`, `error_message` |
| `Penalty` | Disciplinary penalty rules for chronic late arrivals or unauthorized absence. | `penalty_name`, `violation_threshold_count`, `action_type`, `deduction_amount` |

---

## 2.3 Core Middlewares & System Interceptors

HRMS enforces critical security, tenant isolation, and session integrity policies via custom Django middlewares defined in `base.middleware` and `hrms.hrms_middlewares`:

1. **`CompanyMiddleware`**: Intercepts every incoming HTTP request. Identifies the authenticated user's assigned company context or reads the explicit company header (`X-Company-ID`). Attaches `request.company` and activates database filtering to isolate tenant data.
2. **`ForcePasswordChangeMiddleware`**: Inspects user profile state upon successful authentication. If `user.force_password_change` is set (such as following account provisioning or admin reset), the user is forcibly redirected to the password reset view, blocking all other endpoints until a secure password is established.
3. **`TwoFactorAuthMiddleware`**: Enforces Time-Based One-Time Password (TOTP) verification for privileged user tiers (System Administrators, HR Directors, Payroll Managers) before allowing access to administrative or financial views.
4. **`SVGSecurityMiddleware`**: Inspects all file uploads containing SVG images. Parses and sanitizes XML payloads to neutralize embedded `<script>`, `onload`, or malicious SVG-based Cross-Site Scripting (XSS) vectors.
5. **`DefaultLanguageMiddleware`**: Detects user-selected language preferences from cookies or browser accept headers and activates Django's `i18n` locale context.
6. **`MethodNotAllowedMiddleware` & `MissingParameterMiddleware`**: Intercepts ill-formed requests or unsupported HTTP verbs, transforming raw Django exceptions into standardized JSON responses with error codes.

---

## 2.4 User Interfaces & Dashboards

The `base` module provides several specialized UI layouts:
- **Unified Main Dashboard (`/dashboard/`)**: Executive overview presenting KPI metrics: Total Active Headcount, Today's Attendance Rate, Leave Breakdown Donut Chart, Department Distribution Bar Chart, Gender Split, and Company Announcements.
- **Employee Self-Service (ESS) Dashboard (`/ess/`)**: Employee-centric portal showing live check-in status, remaining leave balances, upcoming holidays, shift schedules, assigned tasks, and quick-action buttons to request leave or regularize attendance.
- **Request & Approval Central**: Centralized queue where managers review, approve, or reject pending requests across Leave, Attendance, Shifts, Assets, and Expenses with audit notes.
""",
    "content_html": """
<div class="chapter-content">
  <p>The <code>base</code> module is the bedrock of HRMS, orchestrating multi-tenant companies, organizational units, working schedules, dynamic approval chains, and security middlewares.</p>

  <h3>Core Relational Models</h3>
  <table class="data-table">
    <thead>
      <tr><th>Model</th><th>Category</th><th>Key Fields</th><th>Description</th></tr>
    </thead>
    <tbody>
      <tr><td><code>Company</code></td><td>Tenant</td><td><code>company_name</code>, <code>registration_number</code>, <code>currency</code>, <code>timezone</code></td><td>Root multi-tenancy entity for legal entities.</td></tr>
      <tr><td><code>Department</code></td><td>Hierarchy</td><td><code>department_name</code>, <code>department_manager</code>, <code>parent_department</code></td><td>Organizational division with recursive nesting.</td></tr>
      <tr><td><code>JobPosition</code></td><td>Hierarchy</td><td><code>job_position_name</code>, <code>department</code>, <code>maximum_headcount</code></td><td>Official job designation within departments.</td></tr>
      <tr><td><code>EmployeeShift</code></td><td>Schedule</td><td><code>start_time</code>, <code>end_time</code>, <code>grace_time_minutes</code>, <code>working_days</code></td><td>Operational shift timing and grace tolerances.</td></tr>
      <tr><td><code>RotatingShift</code></td><td>Schedule</td><td><code>name</code>, <code>rotation_frequency_days</code>, <code>shifts</code></td><td>Automated multi-week recurring shift rotation.</td></tr>
      <tr><td><code>Roster</code></td><td>Schedule</td><td><code>employee</code>, <code>shift</code>, <code>date</code>, <code>published_by</code></td><td>Published duty assignments per employee per date.</td></tr>
      <tr><td><code>WorkType</code></td><td>Policy</td><td><code>work_type_name</code>, <code>is_remote</code>, <code>requires_approval</code></td><td>Work arrangements (On-site, Remote, Hybrid).</td></tr>
      <tr><td><code>MultipleApprovalCondition</code></td><td>Workflow</td><td><code>workflow_type</code>, <code>step_number</code>, <code>approver_role</code>, <code>is_mandatory</code></td><td>Configurable multi-tier hierarchical approval engine.</td></tr>
      <tr><td><code>Holidays</code></td><td>Calendar</td><td><code>holiday_name</code>, <code>holiday_date</code>, <code>is_recurring</code></td><td>Public and religious holiday dates.</td></tr>
      <tr><td><code>HRMSMailTemplate</code></td><td>System</td><td><code>title</code>, <code>subject</code>, <code>body_html</code>, <code>available_variables</code></td><td>Dynamic notification email templates with merge tags.</td></tr>
    </tbody>
  </table>

  <div class="callout callout-warning">
    <h4>Security & Enforcement Middlewares</h4>
    <ul>
      <li><strong>CompanyMiddleware:</strong> Automatic tenant-level data isolation based on authenticated session context.</li>
      <li><strong>ForcePasswordChangeMiddleware:</strong> Mandatory password updates upon initial provision or reset.</li>
      <li><strong>TwoFactorAuthMiddleware:</strong> Enforces TOTP 2FA for administrative and financial operations.</li>
      <li><strong>SVGSecurityMiddleware:</strong> Neutralizes XML/script injection attacks within SVG attachments.</li>
    </ul>
  </div>
</div>
"""
})

# ==============================================================================
# CHAPTER 3: EMPLOYEE LIFECYCLE MANAGEMENT
# ==============================================================================
CHAPTERS.append({
    "num": 3,
    "id": "employee-lifecycle",
    "title": "Employee Profile & Lifecycle Management (`employee`)",
    "subtitle": "Employee master records, statutory information, banking, emergency contacts, disciplinary tracking, and company policies.",
    "content_md": """
## 3.1 Overview & Responsibilities

The `employee` application manages the comprehensive digital profile of every staff member. It serves as the single source of truth for personal data, statutory identification, compensation structures, banking credentials, emergency contacts, academic qualifications, previous work history, company policies, and disciplinary proceedings.

---

## 3.2 Database Models Specification

| Model Name | Purpose | Primary Attributes & Relationships |
|---|---|---|
| `Employee` | Master employee profile linked 1:1 to the system `HRMSUser`. | `badge_id`, `first_name`, `last_name`, `email`, `phone`, `gender`, `dob`, `marital_status`, `nationality`, `blood_group`, `avatar`, `joining_date`, `is_active` |
| `EmployeeWorkInformation` | Employment details, contractual status, and reporting lines. | `employee` (1:1), `company` (FK), `department` (FK), `job_position` (FK), `job_role` (FK), `shift` (FK), `work_type` (FK), `reporting_manager` (FK), `probation_end_date` |
| `EmployeeBankDetails` | Payroll disbursement bank account details and statutory IDs. | `employee` (1:1), `bank_name`, `account_number`, `branch_name`, `ifsc_or_swift_code`, `pan_or_ssn_number`, `tax_id` |
| `EmployeeTag` | Metadata categorization tags for skills, projects, or committees. | `tag_name`, `color_code`, `company` (FK) |
| `EmployeeNote` | Confidential notes, HR interview logs, and performance remarks. | `employee` (FK), `author` (FK), `note_title`, `description`, `is_confidential`, `created_at` |
| `NoteFiles` | Document attachments associated with employee notes. | `note` (FK), `attachment_file`, `file_name`, `uploaded_at` |
| `Policy` | Corporate compliance policies, handbooks, and code of conduct. | `policy_title`, `company` (FK), `description`, `effective_date`, `mandatory_acknowledgement` |
| `PolicyMultipleFile` | PDF attachments and official documents linked to corporate policies. | `policy` (FK), `document_file`, `uploaded_at` |
| `BonusPoint` | Recognition and reward points granted by managers or peers. | `employee` (FK), `points`, `awarded_by` (FK), `reason`, `date_awarded` |
| `Actiontype` | Standardized disciplinary action categories (e.g. Warning, Suspension, Fine). | `action_name`, `severity_level`, `company` (FK) |
| `DisciplinaryAction` | Records of formal infractions, investigations, and penalties. | `employee` (FK), `action_type` (FK), `infraction_date`, `description`, `decision`, `penalty_deduction`, `status` |
| `ProfileEditFeature` | Fine-grained controls dictating which profile fields employees can edit. | `field_name`, `allow_employee_edit`, `requires_hr_approval` |
| `EmployeeGeneralSetting` | Global settings for employee auto-numbering, prefix, and defaults. | `employee_id_prefix`, `next_auto_number`, `require_photo_on_creation` |

---

## 3.3 Lifecycle Operations & Workflows

### 1. Employee Creation & Onboarding Handoff
When a candidate successfully finishes onboarding or an HR admin manually creates a staff record:
1. An `Employee` profile is generated, and a unique `badge_id` is assigned according to `EmployeeGeneralSetting`.
2. A corresponding `HRMSUser` authentication record is provisioned with a secure random password and temporary flag.
3. Reporting manager, shift timings, work types, and departments are configured in `EmployeeWorkInformation`.
4. Mandatory corporate policies (`Policy`) are automatically bound to the new employee, triggering an acknowledgement notification on their next login.

### 2. Disciplinary Action & Governance
When compliance violations or behavioral infractions occur:
1. HR initiates a `DisciplinaryAction` linking the employee and an `Actiontype`.
2. Documentation, witness statements, and formal warnings are attached.
3. If financial penalties or suspensions are levied, `penalty_deduction` communicates directly with the `payroll` module during the subsequent monthly pay cycle to apply structured wage deductions.

### 3. Employee Self-Service (ESS) Profile Management
Employees can review and update non-critical personal data (e.g. personal contact numbers, emergency contacts, residential address) directly from their ESS portal. The `ProfileEditFeature` model allows HR administrators to lock sensitive fields (e.g. Bank Account Number, Legal Name, Date of Birth, Job Title) so that modifications require formal HR ticket submission and verification.
""",
    "content_html": """
<div class="chapter-content">
  <p>The <code>employee</code> application governs the complete identity, employment context, banking credentials, compliance policies, and disciplinary history for the entire workforce.</p>

  <h3>Key Data Models</h3>
  <table class="data-table">
    <thead>
      <tr><th>Model</th><th>Relationship</th><th>Key Attributes</th><th>Description</th></tr>
    </thead>
    <tbody>
      <tr><td><code>Employee</code></td><td>1:1 to User</td><td><code>badge_id</code>, <code>email</code>, <code>phone</code>, <code>avatar</code>, <code>joining_date</code></td><td>Master demographic and personal record.</td></tr>
      <tr><td><code>EmployeeWorkInformation</code></td><td>1:1 to Employee</td><td><code>department</code>, <code>job_position</code>, <code>reporting_manager</code>, <code>shift</code></td><td>Contractual, structural, and reporting setup.</td></tr>
      <tr><td><code>EmployeeBankDetails</code></td><td>1:1 to Employee</td><td><code>bank_name</code>, <code>account_number</code>, <code>ifsc_or_swift_code</code>, <code>tax_id</code></td><td>Direct-deposit payroll information and tax IDs.</td></tr>
      <tr><td><code>Policy</code></td><td>Company FK</td><td><code>policy_title</code>, <code>effective_date</code>, <code>mandatory_acknowledgement</code></td><td>Corporate governance policies and handbooks.</td></tr>
      <tr><td><code>DisciplinaryAction</code></td><td>Employee FK</td><td><code>action_type</code>, <code>infraction_date</code>, <code>penalty_deduction</code>, <code>status</code></td><td>Formal infractions, warnings, and payroll penalties.</td></tr>
      <tr><td><code>ProfileEditFeature</code></td><td>System</td><td><code>field_name</code>, <code>allow_employee_edit</code>, <code>requires_hr_approval</code></td><td>Granular self-service profile modification permissions.</td></tr>
    </tbody>
  </table>

  <div class="callout callout-info">
    <h4>Integration Highlights</h4>
    <p>The Employee module connects directly into <strong>Payroll</strong> (bank details & salary contract), <strong>Attendance</strong> (badge ID & shift assignment), <strong>Onboarding</strong> (profile conversion), and <strong>PMS</strong> (manager evaluation chains).</p>
  </div>
</div>
"""
})

# Let's add remaining chapters: attendance, biometric/face/geo, leave, payroll, pms, asset, recruitment, onboarding, offboarding, project, helpdesk, report, hrms_api, auth/security, audit, automations/notifications, documents/templates, backup, integrations, ui/ux, devops.
# We will write detailed sections for each so that no feature is left out.

print("Chapters 1-3 built. Adding Chapters 4 to 24...")

# ==============================================================================
# CHAPTER 4: ATTENDANCE & TIME TRACKING ENGINE
# ==============================================================================
CHAPTERS.append({
    "num": 4,
    "id": "attendance-engine",
    "title": "Attendance & Time Tracking Engine (`attendance`)",
    "subtitle": "Clock in/out tracking, grace periods, overtime computation, late-in/early-out rules, and work records.",
    "content_md": """
## 4.1 Overview & Responsibilities

The `attendance` application records, computes, and audits employee working hours across physical offices, remote workstations, and field operations. It tracks precise timestamps, evaluates attendance against scheduled shift rules, calculates grace period tolerances, detects late arrivals and early departures, manages overtime approvals, and provides daily summary work records utilized directly by the payroll calculation engine.

---

## 4.2 Database Models Specification

| Model Name | Purpose | Primary Attributes & Relationships |
|---|---|---|
| `Attendance` | Primary daily attendance record per employee per calendar date. | `employee` (FK), `attendance_date`, `attendance_clock_in`, `attendance_clock_out`, `attendance_clock_in_date`, `attendance_clock_out_date`, `minimum_hour`, `at_work`, `attendance_worked_hour`, `is_validated` |
| `AttendanceActivity` | Raw punch logs capturing individual clock-in/out events and sources. | `employee` (FK), `attendance_date`, `time`, `clock_in`, `clock_out`, `device_id`, `ip_address`, `latitude`, `longitude` |
| `BatchAttendance` | Bulk attendance creation records for shifts, teams, or departments. | `batch_name`, `company` (FK), `department` (FK), `shift` (FK), `date`, `created_by` |
| `AttendanceOverTime` | Tracks verified overtime hours and managerial approval state. | `employee` (FK), `attendance` (FK), `month_sequence`, `overtime_hour`, `status` (Requested/Approved/Rejected), `approved_by` |
| `AttendanceLateComeEarlyOut` | Tracks minutes and frequency of late arrivals and early departures. | `employee` (FK), `attendance` (FK), `attendance_date`, `type` (Late Come / Early Out), `duration_minutes`, `reason`, `is_excused` |
| `AttendanceValidationCondition` | Logical threshold rules determining daily status (Present, Half Day, Absent). | `company` (FK), `minimum_hours_full_day`, `minimum_hours_half_day`, `auto_validate` |
| `GraceTime` | Configurable grace tolerance windows before late-arrival penalties trigger. | `company` (FK), `shift` (FK), `allowed_late_minutes`, `allowed_grace_frequency_per_month` |
| `AttendanceGeneralSetting` | Global operational rules for auto-clock-out, selfie capture, and IP locks. | `auto_clock_out_time`, `enable_ip_restriction`, `require_selfie_on_punch`, `enable_overtime_approval` |
| `WorkRecords` | Aggregated daily work units feeding directly into payroll processing. | `employee` (FK), `date`, `regular_hours`, `overtime_hours`, `loss_of_pay_units`, `salary_ready` |
| `AttendanceConflictResolution` | Resolution record for punch collisions, missing check-outs, or hardware drift. | `attendance` (FK), `conflict_type`, `original_value`, `corrected_value`, `resolved_by` |
| `AttendanceDailyHours` & `AttendanceSummaryHours` | Pre-aggregated caches of daily and monthly hours for instant dashboard reporting. | `employee` (FK), `period_date`, `total_hours_worked`, `overtime_total`, `late_count`, `early_out_count` |

---

## 4.3 Key Workflows & Business Logic

### 1. Clock In / Clock Out Lifecycle
1. When an employee punches via the web portal, mobile app, or biometric device, an `AttendanceActivity` record is logged with timestamp, device source, IP, and GPS coordinates.
2. If no open `Attendance` record exists for the date, a new record is initialized with `attendance_clock_in`.
3. Subsequent punches calculate total duration at work (`attendance_worked_hour`).
4. Shift start time is compared with actual check-in time. If the arrival exceeds the assigned shift's `GraceTime`, an `AttendanceLateComeEarlyOut` record is registered.
5. If total worked hours fall below `minimum_hours_half_day`, the day is marked as Absent or Half Day based on `AttendanceValidationCondition`.

### 2. Overtime & Regularization Requests
- When an employee works beyond their scheduled shift conclusion, surplus minutes are captured. If overtime tracking is active, an `AttendanceOverTime` request is routed to the employee's reporting manager.
- If an employee forgets to clock in/out, they submit an **Attendance Regularization Request** via ESS with justification notes. Upon manager approval, the master `Attendance` record updates and is marked `is_validated = True`.
""",
    "content_html": """
<div class="chapter-content">
  <p>The <code>attendance</code> application enforces precise working hour tracking, shift compliance, grace period allowances, overtime approvals, and daily work record generation.</p>

  <h3>Key Relational Models</h3>
  <table class="data-table">
    <thead>
      <tr><th>Model</th><th>Key Attributes</th><th>Function</th></tr>
    </thead>
    <tbody>
      <tr><td><code>Attendance</code></td><td><code>employee</code>, <code>attendance_clock_in</code>, <code>attendance_clock_out</code>, <code>attendance_worked_hour</code></td><td>Daily master record of employee presence.</td></tr>
      <tr><td><code>AttendanceActivity</code></td><td><code>time</code>, <code>clock_in</code>, <code>clock_out</code>, <code>device_id</code>, <code>ip_address</code></td><td>Granular audit log of each individual punch event.</td></tr>
      <tr><td><code>AttendanceOverTime</code></td><td><code>employee</code>, <code>overtime_hour</code>, <code>status</code>, <code>approved_by</code></td><td>Verified extra hours and approval workflow.</td></tr>
      <tr><td><code>AttendanceLateComeEarlyOut</code></td><td><code>type</code>, <code>duration_minutes</code>, <code>reason</code>, <code>is_excused</code></td><td>Tracks shift variance penalties and excused exceptions.</td></tr>
      <tr><td><code>WorkRecords</code></td><td><code>regular_hours</code>, <code>overtime_hours</code>, <code>loss_of_pay_units</code></td><td>Normalized daily work metrics feeding into Payroll.</td></tr>
    </tbody>
  </table>
</div>
"""
})

# ==============================================================================
# CHAPTER 5: BIOMETRIC, FACE DETECTION & GEOFENCING
# ==============================================================================
CHAPTERS.append({
    "num": 5,
    "id": "biometric-face-geofence",
    "title": "Biometric Devices, Facial Recognition & Geofencing (`biometric`, `facedetection`, `geofencing`)",
    "subtitle": "Hardware time clock synchronization, AI camera face recognition, and GPS boundary validation.",
    "content_md": """
## 5.1 Overview & Responsibilities

To accommodate varied corporate environments—from traditional corporate offices and manufacturing facilities to remote and field workforces—HRMS incorporates three advanced verification modules:
1. **`biometric`**: Direct hardware network integration with standalone biometric terminals (ZKTeco, Matrix COSEC, TCP/IP time-clocks).
2. **`facedetection`**: Browser and kiosk camera-based facial recognition attendance capture.
3. **`geofencing`**: GPS location perimeter validation for mobile and field employees.

---

## 5.2 Biometric Device Integration (`biometric`)

### Database Models
- `BiometricDevices`: Represents physical hardware clocks. Attributes: `device_name`, `device_ip`, `port`, `device_type` (ZKTeco, Matrix, Suprema), `username`, `password`, `company` (FK), `last_sync_time`, `is_active`.
- `BiometricEmployees`: Maps HRMS internal `badge_id` to hardware device user IDs, fingerprint templates, and RFID card numbers.
- `COSECAttendanceArguments`: Specialized parameters for Matrix COSEC enterprise device communication.

### Synchronization Architecture
A background synchronization service connects via TCP socket or HTTP API to active biometric devices on scheduled cron intervals:
1. Queries the terminal's punch log buffer.
2. Extracts raw punch records (`user_id`, `timestamp`, `in_out_mode`).
3. Resolves the corresponding `Employee` record via `BiometricEmployees`.
4. Ingests raw punches into `AttendanceActivity` and computes daily `Attendance`.
5. Clears or acknowledges processed logs on the physical terminal to prevent duplicates.

---

## 5.3 Facial Recognition Attendance (`facedetection`)

### Database Models & Workflow
- `FaceDetection`: System configuration for camera-based face verification, confidence threshold (e.g. 0.85), and anti-spoofing flags.
- `EmployeeFaceDetection`: Stores 128-dimensional facial feature vector embeddings extracted from employee photo uploads.

### Kiosk & Web Punch Flow
1. An on-site tablet kiosk or employee browser activates the camera.
2. Captures face frame, evaluates liveness (blink or micro-movement detection to prevent photo spoofing).
3. Compares facial embedding vectors against the registered gallery in `EmployeeFaceDetection` using Euclidean distance / cosine similarity.
4. On positive match (confidence >= threshold), generates an automated clock-in/out in `attendance`.

---

## 5.4 Geofencing Boundary Validation (`geofencing`)

### Database Models & Logic
- `GeoFencing`: Office or work-site boundary definition: `location_name`, `company` (FK), `latitude`, `longitude`, `radius_in_meters`, `is_active`.

### Validation Workflow
When field employees clock in via mobile ESS:
1. The client sends HTML5 Geolocation coordinates (`lat`, `lng`, `accuracy`).
2. The server executes the **Haversine formula** against all active `GeoFencing` sites assigned to the employee:
   $$d = 2r \\arcsin\\left(\\sqrt{\\sin^2\\left(\\frac{\\Delta \\phi}{2}\\right) + \\cos(\\phi_1)\\cos(\\phi_2)\\sin^2\\left(\\frac{\\Delta \\lambda}{2}\\right)}\\right)$$
3. If distance $d \\le \\text{radius}$, the punch is approved and tagged with location.
4. If out of bounds, the punch is rejected or submitted as an exception flag requiring manager review.
""",
    "content_html": """
<div class="chapter-content">
  <p>HRMS provides cutting-edge hardware, computer vision, and spatial intelligence modules to verify attendance integrity across all workforce environments.</p>

  <h3>Hardware & Location Features</h3>
  <div class="feature-grid">
    <div class="feature-card">
      <h4>Biometric Hardware Clocks</h4>
      <p>Direct TCP/IP and API integration with ZKTeco, Matrix COSEC, and Suprema biometric terminals with automated scheduled log pulling.</p>
    </div>
    <div class="feature-card">
      <h4>Facial Recognition Kiosks</h4>
      <p>Touchless camera attendance with 128-dimensional vector embedding comparison and anti-spoofing liveness verification.</p>
    </div>
    <div class="feature-card">
      <h4>GPS Geofencing</h4>
      <p>Restricts mobile clock-ins within authorized radius perimeters calculated via the Haversine spherical distance formula.</p>
    </div>
  </div>
</div>
"""
})

# ==============================================================================
# CHAPTER 6: LEAVE & ABSENCE MANAGEMENT
# ==============================================================================
CHAPTERS.append({
    "num": 6,
    "id": "leave-management",
    "title": "Leave & Absence Management (`leave`)",
    "subtitle": "Leave types, accrual logic, available balances, multi-tier approvals, carry-overs, and holiday calendars.",
    "content_md": """
## 6.1 Overview & Responsibilities

The `leave` application provides comprehensive absence administration. It manages categorized leave quotas (Annual, Sick, Casual, Maternity, Paternity, Compensatory Off, Unpaid Leave), calculates dynamic monthly or annual accruals, verifies supporting medical documents, enforces blackout dates, and manages multi-level approval hierarchies.

---

## 6.2 Database Models Specification

| Model Name | Purpose | Primary Attributes & Relationships |
|---|---|---|
| `LeaveType` | Definition of distinct leave categories. | `name`, `company` (FK), `color_code`, `is_paid`, `is_carry_forward`, `max_carry_forward_days`, `is_encashable`, `requires_approval`, `requires_attachment` |
| `LeaveTypeCondition` | Accrual rules, probation eligibility, and duration limits. | `leave_type` (FK), `accrual_frequency` (Monthly/Yearly/Lump Sum), `probation_period_months`, `max_consecutive_days`, `sandwich_rule_active` |
| `AvailableLeave` | Live balance ledger per employee per leave type. | `employee` (FK), `leave_type` (FK), `allocated_days`, `used_days`, `pending_approval_days`, `carry_forward_days`, `remaining_days` |
| `LeaveRequest` | Employee leave application record. | `employee` (FK), `leave_type` (FK), `start_date`, `end_date`, `duration` (Full Day / Half Day), `reason`, `status` (Requested/Approved/Rejected/Cancelled) |
| `LeaverequestFile` | File attachments (medical certificates, travel orders) for leave requests. | `leave_request` (FK), `attachment_file`, `uploaded_at` |
| `LeaverequestComment` | Two-way dialogue thread between applicant and approving managers. | `leave_request` (FK), `commenter` (FK to User), `comment_text`, `created_at` |
| `LeaveAllocationRequest` | Employee requests for additional leave grants (e.g. Compensatory Off). | `employee` (FK), `leave_type` (FK), `requested_days`, `reason`, `status` |
| `LeaveallocationrequestComment` | Discussion notes on manual leave allocation claims. | `leave_allocation_request` (FK), `commenter` (FK), `comment_text` |
| `LeaveRequestConditionApproval`| Tracks individual stage approvals in a multi-tier approval chain. | `leave_request` (FK), `approval_stage`, `approver` (FK), `action` (Approved/Rejected), `action_date` |
| `RestrictLeave` | Departmental or corporate blackout windows restricting leave. | `company` (FK), `department` (FK), `start_date`, `end_date`, `reason` |
| `LeaveGeneralSetting` | Global parameters governing retroactive leave limits and calendar displays. | `max_past_days_to_apply`, `include_holidays_in_duration`, `enable_comp_off` |
| `EmployeePastLeaveRestrict` | Specific exemptions or restrictions on applying for past-dated leave. | `employee` (FK), `allow_past_leave`, `max_retroactive_days` |

---

## 6.3 Leave Application & Approval Workflow

```text
[Employee Submits Request]
           │
           ▼
[Validate Balance in AvailableLeave]
           │
           ├─ Negative Balance? ──► [Reject Application]
           │
           ▼
[Check RestrictLeave Blackout Windows & Past Limits]
           │
           ▼
[Determine Approver Sequence (MultipleApprovalCondition)]
           │
           ▼
[Tier 1: Reporting Manager Review]
    ├─ Rejected ──► [Status: Rejected, Release Pending Days]
    └─ Approved ──► [Tier 2: HR / Department Head Review]
                         ├─ Rejected ──► [Status: Rejected]
                         └─ Approved ──► [Status: Approved, Deduct from Remaining Days]
```

- **Sandwich Rule Processing**: If configured on `LeaveTypeCondition`, weekends or public holidays occurring between leave days are automatically counted as leave consumption.
- **Accrual Engine**: Scheduled monthly background jobs credit fractional leave allocations (e.g. 1.75 days/month for Annual Leave) directly into `AvailableLeave`.
""",
    "content_html": """
<div class="chapter-content">
  <p>The <code>leave</code> module delivers an enterprise absence workflow handling accrual quotas, carry-overs, blackout periods, and multi-tier approval chains.</p>

  <h3>Leave Architecture & Balances</h3>
  <table class="data-table">
    <thead>
      <tr><th>Model</th><th>Key Attributes</th><th>Function</th></tr>
    </thead>
    <tbody>
      <tr><td><code>LeaveType</code></td><td><code>name</code>, <code>is_paid</code>, <code>is_carry_forward</code>, <code>is_encashable</code></td><td>Defines leave quota rules and financial attributes.</td></tr>
      <tr><td><code>AvailableLeave</code></td><td><code>allocated_days</code>, <code>used_days</code>, <code>remaining_days</code></td><td>Live balance ledger per employee per leave type.</td></tr>
      <tr><td><code>LeaveRequest</code></td><td><code>start_date</code>, <code>end_date</code>, <code>duration</code>, <code>status</code></td><td>Employee absence application and status lifecycle.</td></tr>
      <tr><td><code>LeaveRequestConditionApproval</code></td><td><code>approval_stage</code>, <code>approver</code>, <code>action</code></td><td>Multi-tier hierarchical approval records.</td></tr>
      <tr><td><code>RestrictLeave</code></td><td><code>start_date</code>, <code>end_date</code>, <code>department</code></td><td>Blackout windows prohibiting leave requests.</td></tr>
    </tbody>
  </table>
</div>
"""
})

# ==============================================================================
# CHAPTER 7: PAYROLL, COMPENSATION & BENEFITS
# ==============================================================================
CHAPTERS.append({
    "num": 7,
    "id": "payroll-compensation",
    "title": "Payroll, Compensation & Benefits Administration (`payroll`)",
    "subtitle": "Employment contracts, salary structures, earnings, statutory deductions, tax brackets, loans, and batch payslips.",
    "content_md": """
## 7.1 Overview & Responsibilities

The `payroll` application constitutes the financial compensation core of HRMS. It models complex remuneration packages, computes earnings allowances, calculates statutory deductions and income tax brackets, processes employee loans and expense reimbursements, generates monthly batch payslips, renders official PDF payslips, and archives detailed audit trails.

---

## 7.2 Database Models Specification

| Model Name | Purpose | Primary Attributes & Relationships |
|---|---|---|
| `Contract` | Employment terms, contract validity, and compensation baseline. | `employee` (FK), `contract_title`, `wage_type` (Monthly/Hourly), `wage`, `start_date`, `end_date`, `salary_structure` (FK), `status` (Draft/Active/Terminated) |
| `SalaryStructure` | Master compensation template combining allowances and deduction rules. | `structure_name`, `company` (FK), `base_salary_percentage`, `description` |
| `Allowance` | Earnings components (e.g. Basic, HRA, Medical, Transport, Performance Bonus). | `allowance_name`, `company` (FK), `value_type` (Fixed Amount / Percentage of Base), `value`, `is_taxable`, `is_condition_based` |
| `Deduction` | Deduction components (e.g. Provident Fund, Health Insurance, Professional Tax). | `deduction_name`, `company` (FK), `value_type` (Fixed / Percentage), `value`, `is_statutory` |
| `FilingStatus` & `TaxBracket` | Tax slabs, progressive tax rates, and standard deduction brackets. | `filing_status_name`, `min_income`, `max_income`, `tax_percentage`, `fixed_tax_amount` |
| `Payslip` | Master monthly remuneration statement for an employee. | `employee` (FK), `contract` (FK), `month`, `year`, `basic_pay`, `gross_pay`, `total_allowance`, `total_deduction`, `net_pay`, `status` (Draft/Generated/Approved/Paid), `pdf_file` |
| `PayslipAutoGenerate` | Scheduled batch runner configuration for automated monthly payroll. | `company` (FK), `generation_day_of_month`, `auto_send_email`, `is_active` |
| `LoanAccount` | Corporate employee loans and automated installment recovery. | `employee` (FK), `loan_amount`, `monthly_installment`, `total_installments`, `paid_installments`, `remaining_balance`, `interest_rate`, `status` |
| `Reimbursement` | Employee business expense claims and receipts. | `employee` (FK), `claim_title`, `amount`, `receipt_date`, `status` (Requested/Approved/Paid), `approved_by` |
| `ReimbursementFile` | Scanned receipts, invoices, and expense documentation. | `reimbursement` (FK), `attachment_file`, `uploaded_at` |
| `PayrollGeneralSetting` | Global payroll parameters: currency, work days per month, loss-of-pay formula. | `currency_symbol`, `default_work_days_per_month`, `lop_calculation_mode`, `payslip_prefix` |
| `EncashmentGeneralSettings` | Policies for leave encashment calculations upon year-end or separation. | `encashable_leave_types` (M2M), `encashment_wage_basis` (Basic vs Gross), `max_encashable_days` |

---

## 7.3 Salary Calculation Formula & Workflow

The calculation of monthly remuneration follows rigorous financial formulas:

1. **Working Days & Loss of Pay (LOP)**:
   $$\\text{Effective Days} = \\text{Total Month Days} - \\text{Unpaid Leaves} - \\text{Unauthorized Absences}$$
   $$\\text{Base Pro-rated Salary} = \\left(\\frac{\\text{Contract Wage}}{\\text{Work Days in Month}}\\right) \\times \\text{Effective Days}$$

2. **Gross Earnings**:
   $$\\text{Gross Pay} = \\text{Base Salary} + \\sum \\text{Allowances} + \\text{Approved Overtime} + \\text{Reimbursements}$$

3. **Total Deductions**:
   $$\\text{Total Deductions} = \\sum \\text{Statutory Deductions} + \\text{Income Tax} + \\text{Loan Installment} + \\text{Disciplinary Fines}$$

4. **Net Disbursed Salary**:
   $$\\text{Net Pay} = \\text{Gross Pay} - \\text{Total Deductions}$$

When batch payslip generation executes, the system creates individual `Payslip` records, generates formatted PDF documents, stores them in the media archive, and optionally delivers them via email to each employee.
""",
    "content_html": """
<div class="chapter-content">
  <p>The <code>payroll</code> module orchestrates employment contracts, compensation packages, statutory tax brackets, loan installment deductions, expense claims, and batch payslip generation.</p>

  <h3>Payroll Core Entities</h3>
  <table class="data-table">
    <thead>
      <tr><th>Model</th><th>Key Attributes</th><th>Function</th></tr>
    </thead>
    <tbody>
      <tr><td><code>Contract</code></td><td><code>wage</code>, <code>wage_type</code>, <code>salary_structure</code>, <code>status</code></td><td>Binds employee to wage rate and salary structure.</td></tr>
      <tr><td><code>SalaryStructure</code></td><td><code>structure_name</code>, <code>base_salary_percentage</code></td><td>Package definition grouping allowances and deductions.</td></tr>
      <tr><td><code>Allowance</code></td><td><code>allowance_name</code>, <code>value_type</code>, <code>value</code>, <code>is_taxable</code></td><td>Earnings additions (HRA, Transport, Medical).</td></tr>
      <tr><td><code>Deduction</code></td><td><code>deduction_name</code>, <code>value_type</code>, <code>value</code>, <code>is_statutory</code></td><td>Pay deductions (PF, Tax, Health Insurance).</td></tr>
      <tr><td><code>Payslip</code></td><td><code>basic_pay</code>, <code>gross_pay</code>, <code>total_deduction</code>, <code>net_pay</code></td><td>Master monthly payment statement with PDF export.</td></tr>
      <tr><td><code>LoanAccount</code></td><td><code>loan_amount</code>, <code>monthly_installment</code>, <code>remaining_balance</code></td><td>Corporate loan recovery via automated payroll deductions.</td></tr>
    </tbody>
  </table>
</div>
"""
})

# ==============================================================================
# CHAPTER 8: PERFORMANCE MANAGEMENT SYSTEM (PMS)
# ==============================================================================
CHAPTERS.append({
    "num": 8,
    "id": "performance-pms",
    "title": "Performance Management System (`pms`)",
    "subtitle": "Objectives & Key Results (OKRs), KPIs, 360-degree feedback, appraisal review cycles, and gamified bonus points.",
    "content_md": """
## 8.1 Overview & Responsibilities

The `pms` application facilitates modern organizational alignment through Objectives and Key Results (OKRs), annual and quarterly appraisal cycles, 360-degree peer reviews, 1-on-1 performance meetings, and gamified employee recognition points.

---

## 8.2 Database Models Specification

| Model Name | Purpose | Primary Attributes & Relationships |
|---|---|---|
| `Period` | Appraisal evaluation timeframes (e.g. Q1 2026, Annual Review 2026). | `period_name`, `company` (FK), `start_date`, `end_date`, `is_active` |
| `Objective` | High-level organizational, departmental, or team strategic goals. | `title`, `company` (FK), `department` (FK), `period` (FK), `target_value`, `unit`, `description` |
| `KeyResult` | Specific, quantifiable outcomes required to accomplish an Objective. | `objective` (FK), `title`, `start_value`, `target_value`, `current_value`, `unit`, `weightage_percentage` |
| `EmployeeObjective` & `EmployeeKeyResult` | Cascaded individual goals assigned to specific employees. | `employee` (FK), `objective` (FK), `progress_percentage`, `self_rating`, `manager_rating`, `status` |
| `QuestionTemplate` & `Question` | Standardized evaluation forms for appraisals and feedback surveys. | `template_name`, `question_text`, `question_type` (Rating 1-5, Text, Multiple Choice) |
| `Feedback` & `AnonymousFeedback` | Continuous peer praise, constructive feedback, and anonymous surveys. | `employee` (FK), `reviewer` (FK), `period` (FK), `feedback_text`, `rating`, `is_anonymous` |
| `Meetings` & `MeetingsAnswer` | 1-on-1 performance review sessions and documented action items. | `employee` (FK), `manager` (FK), `meeting_date`, `agenda`, `minutes`, `next_steps` |
| `EmployeeBonusPoint` & `BonusPointSetting`| Gamified peer-to-peer and managerial recognition point ledger. | `employee` (FK), `points`, `awarded_by` (FK), `reason`, `monthly_award_limit` |

---

## 8.3 Appraisal Review & OKR Tracking Process

1. **Goal Setting**: At the beginning of each `Period`, strategic `Objective` targets are established and broken down into quantifiable `KeyResult` milestones.
2. **Cascading**: Objectives cascade down to individual `EmployeeObjective` records. Employees update progress percentages weekly or monthly.
3. **Appraisal Review**: At period close, formal evaluations are initiated:
   - **Self-Assessment**: The employee provides self-ratings and narrative justifications.
   - **360-Degree Feedback**: Selected peers, direct reports, and cross-functional collaborators submit evaluations via `Feedback`.
   - **Manager Review**: The reporting manager reviews combined feedback, assigns final ratings, and conducts a formal `Meetings` review.
""",
    "content_html": """
<div class="chapter-content">
  <p>The <code>pms</code> application empowers continuous performance management through OKRs, key result tracking, 360-degree reviews, and gamified recognition.</p>

  <h3>Performance System Components</h3>
  <table class="data-table">
    <thead>
      <tr><th>Model</th><th>Key Attributes</th><th>Function</th></tr>
    </thead>
    <tbody>
      <tr><td><code>Period</code></td><td><code>period_name</code>, <code>start_date</code>, <code>end_date</code></td><td>Defines evaluation cycles (Quarterly / Annual).</td></tr>
      <tr><td><code>Objective</code></td><td><code>title</code>, <code>department</code>, <code>period</code></td><td>Strategic organizational or team goals.</td></tr>
      <tr><td><code>KeyResult</code></td><td><code>start_value</code>, <code>target_value</code>, <code>current_value</code></td><td>Quantifiable milestones linked to objectives.</td></tr>
      <tr><td><code>Feedback</code></td><td><code>employee</code>, <code>reviewer</code>, <code>rating</code>, <code>is_anonymous</code></td><td>Peer and 360-degree feedback reviews.</td></tr>
      <tr><td><code>Meetings</code></td><td><code>employee</code>, <code>manager</code>, <code>meeting_date</code>, <code>agenda</code></td><td>1-on-1 manager appraisal review records.</td></tr>
    </tbody>
  </table>
</div>
"""
})

# ==============================================================================
# CHAPTER 9: ASSET MANAGEMENT
# ==============================================================================
CHAPTERS.append({
    "num": 9,
    "id": "asset-management",
    "title": "Asset & Equipment Lifecycle Management (`asset`)",
    "subtitle": "Hardware and software inventory, batch procurement, employee allocation, condition photos, and returns.",
    "content_md": """
## 9.1 Overview & Responsibilities

The `asset` application tracks the complete custody and lifecycle of company physical and digital property—laptops, monitors, mobile phones, peripherals, software licenses, and vehicles. It manages procurement batches, barcode/serial number identification, employee allocations, handover agreements, return condition photographic proof, and maintenance reporting.

---

## 9.2 Database Models Specification

| Model Name | Purpose | Primary Attributes & Relationships |
|---|---|---|
| `AssetCategory` | Classification of asset types (e.g. Laptops, Mobile Devices, Furniture, Software). | `category_name`, `company` (FK), `description`, `depreciation_rate_percentage` |
| `AssetLot` | Procurement batches and purchase orders. | `lot_number`, `vendor_name`, `purchase_date`, `invoice_number`, `total_quantity`, `total_cost` |
| `Asset` | Master asset specification profile. | `asset_name`, `category` (FK), `lot` (FK), `manufacturer`, `model_number`, `specifications` |
| `AssetItem` | Distinct individual physical unit with unique tracking identifiers. | `asset` (FK), `tracking_id`, `serial_number`, `barcode`, `purchase_cost`, `warranty_expiry_date`, `status` (Available/Assigned/In Repair/Disposed) |
| `AssetAssignment` | Custody record tracking assignment of an asset to an employee. | `asset_item` (FK), `assigned_to` (FK to Employee), `assigned_by` (FK), `assigned_date`, `expected_return_date`, `notes` |
| `AssetRequest` | Employee self-service requisition for equipment or replacement. | `employee` (FK), `category` (FK), `reason`, `urgency`, `status` (Requested/Approved/Allocated/Rejected) |
| `ReturnImages` | Photographic documentation verifying asset physical condition upon return. | `asset_assignment` (FK), `image_file`, `uploaded_at`, `notes` |
| `AssetReport` | Damage reports, maintenance logs, and depreciation records. | `asset_item` (FK), `report_type` (Maintenance/Damage/Audit), `cost`, `description`, `reported_by` |
| `AssetDocuments` | Invoices, warranty cards, user manuals, and procurement contracts. | `asset` (FK), `document_file`, `document_name`, `uploaded_at` |

---

## 9.3 Asset Lifecycle Workflow

1. **Procurement & Intake**: Assets arrive in bulk batches recorded under `AssetLot`. Individual physical items are registered in `AssetItem` with unique serial numbers, barcodes, and warranty dates.
2. **Allocation**: When an employee joins or requests equipment via `AssetRequest`, HR or IT assigns an available `AssetItem` creating an `AssetAssignment`. An official handover form is generated.
3. **Return & Condition Audit**: Upon offboarding or equipment upgrades, the asset is returned. IT captures digital photographs stored in `ReturnImages` to confirm device condition, screen integrity, and hardware completeness before releasing clearance.
""",
    "content_html": """
<div class="chapter-content">
  <p>The <code>asset</code> module safeguards company capital through end-to-end hardware tracking, barcode identification, custody records, and digital return inspections.</p>

  <h3>Asset Inventory & Custody</h3>
  <table class="data-table">
    <thead>
      <tr><th>Model</th><th>Key Attributes</th><th>Function</th></tr>
    </thead>
    <tbody>
      <tr><td><code>AssetCategory</code></td><td><code>category_name</code>, <code>depreciation_rate_percentage</code></td><td>Asset classification and depreciation profile.</td></tr>
      <tr><td><code>AssetItem</code></td><td><code>tracking_id</code>, <code>serial_number</code>, <code>warranty_expiry_date</code>, <code>status</code></td><td>Individual trackable asset instance.</td></tr>
      <tr><td><code>AssetAssignment</code></td><td><code>asset_item</code>, <code>assigned_to</code>, <code>assigned_date</code></td><td>Custody record binding equipment to staff.</td></tr>
      <tr><td><code>AssetRequest</code></td><td><code>employee</code>, <code>category</code>, <code>urgency</code>, <code>status</code></td><td>Self-service requisition for new/replacement gear.</td></tr>
      <tr><td><code>ReturnImages</code></td><td><code>asset_assignment</code>, <code>image_file</code>, <code>uploaded_at</code></td><td>Photographic evidence of equipment state on return.</td></tr>
    </tbody>
  </table>
</div>
"""
})

# ==============================================================================
# CHAPTER 10: RECRUITMENT & ATS
# ==============================================================================
CHAPTERS.append({
    "num": 10,
    "id": "recruitment-ats",
    "title": "Recruitment & Applicant Tracking System (`recruitment`)",
    "subtitle": "Job openings, multi-stage hiring pipelines, resume parsing, interview scorecards, and candidate skill zones.",
    "content_md": """
## 10.1 Overview & Responsibilities

The `recruitment` application delivers an enterprise Applicant Tracking System (ATS). It oversees talent acquisition from vacancy requisition, job posting, and candidate intake to resume parsing, pipeline stage transitions, interview scheduling, scorecard rating, and talent pool archiving.

---

## 10.2 Database Models Specification

| Model Name | Purpose | Primary Attributes & Relationships |
|---|---|---|
| `Recruitment` | Job opening campaign. | `recruitment_title`, `company` (FK), `department` (FK), `job_position` (FK), `open_positions`, `start_date`, `end_date`, `job_description`, `status` (Open/Closed/On Hold) |
| `Stage` | Configurable hiring pipeline stages for a recruitment campaign. | `recruitment` (FK), `stage_name` (e.g. Applied, Tech Screening, Panel Interview, Offer), `sequence_order` |
| `Candidate` | Applicant profile and recruitment progress tracker. | `recruitment` (FK), `stage` (FK), `first_name`, `last_name`, `email`, `phone`, `current_ctc`, `expected_ctc`, `notice_period_days`, `status` |
| `Resume` | Candidate resume documents and parsed plain-text representation. | `candidate` (FK), `resume_file`, `parsed_text`, `uploaded_at` |
| `Skill` & `SkillZone` | Skill taxonomy tags and talent pools for future requisition matching. | `skill_name`, `category`, `candidates` (M2M via `SkillZoneCandidate`) |
| `InterviewSchedule` | Scheduled interview rounds with panel links and calendar integrations. | `candidate` (FK), `stage` (FK), `interview_date`, `interview_time`, `interviewers` (M2M), `meeting_link`, `status` |
| `CandidateRating` | Interviewer scorecard evaluations, criteria ratings, and comments. | `candidate` (FK), `interview` (FK), `interviewer` (FK), `rating` (1-5), `technical_skills`, `communication`, `recommendation` |
| `CandidateDocumentRequest` & `CandidateDocument` | Pre-offer document requests (degrees, previous pay slips, ID proofs). | `candidate` (FK), `document_title`, `file`, `status` (Pending/Uploaded/Verified) |
| `RejectReason` & `RejectedCandidate` | Standardized rejection reasons and talent pool archiving. | `candidate` (FK), `reject_reason` (FK), `rejection_notes`, `rejected_at` |
| `RecruitmentSurvey` & `SurveyTemplate` | Candidate candidate-experience feedback surveys. | `title`, `questions`, `answers` (FK to `RecruitmentSurveyAnswer`) |

---

## 10.3 Hiring Pipeline Execution

```text
[Job Requisition: Recruitment]
              │
              ▼
[Candidate Application & Resume Ingestion]
              │
              ▼
[Pipeline Stages: Stage 1 ➔ Stage 2 ➔ Stage 3]
              │
    ┌─────────┴─────────┐
    ▼                   ▼
[Interview Scheduled]  [Candidate Rating Scorecard]
    │                   │
    └─────────┬─────────┘
              ▼
[Final Decision] ──► Hired ──► [Handoff to Onboarding]
                 └──► Rejected ──► [Log RejectReason & Archive]
```
""",
    "content_html": """
<div class="chapter-content">
  <p>The <code>recruitment</code> application is an enterprise ATS managing hiring pipelines, resume indexing, interview scorecards, and candidate evaluation.</p>

  <h3>Recruitment Core Entities</h3>
  <table class="data-table">
    <thead>
      <tr><th>Model</th><th>Key Attributes</th><th>Function</th></tr>
    </thead>
    <tbody>
      <tr><td><code>Recruitment</code></td><td><code>recruitment_title</code>, <code>job_position</code>, <code>open_positions</code></td><td>Job opening requisition and vacancies.</td></tr>
      <tr><td><code>Stage</code></td><td><code>recruitment</code>, <code>stage_name</code>, <code>sequence_order</code></td><td>Sequential stages in the hiring pipeline.</td></tr>
      <tr><td><code>Candidate</code></td><td><code>first_name</code>, <code>last_name</code>, <code>stage</code>, <code>expected_ctc</code></td><td>Applicant profile and pipeline position.</td></tr>
      <tr><td><code>InterviewSchedule</code></td><td><code>candidate</code>, <code>interview_date</code>, <code>interviewers</code>, <code>meeting_link</code></td><td>Interview round booking and calendar integration.</td></tr>
      <tr><td><code>CandidateRating</code></td><td><code>candidate</code>, <code>rating</code>, <code>technical_skills</code>, <code>recommendation</code></td><td>Interviewer scorecard and hiring recommendation.</td></tr>
    </tbody>
  </table>
</div>
"""
})

# ==============================================================================
# CHAPTER 11: ONBOARDING
# ==============================================================================
CHAPTERS.append({
    "num": 11,
    "id": "onboarding-module",
    "title": "Employee Onboarding Management (`onboarding`)",
    "subtitle": "Pre-boarding portal, onboarding stages, task checklists, document submission, and conversion to employee.",
    "content_md": """
## 11.1 Overview & Responsibilities

The `onboarding` application guides new hires from the moment an offer is accepted until their first 90 days of employment. It provides an external self-service portal where candidates can upload compliance documentation, complete onboarding checklists, and familiarize themselves with company culture prior to day one.

---

## 11.2 Database Models Specification

| Model Name | Purpose | Primary Attributes & Relationships |
|---|---|---|
| `OnboardingStage` | Sequential phases in the onboarding journey. | `stage_name` (e.g. Pre-boarding, Day 1 Orientation, Week 1 Induction, Probation), `sequence_order`, `company` (FK) |
| `OnboardingTask` | Reusable checklist tasks assigned to departments or the candidate. | `stage` (FK), `task_title`, `assigned_department` (IT/HR/Finance/Facilities), `due_days_from_joining`, `is_mandatory` |
| `OnboardingCandidate` | Prospective employee record in the onboarding pipeline. | `candidate` (FK from recruitment), `first_name`, `last_name`, `email`, `joining_date`, `status` (In Progress / Completed) |
| `CandidateStage` | Tracks a candidate's current stage completion status. | `candidate` (FK to OnboardingCandidate), `stage` (FK), `is_completed`, `completed_at` |
| `CandidateTask` | Specific task assignment for an onboarding candidate. | `candidate` (FK), `task` (FK to OnboardingTask), `status` (Pending/In Review/Completed), `submitted_file`, `verified_by` |
| `OnboardingPortal` | Security access tokens for external pre-hire portal access. | `candidate` (FK), `access_token`, `token_expiry`, `is_active` |

---

## 11.3 Onboarding Lifecycle

1. **Candidate Handoff**: A hired candidate in `recruitment` is promoted to `OnboardingCandidate`.
2. **Pre-Boarding Access**: An `OnboardingPortal` token is generated and emailed to the candidate. Without requiring full system login, the candidate accesses their private portal to provide bank information, national identity cards, emergency contacts, and signed agreements.
3. **Cross-Departmental Tasks**: `CandidateTask` entries are automatically triggered for departmental teams:
   - **IT**: Configure email account, prepare laptop, allocate software licenses.
   - **Admin / Facilities**: Issue building access pass and desk allocation.
   - **HR**: Verify educational credentials, initiate background verification.
4. **Employee Profile Generation**: Upon completing onboarding stages, a single action creates the permanent `Employee` profile, `EmployeeWorkInformation`, and `HRMSUser` account.
""",
    "content_html": """
<div class="chapter-content">
  <p>The <code>onboarding</code> module guarantees a seamless welcome experience, structuring pre-joining document intake, departmental tasks, and automated conversion into full employee records.</p>
</div>
"""
})

# ==============================================================================
# CHAPTER 12: OFFBOARDING & EXIT CLEARANCE
# ==============================================================================
CHAPTERS.append({
    "num": 12,
    "id": "offboarding-exit",
    "title": "Employee Offboarding & Exit Clearance (`offboarding`)",
    "subtitle": "Resignations, notice periods, multi-department clearances (IT, HR, Finance), exit interviews, and settlement.",
    "content_md": """
## 12.1 Overview & Responsibilities

The `offboarding` application governs employee separations—voluntary resignations, contract expirations, or terminations. It ensures strict governance across asset recovery, financial settlements, non-disclosure compliance, system de-provisioning, and exit interview analytics.

---

## 12.2 Database Models Specification

| Model Name | Purpose | Primary Attributes & Relationships |
|---|---|---|
| `ResignationLetter` | Formal resignation application submitted by an employee. | `employee` (FK), `resignation_date`, `requested_last_working_day`, `reason`, `status` (Requested/Accepted/Withdrawn/Rejected) |
| `Offboarding` | Approved separation case governing notice period and clearance. | `employee` (FK), `notice_period_days`, `approved_last_working_day`, `exit_reason` (FK), `status` (In Progress/Completed) |
| `OffboardingStage` | Departmental clearance checkpoints (IT, Finance, HR, Admin). | `stage_name`, `sequence_order`, `responsible_department` (FK) |
| `OffboardingTask` | Specific clearance items required by departments. | `stage` (FK), `task_title`, `description`, `is_mandatory` |
| `EmployeeTask` | Individual task assignment and clearance status per exiting employee. | `offboarding_employee` (FK), `task` (FK), `status` (Pending/Cleared/Rejected), `cleared_by` (FK), `clearance_date` |
| `ExitReason` | Standardized separation categories for workforce attrition analytics. | `reason_title`, `category` (Career Growth, Compensation, Personal, Relocation) |
| `OffboardingNote` | Confidential HR exit interview transcripts and settlement notes. | `offboarding` (FK), `notes`, `created_by` (FK), `created_at` |
| `OffboardingGeneralSetting` | Policy parameters for notice period waivers, gratuity rules, and account locking. | `auto_lock_account_on_exit`, `default_notice_days`, `require_asset_clearance` |

---

## 12.3 Multi-Department Clearance Workflow

1. **Submission & Acceptance**: Employee submits `ResignationLetter`. Reporting manager and HR review notice obligations and approve official `approved_last_working_day`.
2. **Clearance Checklists**: System spawns clearance tasks across departments:
   - **IT Department**: Verify return of laptop and peripherals, revoke VPN and corporate email, remove GitHub/Jira access.
   - **Finance Department**: Calculate remaining loan balances, travel expense claims, and compute Full & Final (F&F) settlement amount.
   - **HR Department**: Conduct exit interview survey, process leave encashment calculations, prepare Relieving and Experience letters.
   - **Facilities**: Retrieve physical building access cards and company vehicle keys.
3. **Archival**: Upon 100% task clearance, the `Employee` record is marked `is_active = False` and `HRMSUser` account is locked.
""",
    "content_html": """
<div class="chapter-content">
  <p>The <code>offboarding</code> application ensures systematic, compliant employee exits, tracking asset returns, departmental sign-offs, exit interviews, and final settlements.</p>
</div>
"""
})

# ==============================================================================
# CHAPTER 13: PROJECT MANAGEMENT & TIMESHEETS
# ==============================================================================
CHAPTERS.append({
    "num": 13,
    "id": "project-timesheets",
    "title": "Project Management & Timesheets (`project`)",
    "subtitle": "Project tracking, Kanban task boards, milestones, and billable hour timesheets.",
    "content_md": """
## 13.1 Overview & Responsibilities

The `project` application provides project tracking and workforce utilization tools directly inside HRMS. Teams can create projects, organize tasks across Kanban stages, assign employees, monitor deadlines, and log daily timesheets for payroll and client billing.

---

## 13.2 Database Models Specification

| Model Name | Purpose | Primary Attributes & Relationships |
|---|---|---|
| `Project` | Master project record. | `project_name`, `company` (FK), `client_name`, `project_manager` (FK to Employee), `start_date`, `end_date`, `budget`, `status` (Planning/Active/On Hold/Completed) |
| `ProjectStage` | Workflow states for project tasks (e.g. Backlog, In Progress, In Review, Done). | `project` (FK), `stage_name`, `sequence_order` |
| `Task` | Individual work assignments and deliverables. | `project` (FK), `stage` (FK), `task_name`, `assigned_to` (M2M to Employee), `priority` (Low/Medium/High/Urgent), `estimated_hours`, `due_date`, `status` |
| `TimeSheet` | Daily hours logged by employees against specific tasks and projects. | `employee` (FK), `project` (FK), `task` (FK), `date`, `hours_spent`, `is_billable`, `description`, `status` (Draft/Submitted/Approved) |
""",
    "content_html": """
<div class="chapter-content">
  <p>The <code>project</code> module integrates project tracking and billable work records, connecting task execution to workforce timesheets.</p>
</div>
"""
})

# ==============================================================================
# CHAPTER 14: HELPDESK & INTERNAL TICKETING
# ==============================================================================
CHAPTERS.append({
    "num": 14,
    "id": "helpdesk-ticketing",
    "title": "Helpdesk & Internal Support Ticketing (`helpdesk`)",
    "subtitle": "Internal ticketing system, departmental routing, SLA timers, comments, and knowledge base FAQs.",
    "content_md": """
## 14.1 Overview & Responsibilities

The `helpdesk` module provides an internal support desk where employees submit service requests, report hardware issues, query payroll discrepancies, or resolve policy questions. It includes SLA tracking, departmental routing, two-way threaded discussions, and a self-service FAQ knowledge base.

---

## 14.2 Database Models Specification

| Model Name | Purpose | Primary Attributes & Relationships |
|---|---|---|
| `TicketType` | Ticket classification (e.g. IT Incident, Payroll Query, HR Request, Facilities). | `type_name`, `department` (FK), `sla_hours`, `company` (FK) |
| `Ticket` | Individual support ticket. | `ticket_number`, `employee` (FK), `ticket_type` (FK), `title`, `description`, `priority` (Low/Medium/High/Urgent), `status` (Open/Assigned/In Progress/Resolved/Closed), `assigned_to` (FK to Employee) |
| `DepartmentManager` | Designates lead support agents responsible for ticket queues per department. | `department` (FK), `manager` (FK to Employee), `company` (FK) |
| `Comment` | Threaded discussions between employee and assigned support agents. | `ticket` (FK), `author` (FK to User), `comment_text`, `is_internal_note`, `created_at` |
| `Attachment` | File attachments (screenshots, logs, error reports) linked to tickets. | `ticket` (FK), `attachment_file`, `uploaded_at` |
| `ClaimRequest` | Specific financial or resource claims associated with a ticket. | `ticket` (FK), `claim_amount`, `claim_reason`, `status` |
| `FAQCategory` & `FAQ` | Self-service articles answering common employee questions. | `category` (FK), `question`, `answer_html`, `is_published` |
""",
    "content_html": """
<div class="chapter-content">
  <p>The <code>helpdesk</code> application streamlines internal service delivery across IT, HR, Finance, and Facilities with SLA monitoring and self-service FAQs.</p>
</div>
"""
})

# ==============================================================================
# CHAPTER 15: REPORTING & BI ENGINE
# ==============================================================================
CHAPTERS.append({
    "num": 15,
    "id": "reporting-bi",
    "title": "Reporting & Business Intelligence Engine (`report`)",
    "subtitle": "Dynamic report builder, scheduled email subscriptions, saved views, and multi-format exports (CSV, Excel, PDF).",
    "content_md": """
## 15.1 Overview & Responsibilities

The `report` application provides comprehensive cross-module analytics. HR directors and executive leadership can generate real-time metrics on headcount distribution, attrition trends, attendance punctuality, leave utilization, asset allocations, and payroll expenditures.

---

## 15.2 Database Models Specification

| Model Name | Purpose | Primary Attributes & Relationships |
|---|---|---|
| `ReportTemplate` | Pre-configured or custom query definitions for specific modules. | `template_name`, `module` (Employee/Attendance/Leave/Payroll/Asset), `selected_fields`, `filter_criteria` |
| `ReportSubscription`| Scheduled automated report delivery to managers' emails. | `template` (FK), `recipient_emails`, `frequency` (Daily/Weekly/Monthly), `export_format` (CSV/Excel/PDF), `is_active` |
| `ReportFavorite` | Personal pinned reports for quick access on user dashboards. | `user` (FK), `template` (FK) |
| `ReportSavedView` | User-customized column sets, sorting rules, and filter presets. | `template` (FK), `user` (FK), `view_name`, `column_configuration` |
| `ReportRunLog` | Audit log tracking report execution duration, record counts, and user identity. | `template` (FK), `executed_by` (FK), `executed_at`, `duration_seconds`, `rows_count` |
| `ReportAccess` | Role-based permission controls dictating who can run sensitive financial reports. | `template` (FK), `allowed_roles` (M2M), `allowed_departments` (M2M) |
""",
    "content_html": """
<div class="chapter-content">
  <p>The <code>report</code> application delivers dynamic workforce analytics, scheduled email dispatches, and multi-format streaming data exports.</p>
</div>
"""
})

# ==============================================================================
# CHAPTER 16: REST API & SWAGGER
# ==============================================================================
CHAPTERS.append({
    "num": 16,
    "id": "rest-api-swagger",
    "title": "RESTful API Architecture & Interactive Swagger UI (`hrms_api`)",
    "subtitle": "Django REST Framework endpoints, SimpleJWT bearer tokens, Swagger UI, ReDoc, and module serializers.",
    "content_md": """
## 16.1 Overview & Architecture

The `hrms_api` application exposes secure RESTful endpoints for integration with mobile applications, corporate portals, and third-party systems. Built with Django REST Framework (DRF) and `drf_yasg`, it provides full OpenAPI 3.0 interactive documentation via Swagger UI (`/api/v1/swagger/`) and ReDoc (`/api/v1/redoc/`).

---

## 16.2 Authentication & Security

- **JWT Authentication**: Clients obtain JSON Web Token pairs via `/api/v1/auth/token/` and refresh via `/api/v1/auth/token/refresh/`.
- **Bearer Token Header**: All subsequent API calls require:
  ```http
  Authorization: Bearer <jwt_access_token>
  ```
- **Permission Classes**: Endpoints enforce `IsAuthenticated` alongside granular role checks. Managerial endpoints enforce custom permissions returning HTTP 403 Forbidden for unauthorized tiers.

---

## 16.3 Module API Coverage Matrix

The API encompasses 14 dedicated packages under `hrms_api/api_urls/`:

| API Domain | Base Endpoint | Key Operations |
|---|---|---|
| **Auth** | `/api/v1/auth/` | Token obtain, token refresh, password reset, user profile |
| **Base** | `/api/v1/base/` | Companies, departments, job positions, shifts, work types |
| **Employee** | `/api/v1/employee/` | Employee CRUD, work info, bank details, emergency contacts |
| **Attendance**| `/api/v1/attendance/` | Clock-in, clock-out, attendance validation, overtime requests |
| **Leave** | `/api/v1/leave/` | Leave types, available balances, request submissions, approvals |
| **Payroll** | `/api/v1/payroll/` | Contracts, salary structures, payslip queries, expense claims |
| **PMS** | `/api/v1/pms/` | OKRs, objectives, key results, 360 feedback submissions |
| **Asset** | `/api/v1/asset/` | Asset catalog, asset items, assignment history, asset requests |
| **Recruitment**| `/api/v1/recruitment/` | Openings, candidates, interview schedules, candidate ratings |
| **Onboarding** | `/api/v1/onboarding/` | Onboarding candidates, task lists, portal submissions |
| **Offboarding**| `/api/v1/offboarding/`| Resignation requests, departmental clearance checklists |
| **Project** | `/api/v1/project/` | Projects, tasks, stages, timesheet logging |
| **Helpdesk** | `/api/v1/helpdesk/` | Tickets, comments, ticket types, attachments |
| **Notifications**| `/api/v1/notifications/`| Unread notifications, mark-as-read, user broadcasts |
""",
    "content_html": """
<div class="chapter-content">
  <p>The <code>hrms_api</code> module delivers a high-performance REST API powered by Django REST Framework, SimpleJWT bearer tokens, and Swagger UI.</p>
</div>
"""
})

# ==============================================================================
# CHAPTER 17: AUTHENTICATION, SECURITY & PERMISSIONS
# ==============================================================================
CHAPTERS.append({
    "num": 17,
    "id": "auth-security-permissions",
    "title": "Enterprise Authentication, RBAC & Security (`hrms_auth`, `base`)",
    "subtitle": "Custom user models, role-based access control (RBAC), two-factor authentication (2FA), and session protection.",
    "content_md": """
## 17.1 Overview & Responsibilities

HRMS implements enterprise-grade identity and access governance via `hrms_auth`. It supports username or corporate email login, multi-company role assignments, TOTP two-factor authentication, forced password rotation, and active session protection.

---

## 17.2 Database Models & User Architecture

- `HRMSUser`: Primary authentication model extending `AbstractUser`. Attributes: `email` (unique index), `username`, `phone`, `is_verified`, `two_factor_enabled`, `force_password_change`, `company` (FK).
- `LegacyUser`: Migration bridge preserving backward compatibility with legacy authentication systems.
- `AuthUserGroups` & `AuthUserUserPermissions`: Scoped permission mappings associating users with granular roles within their specific operating company.

---

## 17.3 Security Defenses & Hardening

1. **Two-Factor Authentication (2FA)**: Generates standard TOTP secrets compatible with Google Authenticator or Microsoft Authenticator. Mandatory for payroll and administrative roles.
2. **Brute Force Protection**: Failed login tracking locks accounts after configurable attempts, logging the event in `hrms_audit.AccountBlockUnblock`.
3. **SVG & File Sanitization**: `SVGSecurityMiddleware` strips executable scripts from XML-based image files to eliminate SVG XSS vectors.
4. **Session Expiry & CSRF**: Secure, HTTP-only session cookies with strict SameSite attributes and mandatory CSRF token verification on all POST/PUT/DELETE requests.
""",
    "content_html": """
<div class="chapter-content">
  <p>The <code>hrms_auth</code> module delivers robust security with custom user authentication, TOTP 2FA, brute-force defense, and scoped RBAC permissions.</p>
</div>
"""
})

# ==============================================================================
# CHAPTER 18: AUDIT TRAILS & COMPLIANCE
# ==============================================================================
CHAPTERS.append({
    "num": 18,
    "id": "audit-compliance",
    "title": "Audit Trails & Regulatory Compliance (`hrms_audit`)",
    "subtitle": "Complete changelog tracking, field-level diffs, audit tags, and user block/unblock logs via django-auditlog.",
    "content_md": """
## 18.1 Overview & Responsibilities

The `hrms_audit` application provides complete regulatory compliance and non-repudiation tracking. Integrated with `django-auditlog` and `simple_history`, every data modification across sensitive entities (contracts, wages, employee records, attendance punches, and leave approvals) is archived with timestamps, user IDs, IP addresses, and before-and-after diffs.

---

## 18.2 Database Models Specification

| Model Name | Purpose | Primary Attributes & Relationships |
|---|---|---|
| `HRMSAuditLog` | Master changelog recording entity state mutations. | `content_type`, `object_id`, `actor` (FK to User), `action` (Create/Update/Delete), `changes_json`, `timestamp`, `ip_address` |
| `HRMSAuditInfo` | Operational classification and context attached to audit entries. | `audit_log` (FK), `module_name`, `severity` (Low/Medium/High/Critical), `action_description` |
| `AuditTag` | Categorical tags (e.g. "Salary Revision", "Manual Attendance Punch", "Security Alert"). | `tag_name`, `color_code` |
| `HistoryTrackingFields` | Dynamic configuration specifying which model fields trigger audit tracking. | `model_name`, `tracked_fields_list`, `is_active` |
| `AccountBlockUnblock` | Audit records of user accounts locked due to failed logins or admin actions. | `user` (FK), `action` (Blocked/Unblocked), `reason`, `action_by` (FK), `timestamp` |
""",
    "content_html": """
<div class="chapter-content">
  <p>The <code>hrms_audit</code> application ensures end-to-end accountability through detailed change logs, JSON field diffs, and security event records.</p>
</div>
"""
})

# ==============================================================================
# CHAPTER 19: AUTOMATIONS, NOTIFICATIONS & BACKGROUND TASKS
# ==============================================================================
CHAPTERS.append({
    "num": 19,
    "id": "automations-notifications",
    "title": "Automations, Notifications & Scheduled Tasks (`hrms_automations`, `notifications`)",
    "subtitle": "Event-driven email automations, background cron processing via APScheduler, and real-time in-app alerts.",
    "content_md": """
## 19.1 Overview & Responsibilities

The `hrms_automations` and `notifications` modules eliminate manual overhead through event triggers, automated notifications, and scheduled background tasks.

---

## 19.2 Database Models & Features

- `MailAutomation`: Event-driven rules linking system triggers (e.g. On Employee Creation, Contract Expiration, Birthday, Work Anniversary) to dynamic HTML mail templates.
- `Notification`: In-app notification center recording alerts, approval requests, and announcements with unread counter badges.
- `django-apscheduler`: Background task scheduler executing recurring operations:
  - Daily attendance aggregation and hours compilation.
  - Nightly contract expiration scans with warning alerts to HR.
  - Scheduled automated monthly payroll batch runs.
  - Periodic database backups and cloud sync.
""",
    "content_html": """
<div class="chapter-content">
  <p>Event-driven mail automations, scheduled background cron tasks, and real-time in-app alerts keep employees and managers continuously informed.</p>
</div>
"""
})

# ==============================================================================
# CHAPTER 20: DOCUMENTS & DATABASE TEMPLATES
# ==============================================================================
CHAPTERS.append({
    "num": 20,
    "id": "documents-templates",
    "title": "Document Generation & Database Templates (`hrms_documents`, `hrms_dbtemplate`)",
    "subtitle": "Dynamic rich-text letter templates, merge tags, document requests, and automated PDF letter generation.",
    "content_md": """
## 20.1 Overview & Responsibilities

The `hrms_documents` and `hrms_dbtemplate` applications automate the authoring and issuance of corporate letters, agreements, and certificates.

---

## 20.2 Database Models & Features

- `Template` & `TemplateVersion`: Rich-text letter templates (Offer Letters, Experience Certificates, Non-Disclosure Agreements, Salary Certificates) with version control.
- **Dynamic Merge Variables**: Placeholders such as `{{employee_name}}`, `{{job_title}}`, `{{company_name}}`, and `{{salary_ctc}}` are interpolated with live database values at runtime.
- `DocumentRequest`: Employee self-service requests for formal letters, approval workflow, automated PDF generation, and archive downloads.
""",
    "content_html": """
<div class="chapter-content">
  <p>Dynamic rich-text letter templates with merge tags enable instantaneous, automated generation of official HR letters and certificates.</p>
</div>
"""
})

# ==============================================================================
# CHAPTER 21: DATABASE BACKUP & DISASTER RECOVERY
# ==============================================================================
CHAPTERS.append({
    "num": 21,
    "id": "backup-disaster-recovery",
    "title": "Database Backup & Disaster Recovery (`hrms_backup`, `pg_backup`)",
    "subtitle": "Automated and on-demand PostgreSQL database dumps, local encryption, and Google Drive cloud archives.",
    "content_md": """
## 21.1 Overview & Responsibilities

The `hrms_backup` and `pg_backup` applications provide data protection and disaster recovery for PostgreSQL databases.

---

## 21.2 Features & Models

- `LocalBackup`: Automated or manual execution of PostgreSQL `pg_dump` snapshots stored in timestamped, encrypted local volumes.
- `GoogleDriveBackup`: Remote off-site backup synchronization utilizing Google Drive API service credentials.
- **One-Click Restoration**: Web-based database restoration interface with automated connection termination and integrity checks.
""",
    "content_html": """
<div class="chapter-content">
  <p>Automated PostgreSQL database snapshots, local archives, and Google Drive off-site synchronization guarantee complete business continuity.</p>
</div>
"""
})

# ==============================================================================
# CHAPTER 22: EXTERNAL ENTERPRISE INTEGRATIONS
# ==============================================================================
CHAPTERS.append({
    "num": 22,
    "id": "external-integrations",
    "title": "External Enterprise Integrations (WhatsApp, LDAP, Outlook, Meet)",
    "subtitle": "WhatsApp Business API messaging, Active Directory LDAP directory sync, Microsoft Outlook SSO, and Google Meet.",
    "content_md": """
## 22.1 WhatsApp Business Integration (`whatsapp`)
- **Models**: `WhatsappCredientials`, `WhatsappFlowDetails`.
- **Functionality**: Integrates with the Meta WhatsApp Business API to dispatch instant transactional alerts (shift assignment notices, interview confirmations, leave request updates).

## 22.2 Enterprise Directory / LDAP Synchronization (`hrms_ldap`)
- **Models**: `LDAPSettings`.
- **Functionality**: Binds to corporate Active Directory or OpenLDAP servers for centralized authentication, user account provisioning, and group-to-role mappings.

## 22.3 Microsoft Outlook OAuth Single Sign-On (`outlook_auth`)
- **Models**: `AzureApi`.
- **Functionality**: Implements Microsoft Entra ID (Azure AD) OAuth 2.0 Single Sign-On, enabling enterprise users to authenticate with corporate Microsoft 365 accounts.

## 22.4 HRMS Meet Video Conferencing (`hrms_meet`)
- **Models**: `GoogleCloudCredential`, `GoogleCredential`, `GoogleMeeting`.
- **Functionality**: Integrates with Google Workspace APIs to generate Google Meet interview video rooms automatically upon interview scheduling.
""",
    "content_html": """
<div class="chapter-content">
  <p>Extensible enterprise connectors integrate HRMS with WhatsApp Business, Active Directory LDAP, Microsoft Entra ID SSO, and Google Meet.</p>
</div>
"""
})

# ==============================================================================
# CHAPTER 23: UI/UX, THEMES, TOURS & ACCESSIBILITY
# ==============================================================================
CHAPTERS.append({
    "num": 23,
    "id": "ui-ux-accessibility",
    "title": "UI/UX, Dynamic Themes, Guided Tours & Accessibility",
    "subtitle": "White-label theme engine, WCAG accessibility controls, interactive product tours, dynamic fields, and widgets.",
    "content_md": """
## 23.1 Dynamic Theme Engine (`hrms_theme`)
- **Models**: `HRMSColorTheme`, `CompanyTheme`.
- **Functionality**: Dynamic white-label branding allowing each corporate tenant to upload logos, select primary/secondary brand palettes, and style the navigation sidebar.

## 23.2 WCAG Accessibility (`accessibility`)
- **Models**: `DefaultAccessibility`.
- **Functionality**: Built-in accessibility toolset offering high-contrast color modes, text resizing, and OpenDyslexic font toggles for inclusive usability.

## 23.3 Interactive Guided Tours (`hrms_tour`)
- **Models**: `Tour`, `TourStep`, `TourProgress`.
- **Functionality**: Interactive, step-by-step walkthroughs powered by `tourController.js` that guide newly provisioned employees and managers through features.

## 23.4 Dynamic Fields Engine (`dynamic_fields`)
- **Models**: `Choice`, `DynamicField`.
- **Functionality**: Allows administrators to attach custom attributes (text, number, date, dropdowns) to core models at runtime without writing migrations.

## 23.5 Dynamic Views & Widgets (`hrms_views`, `hrms_widgets`, `hrms_crumbs`)
- Configurable table columns, drag-and-drop column orders, saved search filters, customizable dashboard widgets, and breadcrumb trails.
""",
    "content_html": """
<div class="chapter-content">
  <p>HRMS delivers a responsive, accessible, and white-labelable user experience equipped with interactive onboarding tours and dynamic custom fields.</p>
</div>
"""
})

# ==============================================================================
# CHAPTER 24: DEVOPS, DOCKER & DEPLOYMENT
# ==============================================================================
CHAPTERS.append({
    "num": 24,
    "id": "devops-deployment",
    "title": "DevOps, Containerization & Production Deployment",
    "subtitle": "Docker multi-stage builds, Docker Compose, Nginx reverse proxy, PostgreSQL, health probes, and CI/CD.",
    "content_md": """
## 24.1 Container Architecture & Multi-Stage Dockerfile

The HRMS container build leverages a hardened, multi-stage Debian-based Python 3.12 environment with essential system libraries for OpenCV (face detection), WeasyPrint (PDF generation), PostgreSQL client libraries, and LDAP development tools:

```dockerfile
# Multi-stage production build summary
FROM python:3.12-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev libldap2-dev libsasl2-dev ...
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```

---

## 24.2 Docker Compose Configuration

### 1. Development Stack (`docker-compose.yml`)
- Binds project source code directly into `/app/` for live hot-reloading.
- Runs PostgreSQL 16 on port 5432 and Redis 7 on port 6379.
- Exposes web service at `http://127.0.0.1:8080`.

### 2. Production Stack (`docker-compose.prod.yml`)
- Deploys Nginx as the front-facing reverse proxy handling TLS and static file delivery.
- Runs Gunicorn with multiple worker processes.
- Mounts persistent Docker volumes (`postgres_data`, `redis_data`, `media_volume`).

---

## 24.3 Health Probes & Monitoring

The system exposes two dedicated endpoints in `hrms/urls.py`:
- `/health/`: Cheap liveness probe verifying that the application process is alive (used by Docker HEALTHCHECK).
- `/ready/`: Deep readiness probe verifying active connectivity to PostgreSQL and Redis cache read/write capability before routing traffic.

---

## 24.4 Continuous Integration & GitHub Actions

Automated CI/CD workflows under `.github/workflows/` execute on every push:
1. **Linting & Code Style**: Enforces PEP 8 standards with Flake8 and Black.
2. **Unit & Integration Tests**: Runs Django test suites across core applications.
3. **Container Build Verification**: Verifies clean Docker container packaging and health probe responses.
""",
    "content_html": """
<div class="chapter-content">
  <p>Production deployment is streamlined through Docker Compose, Nginx reverse proxying, Gunicorn WSGI workers, PostgreSQL 16, Redis 7, and automated health checks.</p>
</div>
"""
})

print(f"Loaded {len(CHAPTERS)} complete chapters.")

# ==============================================================================
# BUILD MARKDOWN DOCUMENT
# ==============================================================================
def build_markdown(filepath):
    print(f"Writing Markdown documentation to {filepath}...")
    lines = []
    lines.append("# HRMS — Human Resource Management System")
    lines.append("## Complete System Architecture & Operational Documentation")
    lines.append("")
    lines.append(f"**Publication Date:** {datetime.datetime.now().strftime('%B %d, %Y')}")
    lines.append("**System Version:** 2.0.0 Enterprise")
    lines.append("**Repository:** [shawn-cse/hrms](https://github.com/shawn-cse/hrms)")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Table of Contents")
    lines.append("")
    for ch in CHAPTERS:
        lines.append(f"{ch['num']}. [{ch['title']}](#chapter-{ch['num']}-{ch['id']})")
    lines.append("")
    lines.append("---")
    lines.append("")

    for ch in CHAPTERS:
        lines.append(f"# Chapter {ch['num']}: {ch['title']} <a id='chapter-{ch['num']}-{ch['id']}'></a>")
        lines.append(f"*{ch['subtitle']}*")
        lines.append("")
        lines.append(ch['content_md'].strip())
        lines.append("")
        lines.append("---")
        lines.append("")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[OK] Markdown file written successfully: {os.path.getsize(filepath):,} bytes")

# ==============================================================================
# BUILD PRINT-OPTIMIZED HTML DOCUMENT
# ==============================================================================
def build_html(filepath):
    print(f"Writing Print-Optimized HTML to {filepath}...")
    
    html_out = []
    html_out.append("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>HRMS — Complete System Documentation</title>
<style>
  @page {
    size: A4;
    margin: 18mm 14mm 18mm 14mm;
    @top-right {
      content: "HRMS System Documentation";
      font-size: 8pt;
      color: #64748b;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    @bottom-right {
      content: "Page " counter(page);
      font-size: 8pt;
      color: #64748b;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
  }

  *, *:before, *:after {
    box-sizing: border-box;
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.55;
    color: #1e293b;
    background-color: #ffffff;
    margin: 0;
    padding: 0;
  }

  /* COVER PAGE */
  .cover-page {
    page-break-after: always;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 90vh;
    text-align: center;
    padding: 40px 20px;
  }

  .cover-badge {
    display: inline-block;
    background: #e0e7ff;
    color: #3730a3;
    font-size: 11pt;
    font-weight: 700;
    padding: 6px 18px;
    border-radius: 9999px;
    margin-bottom: 24px;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  .cover-title {
    font-size: 34pt;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.15;
    margin: 0 0 16px 0;
  }

  .cover-subtitle {
    font-size: 15pt;
    font-weight: 400;
    color: #475569;
    max-width: 680px;
    margin: 0 0 40px 0;
    line-height: 1.4;
  }

  .cover-divider {
    width: 100px;
    height: 4px;
    background: linear-gradient(90deg, #2563eb, #3b82f6);
    border-radius: 2px;
    margin: 0 0 40px 0;
  }

  .cover-meta {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    width: 100%;
    max-width: 720px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 20px;
    text-align: left;
  }

  .meta-item strong {
    display: block;
    font-size: 9pt;
    text-transform: uppercase;
    color: #64748b;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
  }

  .meta-item span {
    font-size: 11pt;
    font-weight: 600;
    color: #0f172a;
  }

  /* TABLE OF CONTENTS */
  .toc-page {
    page-break-after: always;
    padding-top: 20px;
  }

  .toc-header {
    font-size: 22pt;
    font-weight: 800;
    color: #0f172a;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 12px;
    margin-bottom: 24px;
  }

  .toc-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px 24px;
  }

  .toc-item {
    display: flex;
    align-items: baseline;
    font-size: 9.5pt;
    padding: 4px 0;
    border-bottom: 1px dotted #cbd5e1;
  }

  .toc-number {
    font-weight: 700;
    color: #2563eb;
    min-width: 24px;
  }

  .toc-title {
    color: #1e293b;
    font-weight: 500;
  }

  /* CHAPTER STYLING */
  .chapter-block {
    page-break-before: always;
    padding-top: 10px;
  }

  .chapter-header {
    margin-bottom: 20px;
    border-bottom: 2px solid #2563eb;
    padding-bottom: 10px;
  }

  .chapter-num {
    font-size: 10pt;
    font-weight: 700;
    color: #2563eb;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 4px;
  }

  .chapter-title {
    font-size: 18pt;
    font-weight: 800;
    color: #0f172a;
    margin: 0 0 6px 0;
    line-height: 1.25;
  }

  .chapter-subtitle {
    font-size: 10pt;
    color: #64748b;
    font-style: italic;
    margin: 0;
  }

  h2 {
    font-size: 13pt;
    font-weight: 700;
    color: #1e3a8a;
    margin: 22px 0 10px 0;
    border-left: 3px solid #2563eb;
    padding-left: 8px;
    page-break-after: avoid;
  }

  h3 {
    font-size: 11pt;
    font-weight: 700;
    color: #0f172a;
    margin: 16px 0 8px 0;
    page-break-after: avoid;
  }

  p {
    margin: 0 0 10px 0;
    text-align: justify;
  }

  /* DATA TABLES */
  table, .data-table {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0 16px 0;
    font-size: 8.5pt;
    page-break-inside: avoid;
  }

  table th, .data-table th, table td, .data-table td {
    padding: 7px 10px;
    border: 1px solid #cbd5e1;
    text-align: left;
    vertical-align: top;
  }

  table th, .data-table th {
    background-color: #f1f5f9;
    color: #0f172a;
    font-weight: 700;
  }

  table tr:nth-child(even), .data-table tr:nth-child(even) {
    background-color: #f8fafc;
  }

  code {
    font-family: Consolas, Monaco, "Courier New", monospace;
    font-size: 8.5pt;
    background: #f1f5f9;
    color: #0f172a;
    padding: 2px 4px;
    border-radius: 4px;
    border: 1px solid #e2e8f0;
  }

  pre {
    background: #0f172a;
    color: #f8fafc;
    padding: 12px;
    border-radius: 6px;
    font-family: Consolas, Monaco, "Courier New", monospace;
    font-size: 8pt;
    line-height: 1.45;
    overflow-x: auto;
    margin: 12px 0;
    page-break-inside: avoid;
  }

  pre code {
    background: transparent;
    color: inherit;
    border: none;
    padding: 0;
  }

  /* CALLOUTS */
  .callout {
    border-left: 4px solid #2563eb;
    background: #eff6ff;
    padding: 12px 16px;
    border-radius: 0 6px 6px 0;
    margin: 14px 0;
    page-break-inside: avoid;
  }

  .callout-warning {
    border-left-color: #f59e0b;
    background: #fffbeb;
  }

  .callout-info {
    border-left-color: #0284c7;
    background: #f0f9ff;
  }

  .callout h4 {
    margin: 0 0 6px 0;
    font-size: 9.5pt;
    font-weight: 700;
    color: #0f172a;
  }

  .callout p {
    margin: 0;
    font-size: 9pt;
  }

  /* ARCH DIAGRAM */
  .arch-diagram {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 16px;
    margin: 16px 0;
    page-break-inside: avoid;
  }

  .arch-col {
    flex: 1;
  }

  .arch-arrow {
    padding: 0 10px;
    font-size: 16pt;
    color: #94a3b8;
  }

  .arch-box {
    padding: 12px;
    border-radius: 6px;
    font-size: 8pt;
    line-height: 1.35;
  }

  .arch-box strong {
    display: block;
    font-size: 9pt;
    margin-bottom: 6px;
  }

  .arch-box span {
    display: block;
    margin-bottom: 3px;
  }

  .box-primary {
    background: #e0e7ff;
    border: 1px solid #c7d2fe;
    color: #312e81;
  }

  .box-accent {
    background: #e0f2fe;
    border: 1px solid #bae6fd;
    color: #0c4a6e;
  }

  .box-dark {
    background: #f1f5f9;
    border: 1px solid #cbd5e1;
    color: #0f172a;
  }

  .box-success {
    background: #dcfce7;
    border: 1px solid #bbf7d0;
    color: #14532d;
  }

  /* FEATURE GRID */
  .feature-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin: 14px 0;
    page-break-inside: avoid;
  }

  .feature-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 12px;
  }

  .feature-card h4 {
    margin: 0 0 6px 0;
    font-size: 9.5pt;
    color: #1e3a8a;
  }

  .feature-card p {
    margin: 0;
    font-size: 8.5pt;
    color: #475569;
  }
</style>
</head>
<body>
""")

    # Cover Page
    html_out.append(f"""
<div class="cover-page">
  <div class="cover-badge">Enterprise Human Resource Management System</div>
  <h1 class="cover-title">HRMS System Documentation</h1>
  <p class="cover-subtitle">Complete Architecture, Data Models, Workflows, APIs, and Operational Reference for the Entire Application Suite</p>
  <div class="cover-divider"></div>
  <div class="cover-meta">
    <div class="meta-item">
      <strong>Application Version</strong>
      <span>v2.0.0 Enterprise</span>
    </div>
    <div class="meta-item">
      <strong>Published Date</strong>
      <span>{datetime.datetime.now().strftime('%B %d, %Y')}</span>
    </div>
    <div class="meta-item">
      <strong>Core Stack</strong>
      <span>Django 5.x / PostgreSQL 16</span>
    </div>
    <div class="meta-item">
      <strong>Scope</strong>
      <span>30+ Modules Covered</span>
    </div>
    <div class="meta-item">
      <strong>Architecture</strong>
      <span>Docker-First / Modular</span>
    </div>
    <div class="meta-item">
      <strong>Repository</strong>
      <span>shawn-cse/hrms</span>
    </div>
  </div>
</div>
""")

    # Table of Contents
    html_out.append("""
<div class="toc-page">
  <div class="toc-header">Table of Contents</div>
  <div class="toc-grid">
""")
    for ch in CHAPTERS:
        html_out.append(f"""
    <div class="toc-item">
      <span class="toc-number">{ch['num']}.</span>
      <span class="toc-title">{ch['title']}</span>
    </div>
""")
    html_out.append("""
  </div>
</div>
""")

    import markdown

    # Chapters
    for ch in CHAPTERS:
        # Convert full markdown content to styled HTML
        parsed_body = markdown.markdown(ch['content_md'], extensions=['tables', 'fenced_code'])
        # If there's an extra custom diagram/component, include it
        extra = ch.get('extra_html', '')

        html_out.append(f"""
<div class="chapter-block">
  <div class="chapter-header">
    <div class="chapter-num">Chapter {ch['num']}</div>
    <h1 class="chapter-title">{ch['title']}</h1>
    <div class="chapter-subtitle">{ch['subtitle']}</div>
  </div>
  <div class="chapter-content">
    {extra}
    {parsed_body}
  </div>
</div>
""")

    html_out.append("</body></html>")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("".join(html_out))
    print(f"[OK] HTML print document written: {os.path.getsize(filepath):,} bytes")

# ==============================================================================
# COMPILE PDF VIA HEADLESS CHROME
# ==============================================================================
def compile_pdf(html_path, pdf_path):
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if not os.path.exists(chrome_path):
        chrome_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

    print(f"Compiling PDF with browser engine: {chrome_path}...")
    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 1000:
        print(f"[SUCCESS] PDF compiled: {pdf_path} ({os.path.getsize(pdf_path):,} bytes)")
        return True
    else:
        print(f"[ERROR] PDF compilation failed. Error: {res.stderr}")
        return False

# ==============================================================================
# MAIN RUNNER
# ==============================================================================
if __name__ == "__main__":
    build_markdown(MD_PATH)
    build_html(HTML_PATH)
    success = compile_pdf(HTML_PATH, PDF_PATH)
    print("\nDocumentation build cycle completed.")
