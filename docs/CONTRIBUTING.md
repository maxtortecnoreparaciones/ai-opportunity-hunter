# Contribuyendo a AI Opportunity Hunter

## Flujo de trabajo

1. Revisa los issues abiertos en GitHub
2. Asigna un issue a tu nombre
3. Crea una rama desde `main`: `git checkout -b feat/nombre-corto`
4. Implementa los cambios
5. Ejecuta los tests: `pytest`
6. Crea un Pull Request a `main`

## Convenciones

### Commits
Usamos [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: agregar scraper de Wellfound
fix: corregir rate limiting en LinkedIn
docs: actualizar modelo de datos
test: agregar tests de scoring
refactor: extraer lógica de notificación
```

### Estilo de código

- Python: seguimos PEP 8
- Type hints obligatorios en todas las funciones
- Nombres de clases en PascalCase
- Nombres de funciones/métodos en snake_case
- Máximo 88 caracteres por línea

### Estructura de ramas

- `feat/*` — Nuevas funcionalidades
- `fix/*` — Correcciones de bugs
- `docs/*` — Cambios en documentación
- `test/*` — Agregar o modificar tests
- `refactor/*` — Refactorización de código

## Pull Requests

- Título descriptivo siguiendo conventional commits
- Descripción clara de qué cambia y por qué
- Referenciar el issue: `Closes #12`
- Incluir screenshots si aplica (notificaciones, etc.)

## Revisión

- 1 approval requerido para mergear
- Todos los checks (tests, lint) deben pasar
- No se permite mergear directamente a `main`

## Código de Conducta

Sé respetuoso. Esto es un proyecto educativo y profesional.
