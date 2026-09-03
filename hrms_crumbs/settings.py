from hrms.settings import TEMPLATES

TEMPLATES[0]["OPTIONS"]["context_processors"].append(
    "hrms_crumbs.context_processors.breadcrumbs",
)
