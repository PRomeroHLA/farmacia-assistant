# Diseño Funcional del Sistema — Resumen Operativo para Desarrollo

## 1. Propósito del MVP

Desarrollar un **asistente inteligente para farmacia** que ayude a recomendar medicamentos a partir de la **descripción libre de síntomas de un cliente**.

El sistema permite:

1. Introducir un caso clínico en lenguaje natural.
2. Extraer información clínica estructurada.
3. Validar manualmente el caso por el farmacéutico.
4. Generar recomendaciones de medicamentos.
5. Mostrar producto principal, alternativas y explicación.

El sistema **no sustituye al farmacéutico**.  
La **validación humana es obligatoria** antes de generar recomendaciones.

---

# 2. Arquitectura funcional del sistema

El sistema está compuesto por:

```
Frontend (SPA)
    - Interfaz de usuario
    - Introducción del caso
    - Edición del caso estructurado
    - Visualización de recomendaciones

Backend
    - Autenticación
    - Procesamiento del caso
    - Orquestación de LLM
    - Motor de recomendación
    - Consulta catálogo y stock
    - Generación de respuesta final

Base de datos
    - Catálogo de medicamentos
    - Stock
    - Usuarios

Servicios externos
    - Modelos de lenguaje (LLM)
```

El backend mantiene **toda la lógica de negocio**.

---

# 3. Flujo funcional principal

```
1 Usuario inicia sesión

2 Usuario introduce caso clínico en texto libre

3 Usuario inicia análisis del caso

4 Backend procesa el texto
      └ puede invocar LLM

5 Backend genera estructura clínica

6 Frontend muestra información estructurada editable

7 Usuario revisa y valida el caso

8 Backend analiza caso validado

9 Backend consulta catálogo y stock

10 Backend aplica reglas de exclusión

11 Backend prioriza medicamentos candidatos

12 Backend genera respuesta final

13 Frontend muestra:
      - medicamento recomendado
      - alternativas
      - explicación
```

---

# 4. Información clínica estructurada extraída

El sistema puede extraer del texto:

```
edad
sexo
embarazo
alergias
medicación actual
síntomas
duración de síntomas
intensidad
posibles cuadros clínicos orientativos
```

Los datos se presentan **editables para validación humana**.

---

# 5. Validación humana del caso

Antes de generar recomendaciones el usuario puede:

```
editar datos detectados
añadir síntomas
eliminar síntomas
modificar edad o condiciones
seleccionar hipótesis clínicas
añadir información adicional
```

El sistema **no puede continuar sin confirmación del usuario**.

---

# 6. Generación de recomendaciones

El backend analiza el caso validado mediante:

```
1 consulta del catálogo de medicamentos
2 verificación de stock
3 aplicación de reglas de exclusión
4 priorización de candidatos
```

### Reglas de exclusión

```
incompatibilidad por edad
embarazo
alergias
interacciones con medicación
productos sin stock
```

### Resultado

```
lista priorizada de medicamentos
máximo 3 productos por síntoma
```

---

# 7. Respuesta final generada

El backend construye la respuesta final:

```
producto recomendado principal
alternativas disponibles
explicación breve de la recomendación
```

El texto explicativo puede generarse usando **LLM externos**.

---

# 8. Funcionalidades incluidas en el MVP

El sistema incluye:

```
autenticación de usuarios
introducción de caso clínico
procesamiento del texto
extracción de información clínica
validación manual del caso
generación de recomendaciones
consulta de catálogo
verificación de stock
explicación textual de recomendación
visualización de resultados
```

---

# 9. Funcionalidades excluidas del MVP

No se incluye en esta versión:

```
aprendizaje automático continuo
optimización por rentabilidad
integración con APIs externas farmacológicas
historial clínico de clientes
soporte multi-farmacia
analítica avanzada
entrada por voz
integración con sistemas sanitarios
certificación clínica
```

---

# 10. Actores del sistema

## Actor primario

### Usuario de Farmacia

Responsabilidades:

```
iniciar sesión
introducir caso clínico
revisar información estructurada
editar datos
validar caso
consultar recomendaciones
```

---

## Actor secundario

### Proveedor externo de LLM

Responsabilidades:

```
procesar texto enviado por backend
extraer información estructurada
generar explicaciones textuales
```

Los LLM **no toman decisiones de negocio**.

---

# 11. Componentes internos del backend

## Procesamiento del caso

Responsable de:

```
analizar texto libre
extraer información clínica
generar hipótesis clínicas orientativas
invocar LLM cuando sea necesario
```

---

## Generador de recomendaciones

Responsable de:

```
analizar caso validado
consultar catálogo
verificar stock
aplicar reglas de exclusión
priorizar medicamentos
generar lista de recomendaciones
```

---

## Composición de respuesta

Responsable de:

```
seleccionar recomendación principal
generar alternativas
crear explicación textual
```

---

# 12. Casos de uso principales

```
CU-01 Iniciar sesión
CU-02 Cerrar sesión
CU-03 Introducir caso clínico
CU-04 Analizar caso
CU-05 Validar y editar información
CU-06 Confirmar caso validado
CU-07 Generar recomendaciones
CU-08 Generar respuesta final
CU-09 Consultar recomendación
```

---

# 13. Requisitos de rendimiento

```
análisis del caso          < 5 s
generación recomendaciones < 5 s
respuesta final            < 2 s
usuarios concurrentes      ≥ 5
```

---

# 14. Requisitos de seguridad

```
autenticación obligatoria
credenciales almacenadas con hash
comunicaciones seguras HTTPS
```

---

# 15. Requisitos de usabilidad

El sistema debe:

```
ser utilizable por personal no técnico
guiar el flujo paso a paso
mostrar información clara y estructurada
ser usable en entorno de mostrador
```

---

# 16. Principios de diseño

El sistema debe mantener:

```
separación frontend/backend
lógica de negocio en backend
dependencias externas desacopladas
arquitectura modular
posibilidad de evolución futura
```

---

# 17. Limitaciones del sistema

```
no es un sistema clínico certificado
las recomendaciones son orientativas
requieren validación del farmacéutico
los LLM pueden producir errores
```

El farmacéutico mantiene **la responsabilidad profesional final**.