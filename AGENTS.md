# Asistente de Recomendación Farmacéutica — Instrucciones para Agentes

Instrucciones para agentes IA y desarrolladores. El proyecto tiene **frontend** (`frontend/`) y **backend** (`backend/`), cada uno con su stack y convenciones. Usa la sección que corresponda al código que estés modificando.

---

## Frontend

El front se desarrolla en **`frontend/`**. Comunicación con el backend vía REST API.

### Stack

React + TypeScript + Vite + Tailwind CSS v4 + Vitest + Playwright + React Router

- **Comunicación con backend**: REST API (cliente HTTP). Hasta que exista backend, se usan **mocks** con la misma interfaz.

### TDD — OBLIGATORIO

1. Escribir el **test primero** → ejecutar → debe **fallar**.
2. Implementar el **mínimo código** para que pase.
3. Refactorizar manteniendo los tests en verde.

No implementar funcionalidad sin test que la cubra (salvo configuración o andamiaje acordado).

### Organización de archivos (Scope Rule)

- `src/shared/` → usado por varias features (tipos, utils, constantes, componentes, hooks).
- `src/features/X/` → específico de una feature (auth, case-input, recommendations).
- `src/context/` → estado global (Auth). Si se añade contexto de “caso”, mismo criterio.
- `src/api/` → cliente HTTP, mocks y configuración de base URL.

### Estructura del proyecto

```
frontend/
├── src/
│   ├── shared/{types,utils,constants,components,hooks}/
│   ├── features/
│   │   ├── auth/
│   │   ├── case-input/
│   │   └── recommendations/
│   ├── context/          # Auth: 3 archivos (ver más abajo)
│   ├── api/              # mocks + cliente HTTP
│   └── test/setup.ts     # si se usa
├── e2e/
│   ├── pages/            # Page Objects (LoginPage, DashboardPage)
│   └── *.spec.ts
└── .husky/               # opcional: pre-commit, pre-push
```

### Configuraciones importantes

### tsconfig.app.json

Excluir los tests del build de producción:

```json
{ "exclude": ["src/**/*.test.ts", "src/**/*.test.tsx", "src/test/**"] }
```

### react-refresh: Context en 3 archivos

Si se usa Context API (p. ej. Auth), separar en **3 archivos** para evitar problemas con react-refresh:

```
src/context/
├── AuthContextValue.ts   # createContext + tipos (sin componentes)
├── AuthContext.tsx       # solo exporta AuthProvider
└── useAuth.ts            # solo exporta useAuth()
```

No usar el workaround de `allowExportNames`.

### Husky

Si se usa Husky: ejecutar **git init** antes de **husky init**.

### Scripts

- `pnpm dev` — servidor de desarrollo.
- `pnpm build` — build de producción.
- `pnpm test` / `pnpm test:run` — tests unitarios/integración (Vitest).
- `pnpm test:e2e` — tests E2E (Playwright).
- `pnpm lint` — ESLint.
- `pnpm typecheck` — comprobación de tipos (tsc --noEmit).
- `pnpm quality` — lint + typecheck + test:run.
- `pnpm verify` — quality + test:e2e + build.

### Plan de desarrollo (entregables)

El plan detallado está en **`docs/front/Plan Front Ph/`**. Resumen por tarea:

| Tarea | Contenido principal |
| ----- | ------------------- |
| 01 | Setup: Vite, React, TS, Tailwind v4, Vitest, React Router, estructura de carpetas |
| 02 | Login, AuthContext (3 archivos), rutas protegidas, mock de auth |
| 03 | Introducción del caso: textarea + "Analizar caso", mock de análisis |
| 04 | Información estructurada editable (edad, sexo, síntomas, hipótesis) |
| 05 | Botón "Confirmar caso y obtener recomendaciones", mock de recomendaciones |
| 06 | Vista de productos recomendados (cards, principal/alternativas, "Nuevo caso") |
| 07 | Cliente HTTP, sustitución de mocks por API real (cuando exista backend) |
| 08 | Playwright, Page Objects, E2E del flujo completo |
| 09 | ESLint, scripts quality/verify, refactors de calidad |

### Referencias del proyecto

- **Diseño funcional**: `docs/diseno/DIS-001-diseño.md`
- **Arquitectura**: `docs/adr/ADR-001-arquitectura.md`
- **UI y prototipo**: `docs/front/UI/`, `docs/front/UI/src/imports/pharmacy-assistant-interface.md`
- **Contexto y prompts del plan**: `docs/front/Plan Front Ph/00-context-prompt.md`

### Reglas de frontend

- **Idioma**: interfaz en **español**.
- **Sin lógica de negocio**: el front solo consume la API; no contiene reglas de recomendación ni de análisis clínico.
- **Mocks**: hasta que exista backend, los servicios (login, análisis, recomendaciones) se implementan con mocks; misma interfaz para poder sustituirlos por HTTP en la tarea 07.
- **UX**: flujo paso a paso, claro; no mencionar “IA” en la UI; estilo software profesional sanitario.

### Validación

`pnpm verify` debe pasar: 0 errores de lint, 0 errores de tipos, todos los tests verdes, build correcta.

---

## Backend

El backend se desarrolla en **`backend/`**. Expone API REST consumida por el frontend. Sigue **Clean Architecture** y **TDD**. La persistencia es parametrizable: por defecto **en memoria** (repositorios in-memory); después se puede cambiar a **PostgreSQL** sin tocar la lógica de negocio.

### Stack

- **Python 3.11+**
- **FastAPI** (framework HTTP)
- **Pydantic** (validación y DTOs)
- **pydantic-settings** (configuración)
- **structlog** o **loguru** (logging)
- **pytest** + **pytest-asyncio** (tests)
- **SQLAlchemy 2.0 async** + **asyncpg** (solo cuando se use persistencia PostgreSQL; ver video-04)

### TDD — OBLIGATORIO

1. Escribir el **test primero** → ejecutar → debe **fallar** (Red).
2. Implementar el **mínimo código** para que pase (Green).
3. Refactorizar manteniendo los tests en verde.

No implementar funcionalidad sin un test que la cubra (salvo configuración o andamiaje acordado).

### Organización (Clean Architecture)

- **`app/domain/`** — entidades, value objects, reglas de negocio, **interfaces de repositorios** (puertos). Sin dependencias de framework ni infra.
- **`app/application/`** — casos de uso, DTOs de aplicación, orquestación. Depende solo del dominio.
- **`app/infrastructure/`** — persistencia (repositorios in-memory o PostgreSQL), config, seguridad, LLM, logging. Implementa los puertos del dominio.
- **`app/interfaces/`** — API HTTP: rutas, schemas Pydantic, dependencias FastAPI. Depende de application y de las interfaces (no de implementaciones concretas).

Los casos de uso y la API reciben los repositorios por **inyección** (FastAPI Depends o factory); no conocen si la implementación es in-memory o PostgreSQL.

### Persistencia parametrizable

- Variable de configuración **`STORAGE_BACKEND`**: `memory` (por defecto) | `postgresql`.

### Estructura del proyecto (backend)

```
backend/
├── app/
│   ├── domain/           # entidades, interfaces de repositorios
│   ├── application/       # use cases, puertos
│   ├── infrastructure/    # config, persistence/memory/, db/ (PostgreSQL en video-04)
│   ├── interfaces/        # api (routes, schemas, dependencies)
│   └── main.py
├── tests/
├── pyproject.toml
└── .env.example           # STORAGE_BACKEND=memory, DATABASE_URL (para postgresql)
```

### Scripts

Desde la raíz **`backend/`**:

- `uvicorn app.main:app --reload` (o script `dev`/`run` si está definido) — servidor de desarrollo.
- `pytest` / `pytest -v` — tests.
- Opcional (video-09): `ruff check`, `mypy`, scripts `lint`, `typecheck`, `quality`.

### Plan de desarrollo (entregables)

El plan detallado está en **`docs/back/Plan Back Ph/`**. Resumen:

| Tarea | Contenido principal |
| ----- | ------------------- |
| 01 | Setup: FastAPI, pytest, Clean Architecture, persistencia en memoria, health |
| 02 | Dominio y DTOs (entidades, interfaces de repositorios) |
| 03 | Auth: login, hash, token/sesión |
| 04 | PostgreSQL: SQLAlchemy, modelos, migraciones, repositorios |
| 05 | Análisis de caso (endpoint, mock LLM) |
| 06 | Motor de recomendaciones (catálogo, stock, reglas) |
| 07 | Endpoint recomendaciones (principal + alternativas + explicación) |
| 08 | Integración LLM real |
| 09 | Calidad: ruff, mypy, scripts |

### Referencias del proyecto (backend)

- **Diseño funcional**: `docs/diseno/DIS-001-diseño.md`
- **Arquitectura**: `docs/adr/ADR-001-arquitectura.md`
- **Contexto y plan**: `docs/back/Plan Back Ph/00-context-prompt.md`, `docs/back/Plan Back Ph/00-overview.md`,

### Reglas de backend

- **Contratos**: DTOs y códigos HTTP alineados con lo que consume el frontend (login, análisis de caso, recomendaciones).
- **Seguridad**: contraseñas hasheadas; autenticación obligatoria en endpoints protegidos.
- **Idioma**: código y mensajes en inglés; documentación y mensajes de usuario pueden estar en español.

### Validación (backend)

- `pytest` (o `pytest -v`) debe pasar sin errores.
- Si están configurados: `ruff check`, `mypy` sin errores.
