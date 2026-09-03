"""
hrms/inherit/

Extension infrastructure for HRMS — model field injection and CBV replacement.

Key public symbols re-exported here for convenience:

    from hrms.inherit import HRMSViewInheritMixin   # view extension
    from hrms.inherit import HRMSModelBase           # model metaclass
    from hrms.inherit import INJECTION_MAP              # migration routing
    from hrms.inherit import VIEW_REGISTRY              # registered views
"""

from hrms.inherit.extension_registry import INJECTION_MAP
from hrms.inherit.model_inherit import EXTENSION_REGISTRY, HRMSModelBase
from hrms.inherit.view_inherit import HRMSViewInheritMixin
from hrms.inherit.view_registry import VIEW_REGISTRY

__all__ = [
    "HRMSViewInheritMixin",
    "HRMSModelBase",
    "INJECTION_MAP",
    "EXTENSION_REGISTRY",
    "VIEW_REGISTRY",
]
