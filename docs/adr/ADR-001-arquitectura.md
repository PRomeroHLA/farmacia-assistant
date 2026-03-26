# ADR-001: Arquitectura del sistema

# Arquitectura del Sistema — Resumen Operativo para Agente de IA

## 1. Propósito del sistema

Aplicación que asiste a farmacéuticos en la **recomendación de medicamentos** a partir de una **descripción libre de síntomas**.

El sistema:

1. Recibe un caso clínico en lenguaje natural.
2. Extrae información estructurada.
3. Permite validación humana.
4. Genera recomendaciones de medicamentos basadas en:
   - síntomas
   - reglas farmacológicas
   - disponibilidad en catálogo
   - stock.

El sistema **no sustituye al farmacéutico**, actúa como **herramienta de apoyo a la decisión**.

---

# 2. Arquitectura del sistema

## Estilo arquitectónico

**Monolito modular** compuesto por:

```
Frontend (SPA)
        │
        │ REST API
        ▼
Backend (Clean Architecture)
        │
        ├── Base de datos PostgreSQL
        └── Servicios externos LLM
```

Motivación:

- simplicidad operativa
- baja concurrencia (1-5 usuarios)
- despliegue sencillo
- MVP académico.

---

# 3. Stack tecnológico

## Backend

| Componente | Tecnología |
|---|---|
Lenguaje | Python |
Framework HTTP | FastAPI |
Validación | Pydantic |
ORM / acceso datos | SQLAlchemy 2.0 async o asyncpg |
Base de datos | PostgreSQL |
Logging | structlog o loguru |
DI | FastAPI Depends |
Testing | pytest + pytest-asyncio |

El backend expone una **API REST**.

---

## Frontend

SPA desarrollada con:

| Tecnología | Uso |
|---|---|
React | UI |
TypeScript | tipado |
Vite | bundler |
Tailwind CSS v4 | estilos |
Vitest | testing |
e2e | Playwright
Comunicación directa con backend mediante **REST API**.

---

# 4. Arquitectura interna del backend

El backend sigue **Clean Architecture** con las capas:

```
interfaces/
    controllers HTTP
    DTOs

application/
    use cases
    orchestration

domain/
    entities
    business rules

infrastructure/
    database
    external APIs
    LLM clients
```

Principios:

- independencia de frameworks
- alta testabilidad
- desacoplamiento de dependencias externas.

---

# 5. Componentes principales

## Frontend

Responsabilidades:

- login de usuario
- introducción del caso clínico
- visualización de datos estructurados
- edición y validación del caso
- visualización de recomendaciones.

No contiene lógica de negocio.

---

## Backend

Responsabilidades principales:

- autenticación
- procesamiento del caso clínico
- llamadas a LLM
- generación de estructura clínica
- generación de recomendaciones
- consulta del catálogo
- verificación de stock
- generación de respuesta final.

---

## Base de datos

PostgreSQL almacena:

- catálogo de medicamentos
- stock
- usuarios del sistema.

---

## Servicios externos

LLMs utilizados para:

- extracción de información estructurada + generación de hipótesis clínicas
- generación de explicaciones de recomendaciones.

El LLM **no contiene lógica de negocio**.

---

# 6. Flujo funcional principal

```
1 Usuario inicia sesión

2 Usuario introduce caso en texto libre

3 Frontend envía caso al backend

4 Backend
      └─ llama LLM → extraer estructura clínica

5 Backend devuelve datos estructurados

6 Usuario valida / corrige el caso

7 Backend selecciona medicamentos
      ├ reglas clínicas
      ├ catálogo
      ├ stock

8 Backend genera explicación

9 Frontend muestra recomendaciones
```

---

# 7. Motor de recomendación

Tipo: **híbrido**

Combina:

- reglas deterministas del dominio farmacéutico
- apoyo de IA para análisis y explicación.

Reglas obligatorias:

- incompatibilidad por edad
- embarazo
- alergias
- contraindicaciones
- disponibilidad en stock.

Salida:

```
máximo 5 medicamentos recomendados
```

---

# 8. Requisitos funcionales clave

El sistema debe permitir:

- introducir casos clínicos en lenguaje natural
- extraer estructura clínica
- editar y validar la estructura
- generar recomendaciones de medicamentos
- generar explicación textual de la recomendación.

---

# 9. Requisitos no funcionales

## Rendimiento

Objetivos:

```
análisis del caso        < 5 s
recomendaciones          < 5 s
respuesta final          < 2 s
```

---

## Seguridad

- autenticación obligatoria
- credenciales almacenadas con hash
- comunicaciones HTTPS.

---

## Mantenibilidad

Se garantiza mediante:

- Clean Architecture
- separación frontend/backend
- modularidad
- interfaces desacopladas.

---

# 10. Riesgos técnicos

## Dependencia de LLM

Mitigación:

- tratar LLM como dependencia externa
- timeouts
- control de errores
- posibilidad de cambiar proveedor.

---

## Latencia

Mitigación:

- limitar llamadas externas
- optimizar flujo.

---

## Recomendaciones incorrectas

Mitigación:

- validación humana obligatoria
- reglas deterministas
- control de catálogo y stock.

---

# 11. Evolución futura prevista

La arquitectura permite añadir:

- APIs externas farmacológicas
- nuevos modelos de IA
- nuevas reglas clínicas
- soporte multi-farmacia
- auditoría y analítica.

---

# 12. Suposiciones del entorno

Contexto del MVP:

- farmacia individual
- 1-5 usuarios concurrentes
- sin requerimientos de alta disponibilidad
- sin arquitectura distribuida.


---

# 14. Objetivo de este documento

Este documento contiene únicamente la información necesaria para que un **agente de IA o equipo de desarrollo** pueda:

- generar el **plan de desarrollo del sistema**
- definir la **estructura del repositorio**
- diseñar la **arquitectura del código**
- preparar el **despliegue del MVP**