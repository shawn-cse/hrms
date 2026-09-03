"""
Global template context for the tour engine.

Exposes a lightweight flag so the base template can render the "Help / Take a
tour" launcher (and an optional "pending" dot) without each page having to
know about tours. The heavy lifting — resolving which tour/steps apply — is
done lazily by the JS controller via the ``tour-active`` API.
"""

import logging

logger = logging.getLogger(__name__)


def pending_tours_flag(request):
    """Return launcher availability + whether the user has an unfinished tour."""
    return {"tour_launcher_enabled": False, "tour_has_pending": False}
