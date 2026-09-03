# Contributing

1. Create a feature branch from the repository's active development branch.
2. Keep schema changes in Django migrations.
3. Run formatting/static checks used by CI.
4. Run `python manage.py check`, migration checks, and the relevant tests.
5. Do not commit `.env`, credentials, database dumps, uploaded personal data, or generated secrets.
