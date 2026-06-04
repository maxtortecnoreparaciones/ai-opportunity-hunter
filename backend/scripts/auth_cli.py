"""CLI de autenticación asistida para plataformas de empleo.

Uso:
    python -m backend.scripts.auth_cli login linkedin
    python -m backend.scripts.auth_cli login getonboard
    python -m backend.scripts.auth_cli status
    python -m backend.scripts.auth_cli delete linkedin
"""

import asyncio
import argparse
from backend.auth import PLATFORMS


def main():
    parser = argparse.ArgumentParser(description="Autenticación asistida con navegador")
    sub = parser.add_subparsers(dest="command", required=True)

    login_parser = sub.add_parser("login", help="Iniciar sesión en una plataforma")
    login_parser.add_argument("platform", choices=list(PLATFORMS.keys()), help="Plataforma objetivo")
    login_parser.add_argument("--headless", action="store_true", help="Modo sin interfaz gráfica")

    sub.add_parser("status", help="Ver estado de todas las sesiones")

    delete_parser = sub.add_parser("delete", help="Eliminar sesión guardada")
    delete_parser.add_argument("platform", choices=list(PLATFORMS.keys()), help="Plataforma")

    args = parser.parse_args()

    if args.command == "login":
        asyncio.run(_do_login(args.platform, args.headless))
    elif args.command == "status":
        _show_status()
    elif args.command == "delete":
        _do_delete(args.platform)


async def _do_login(platform: str, headless: bool = False):
    auth_cls = PLATFORMS[platform]
    auth = auth_cls()
    success = await auth.authenticate(headless=headless)
    if success:
        info = auth.session_info()
        print(f"  Sesión activa: {info['cookies']} cookies, {len(info['origins'])} dominios")


def _show_status():
    from backend.auth.session import SESSIONS_DIR, SessionStorage
    CHECK = "+"
    CROSS = "-"
    print()
    print("=== Estado de Sesiones ===")
    print()
    any_session = False
    for platform in PLATFORMS:
        s = SessionStorage(platform)
        info = s.info()
        if info["has_session"]:
            any_session = True
            print(f"  {CHECK} {platform.upper()}")
            print(f"      Cookies: {info['cookies']}")
            print(f"      Dominios: {', '.join(info['origins'][:3])}")
            print(f"      Archivo: {info['file_size']} bytes")
        else:
            print(f"  {CROSS} {platform.upper()}  - sin sesion guardada")
        print()

    sessions_dir = SESSIONS_DIR
    if sessions_dir.exists():
        files = list(sessions_dir.iterdir())
        profiles = [d for d in sessions_dir.iterdir() if d.is_dir()]
        print(f"  Directorio: {sessions_dir}")
        print(f"  Archivos de sesion: {[f.name for f in files if f.suffix == '.json']}")
        print(f"  Perfiles de navegador: {[p.name for p in profiles]}")

    if not any_session:
        print("  No hay sesiones guardadas. Usa: python -m backend.scripts.auth_cli login <plataforma>")


def _do_delete(platform: str):
    from backend.auth.session import SessionStorage
    s = SessionStorage(platform)
    s.delete()
    print(f"  Sesión de {platform} eliminada.")


if __name__ == "__main__":
    main()
