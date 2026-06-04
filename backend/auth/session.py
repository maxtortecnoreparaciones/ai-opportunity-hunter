"""Gestión de almacenamiento de sesión de navegador.

Guarda y carga el estado de Playwright (cookies, localStorage, sessionStorage)
para reutilizar sesiones autenticadas entre ejecuciones.
"""

import json
from pathlib import Path


SESSIONS_DIR = Path("data/sessions")


class SessionStorage:
    """Guarda/carga el storage state de Playwright en disco como JSON."""

    def __init__(self, platform: str):
        self.platform = platform.lower()
        SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
        self._path = SESSIONS_DIR / f"{self.platform}_session.json"

    @property
    def path(self) -> Path:
        return self._path

    def exists(self) -> bool:
        return self._path.exists()

    def save(self, storage_state: dict) -> None:
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(storage_state, f, indent=2, ensure_ascii=False)

    def load(self) -> dict | None:
        if not self.exists():
            return None
        with open(self._path, "r", encoding="utf-8") as f:
            return json.load(f)

    def delete(self) -> None:
        if self.exists():
            self._path.unlink()

    def info(self) -> dict:
        if not self.exists():
            return {"platform": self.platform, "has_session": False}
        data = self.load()
        n_cookies = len(data.get("cookies", []))
        origins = list(data.get("origins", []))
        return {
            "platform": self.platform,
            "has_session": True,
            "cookies": n_cookies,
            "origins": [o.get("origin", "") for o in origins],
            "file_size": self._path.stat().st_size,
        }
