"""String sanitization helpers for demo catalogs and side fixtures."""

from __future__ import annotations

import logging
from pathlib import Path

from django.apps import apps
from django.db import transaction
from django.db.models import Q

from base.demo_data.catalog import STRING_REPLACEMENTS

logger = logging.getLogger(__name__)


def apply_replacements(text: str | None) -> str | None:
    if text is None:
        return None
    result = text
    for old, new in STRING_REPLACEMENTS:
        if old in result:
            result = result.replace(old, new)
    return result


def scrub_side_fixture_files(load_dir: Path) -> int:
    """
    Scrub vendor strings in side-load JSON fixtures (mail/FAQ) on disk.

    These files are not always loaded by load_demo_data but are imported from
    product UIs, so cleaning the source keeps demos consistent.
    """
    targets = (
        "mail_automations.json",
        "mail_templates.json",
        "faq.json",
        "faq_category.json",
        "tags.json",
    )
    scrubbed = 0
    for name in targets:
        path = load_dir / name
        if not path.exists():
            continue
        original = path.read_text(encoding="utf-8")
        updated = apply_replacements(original) or original
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            scrubbed += 1
            logger.info("Scrubbed side fixture: %s", name)
    return scrubbed


@transaction.atomic
def sanitize_loaded_records() -> dict[str, int]:
    """Rewrite informal / vendor-specific labels already loaded into the DB."""
    counts: dict[str, int] = {}

    # Leave restriction titles
    if apps.is_installed("leave"):
        from leave.models import RestrictLeave

        n = 0
        for row in RestrictLeave.objects.filter(
            Q(title__icontains="S/W")
            | Q(title__icontains="Odoo")
            | Q(title__icontains="Engineering.")
            | Q(title__icontains="Dept")
        ):
            new_title = apply_replacements(row.title) or row.title
            new_title = new_title.replace(
                "Engineering. Restriction", "Engineering Restriction"
            )
            new_title = new_title.replace("Engineering. ", "Engineering ")
            if new_title and new_title != row.title:
                row.title = new_title
                row.save(update_fields=["title"])
                n += 1
        counts["restrict_leave"] = n

    # Recruitment survey template + questions
    if apps.is_installed("recruitment"):
        from recruitment.models import RecruitmentSurvey, SurveyTemplate

        n = 0
        for tmpl in SurveyTemplate.objects.filter(
            Q(title__icontains="Odoo") | Q(description__icontains="Odoo")
        ):
            tmpl.title = apply_replacements(tmpl.title) or tmpl.title
            tmpl.description = apply_replacements(tmpl.description)
            # Prefer clean enterprise wording after generic replace
            if "the platform" in (tmpl.title or "").lower() or "Software Engineer" in (
                tmpl.title or ""
            ):
                tmpl.title = "Software Engineer Assessment"
                tmpl.description = (
                    "Structured interview assessment covering software engineering "
                    "fundamentals, backend development, and problem-solving skills."
                )
            tmpl.save()
            n += 1

        QUESTION_MAP = {
            "Have you worked with Odoo's ORM before ?": (
                "Have you worked with an ORM framework before?"
            ),
            "Which Odoo module have you worked on the most?": (
                "Which application modules have you worked on the most?"
            ),
            "Which of the following are key features of OdooÆs ORM?": (
                "Which of the following are key features of a modern ORM?"
            ),
            "Explain how you would customize an Odoo report for a client.": (
                "Explain how you would customize a business report for a client."
            ),
            "How many years of experience do you have working with Odoo?": (
                "How many years of professional software development experience do you have?"
            ),
            "Estimate your proficiency with Python in relation to Odoo development (0-100%).": (
                "Estimate your proficiency with Python (0-100%)."
            ),
            "Rate your experience in using Odoo Studio on a scale of 1 to 5.": (
                "Rate your experience with low-code customization tools on a scale of 1 to 5."
            ),
        }
        for survey in RecruitmentSurvey.objects.all():
            q = survey.question or ""
            new_q = QUESTION_MAP.get(q) or apply_replacements(q)
            if new_q and new_q != q:
                survey.question = new_q
                survey.save(update_fields=["question"])
                n += 1
        counts["recruitment_survey"] = n

    # Projects
    if apps.is_installed("project"):
        from project.models import Project

        n = 0
        for project in Project.objects.filter(
            Q(title__icontains="HRMS")
            | Q(description__icontains="HRMS")
            | Q(title__icontains="Odoo")
        ):
            project.title = apply_replacements(project.title) or project.title
            project.description = apply_replacements(project.description)
            if project.title == "Enterprise HR Platform" or "OpenSource" in (
                project.title or ""
            ):
                project.title = "Enterprise HR Platform"
                project.description = (
                    "Internal platform initiative to modernize HR workflows across "
                    "payroll, attendance, leave, and employee self-service."
                )
            project.save()
            n += 1
        counts["projects"] = n

    # PMS meetings / objectives with brand names
    if apps.is_installed("pms"):
        n = 0
        try:
            from pms.models import Meetings

            for meeting in Meetings.objects.filter(title__icontains="HRMS"):
                meeting.title = apply_replacements(meeting.title) or meeting.title
                meeting.save(update_fields=["title"])
                n += 1
        except Exception:
            pass
        try:
            from pms.models import EmployeeObjective, Objective

            for model in (Objective, EmployeeObjective):
                for obj in model.objects.filter(
                    Q(title__icontains="HRMS") | Q(title__icontains="Odoo")
                ):
                    obj.title = apply_replacements(obj.title) or obj.title
                    obj.save(update_fields=["title"])
                    n += 1
        except Exception:
            pass
        counts["pms"] = n

    # Employee & Candidate Bangladeshi phone and address standardization
    BD_ADDRESS_POOL = (
        ("House 12, Road 5, Dhanmondi", "Dhaka", "Dhaka", "1205"),
        ("Plot 24, Block D, Road 11, Banani", "Dhaka", "Dhaka", "1213"),
        ("House 45, Road 27, Gulshan-1", "Dhaka", "Dhaka", "1212"),
        ("House 8, Road 13, Sector 4, Uttara", "Dhaka", "Dhaka", "1230"),
        ("Holding 18, Road 2, Block B, Mirpur-10", "Dhaka", "Dhaka", "1216"),
        ("House 32, Road 3, Block C, Bashundhara R/A", "Dhaka", "Dhaka", "1229"),
        ("Level 6, 42 Dilkusha C/A, Motijheel", "Dhaka", "Dhaka", "1000"),
        ("Avenue 4, Road 7, Mirpur DOHS", "Dhaka", "Dhaka", "1216"),
        ("House 15, Road 1, Block A, Niketan, Gulshan-2", "Dhaka", "Dhaka", "1212"),
        ("House 22, Road 4, Sector 7, Uttara", "Dhaka", "Dhaka", "1230"),
        ("Plot 7, Main Road, Mohakhali C/A", "Dhaka", "Dhaka", "1212"),
        ("House 9, Road 8, Dhanmondi R/A", "Dhaka", "Dhaka", "1209"),
        ("Holding 54, Kazi Nazrul Islam Avenue, Kawran Bazar", "Dhaka", "Dhaka", "1215"),
        ("House 16, Road 6, Baridhara DOHS", "Dhaka", "Dhaka", "1206"),
        ("Plot 11, Road 2, Block F, Lalmatia", "Dhaka", "Dhaka", "1207"),
        ("House 28, Road 10, Sector 11, Uttara", "Dhaka", "Dhaka", "1230"),
        ("Flat 4B, 15 Panthapath", "Dhaka", "Dhaka", "1205"),
        ("House 7, Road 14, Block G, Banasree", "Dhaka", "Dhaka", "1219"),
        ("Holding 33, Boro Moghbazar", "Dhaka", "Dhaka", "1217"),
        ("House 19, Road 5, Block C, Khilgaon", "Dhaka", "Dhaka", "1219"),
        ("72 Agrabad Commercial Area", "Chattogram", "Chattogram", "4100"),
        ("House 14, Road 3, Nasirabad Housing Society", "Chattogram", "Chattogram", "4203"),
        ("Holding 88, GEC Circle, O.R. Nizam Road", "Chattogram", "Chattogram", "4000"),
        ("Plot 5, Block B, Chandgaon R/A", "Chattogram", "Chattogram", "4212"),
        ("House 21, Road 2, Panchlaish R/A", "Chattogram", "Chattogram", "4203"),
        ("Holding 45, Main Road, Zindabazar", "Sylhet", "Sylhet", "3100"),
        ("House 11, Road 4, Shahjalal Upashahar", "Sylhet", "Sylhet", "3100"),
        ("Holding 12, Station Road, Kumarpara", "Sylhet", "Sylhet", "3100"),
        ("Holding 34, Greater Road, Shaheb Bazar", "Rajshahi", "Rajshahi", "6000"),
        ("House 18, Road 1, Upashahar", "Rajshahi", "Rajshahi", "6202"),
        ("Holding 56, KDA Avenue, Shib Bari Mor", "Khulna", "Khulna", "9100"),
        ("House 25, Road 6, Sonadanga R/A", "Khulna", "Khulna", "9000"),
        ("Holding 82, Dhaka-Mymensingh Road, Board Bazar", "Gazipur", "Dhaka", "1704"),
        ("Plot 14, Sector 2, Joydebpur", "Gazipur", "Dhaka", "1700"),
        ("Holding 29, B.B. Road, Chasara", "Narayanganj", "Dhaka", "1400"),
    )
    PHONE_BD = "+8801700000000"

    if apps.is_installed("employee"):
        from employee.models import Employee

        n_emp = 0
        for idx, emp in enumerate(Employee._base_manager.all().order_by("id")):
            addr, city, state, zip_code = BD_ADDRESS_POOL[idx % len(BD_ADDRESS_POOL)]
            changed = False
            if emp.phone != PHONE_BD:
                emp.phone = PHONE_BD
                changed = True
            if emp.country != "Bangladesh":
                emp.country = "Bangladesh"
                changed = True
            if not emp.address or emp.country != "Bangladesh":
                emp.address = addr
                emp.city = city
                emp.state = state
                emp.zip = zip_code
                changed = True
            if emp.emergency_contact and not emp.emergency_contact.startswith("+880"):
                emp.emergency_contact = PHONE_BD
                changed = True
            if changed:
                emp.save(update_fields=["phone", "country", "address", "city", "state", "zip", "emergency_contact"])
                n_emp += 1
        counts["employees"] = n_emp

    if apps.is_installed("recruitment"):
        from recruitment.models import Candidate

        n_cand = 0
        for idx, cand in enumerate(Candidate.objects.all().order_by("id")):
            addr, city, state, zip_code = BD_ADDRESS_POOL[idx % len(BD_ADDRESS_POOL)]
            changed = False
            if cand.mobile != PHONE_BD:
                cand.mobile = PHONE_BD
                changed = True
            if cand.country != "Bangladesh":
                cand.country = "Bangladesh"
                changed = True
            if not cand.address or cand.country != "Bangladesh":
                cand.address = addr
                cand.city = city
                cand.state = state
                cand.zip = zip_code
                changed = True
            if changed:
                cand.save(update_fields=["mobile", "country", "address", "city", "state", "zip"])
                n_cand += 1
        counts["candidates"] = n_cand

    return counts
