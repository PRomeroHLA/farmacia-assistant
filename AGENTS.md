# Asistente de Recomendación Farmacéutica — Instrucciones para el Frontend

Instrucciones para agentes IA y desarrolladores del **frontend** del Asistente de Farmacia. El front se desarrolla en la carpeta **`frontend/`** en la raíz del repositorio. Solo incluye instrucciones de frontend; el backend es independiente.

## Stack

React + TypeScript + Vite + Tailwind CSS v4 + Vitest + Playwright + React Router

- **Comunicación con backend**: REST API (cliente HTTP). Hasta que exista backend, se usan **mocks** con la misma interfaz.

## TDD — OBLIGATORIO

1. Escribir el **test primero** → ejecutar → debe **fallar**.
2. Implementar el **mínimo código** para que pase.
3. Refactorizar manteniendo los tests en verde.

No implementar funcionalidad sin test que la cubra (salvo configuración o andamiaje acordado).

## Organización de archivos (Scope Rule)

- `src/shared/` → usado por varias features (tipos, utils, constantes, componentes, hooks).
- `src/features/X/` → específico de una feature (auth, case-input, recommendations).
- `src/context/` → estado global (Auth). Si se añade contexto de “caso”, mismo criterio.
- `src/api/` → cliente HTTP, mocks y configuración de base URL.

## Estructura del proyecto (frontend)

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

## Configuraciones importantes

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

## Scripts

- `pnpm dev` — servidor de desarrollo.
- `pnpm build` — build de producción.
- `pnpm test` / `pnpm test:run` — tests unitarios/integración (Vitest).
- `pnpm test:e2e` — tests E2E (Playwright).
- `pnpm lint` — ESLint.
- `pnpm typecheck` — comprobación de tipos (tsc --noEmit).
- `pnpm quality` — lint + typecheck + test:run.
- `pnpm verify` — quality + test:e2e + build.

## Plan de desarrollo (entregables)

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

## Referencias del proyecto

- **Diseño funcional**: `docs/diseno/DIS-001-diseño.md`
- **Arquitectura**: `docs/adr/ADR-001-arquitectura.md`
- **UI y prototipo**: `docs/front/UI/`, `docs/front/UI/src/imports/pharmacy-assistant-interface.md`
- **Contexto y prompts del plan**: `docs/front/Plan Front Ph/00-context-prompt.md`

## Reglas de frontend

- **Idioma**: interfaz en **español**.
- **Sin lógica de negocio**: el front solo consume la API; no contiene reglas de recomendación ni de análisis clínico.
- **Mocks**: hasta que exista backend, los servicios (login, análisis, recomendaciones) se implementan con mocks; misma interfaz para poder sustituirlos por HTTP en la tarea 07.
- **UX**: flujo paso a paso, claro; no mencionar “IA” en la UI; estilo software profesional sanitario.

## Validación

`pnpm verify` debe pasar: 0 errores de lint, 0 errores de tipos, todos los tests verdes, build correcta.
