"""Sistema de Autenticación Asistida con Navegador.

Permite al usuario iniciar sesión manualmente en plataformas de empleo
y reutilizar la sesión para búsquedas automatizadas posteriores.
"""

from .session import SessionStorage
from .authenticator import BaseAuthenticator
from .linkedin_auth import LinkedInAuthenticator
from .wellfound_auth import WellfoundAuthenticator
from .getonboard_auth import GetOnBoardAuthenticator

__all__ = [
    "SessionStorage",
    "BaseAuthenticator",
    "LinkedInAuthenticator",
    "WellfoundAuthenticator",
    "GetOnBoardAuthenticator",
]

PLATFORMS: dict[str, type[BaseAuthenticator]] = {
    "linkedin": LinkedInAuthenticator,
    "wellfound": WellfoundAuthenticator,
    "getonboard": GetOnBoardAuthenticator,
}
