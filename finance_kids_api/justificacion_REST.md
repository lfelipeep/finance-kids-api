# Justificación de la API Adicional — REST
**Equipo:** Finance Kids  
**API Asignada:** gRPC  
**API Adicional Seleccionada:** REST (Representational State Transfer)

---

## Contexto del proyecto

Finance Kids es una plataforma educativa de finanzas para niños, similar a Duolingo pero enfocada en conceptos financieros. Los niños aprenden sobre ahorro, presupuesto, bancos y dinero a través de lecciones cortas, quizzes interactivos y un sistema de recompensas con monedas y badges.

---

## ¿Por qué REST complementa a gRPC en Finance Kids?

### 1. Diferentes roles dentro de la misma plataforma

En una plataforma como Finance Kids, los dos tipos de API cumplen funciones distintas y complementarias:

| Componente                              | API ideal | Razón                                               |
|-----------------------------------------|-----------|-----------------------------------------------------|
| Comunicación servidor ↔ backend de lecciones  | **gRPC**  | Alta velocidad, tipado fuerte, streaming eficiente  |
| Registro de estudiantes, ranking        | **REST**  | Fácil integración con apps web y móviles            |
| Historial de respuestas, perfil público | **REST**  | JSON legible, fácil de cachear y consumir           |
| Sincronización de progreso en tiempo real | **gRPC** | Streaming bidireccional eficiente                   |

### 2. Accesibilidad para el público objetivo

Finance Kids está dirigido a niños y a sus padres. Las interfaces que ellos utilizan (apps móviles, páginas web en el navegador) se conectan naturalmente con APIs REST, ya que:

- Cualquier navegador puede hacer peticiones HTTP directamente.
- Las apps móviles (iOS, Android) tienen soporte nativo para REST.
- No se requiere instalar librerías adicionales de gRPC en el dispositivo del usuario final.

### 3. Panel de padres y maestros

Una funcionalidad clave de Finance Kids es que los padres y maestros puedan ver el progreso de los niños. Un panel de seguimiento web consume fácilmente una API REST para mostrar:

- El ranking de la clase.
- El historial de respuestas de cada estudiante.
- Las lecciones completadas y el nivel actual.

REST es el estándar para este tipo de dashboards web.

### 4. Facilidad de prueba durante el desarrollo

Durante el desarrollo y la presentación en clase, REST tiene una ventaja clave: se puede probar directamente con el navegador o con herramientas como Postman, sin necesidad de compilar esquemas `.proto` ni instalar runtimes especiales. Esto agiliza las demostraciones en vivo.

### 5. Escalabilidad y mantenimiento

REST permite implementar fácilmente caché HTTP en respuestas como el catálogo de lecciones (que no cambia frecuentemente), reduciendo la carga del servidor. gRPC, al ser binario, no se beneficia de esta caché de manera tan directa.

---

## Comparativa directa

| Característica        | gRPC (asignado)                     | REST (adicional)                        |
|-----------------------|-------------------------------------|-----------------------------------------|
| Protocolo             | HTTP/2 + Protocol Buffers (binario) | HTTP/1.1 o HTTP/2 + JSON (texto)        |
| Rendimiento           | Muy alto                            | Alto                                    |
| Legibilidad           | Solo con herramientas especiales    | Directamente en el navegador            |
| Casos de uso          | Lecciones, quizzes, progreso interno| Registro, ranking, panel de padres      |
| Curva de aprendizaje  | Alta                                | Baja                                    |
| Compatibilidad        | Requiere cliente gRPC               | Cualquier cliente HTTP                  |

---

## Conclusión

La combinación **gRPC + REST** en Finance Kids no es redundante sino arquitectónicamente correcta:

- **gRPC** maneja la lógica central del aprendizaje: entrega de lecciones, evaluación de respuestas, seguimiento de progreso y entrega de badges. Es eficiente, rápido y tipado, ideal para el núcleo del sistema.

- **REST** se encarga de la capa pública: registro de nuevos estudiantes, consulta del ranking, panel de padres y maestros. Es accesible desde cualquier dispositivo sin configuración adicional.

Esta arquitectura refleja exactamente cómo funcionan aplicaciones educativas reales como **Duolingo**, **Khan Academy** o **Brilliant**: gRPC o protocolos binarios para el motor interno, y REST para la capa de usuario final.

---

*Finance Kids — Proyecto de APIs | 2025*
