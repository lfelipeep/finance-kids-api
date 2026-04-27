# 🐷 Finance Kids — Plataforma educativa de finanzas para niños

**Equipo:** Finance Kids  
**Concepto:** App educativa de finanzas para niños, como Duolingo pero de finanzas  
**API Asignada:** gRPC  
**API Adicional:** REST  
**Lenguaje:** Python 3.10+

---

## 🎯 ¿Qué es Finance Kids?

Finance Kids es una plataforma donde los niños aprenden conceptos financieros de forma divertida a través de:
- 📚 **Lecciones cortas** sobre dinero, ahorro, presupuesto y bancos
- ❓ **Quizzes interactivos** con retroalimentación inmediata
- 🪙 **Monedas de recompensa** por respuestas correctas
- 🏆 **Insignias** (badges) por logros de aprendizaje
- 🔥 **Racha de días** practicando (como Duolingo)
- 📊 **Tabla de clasificación** entre estudiantes

---

## 📁 Estructura del proyecto

```
finance_kids_api/
├── grpc/
│   ├── finance_kids.proto   ← Esquema gRPC: lecciones, quiz, progreso, badges
│   ├── grpc_server.py       ← Servidor gRPC (puerto 50051)
│   ├── grpc_client.py       ← Cliente gRPC interactivo
│   └── requirements.txt
├── rest/
│   ├── rest_server.py       ← Servidor REST Flask (puerto 5000)
│   ├── rest_client.py       ← Cliente REST interactivo
│   └── requirements.txt
├── justificacion_REST.md    ← Justificación de por qué elegimos REST
└── README.md
```

---

## 🚀 Cómo ejecutar

### ── API gRPC (Asignada) ──────────────────────────────────

```bash
cd grpc

# 1. Instalar dependencias
pip install grpcio grpcio-tools

# 2. Compilar el archivo .proto (genera finance_kids_pb2.py y finance_kids_pb2_grpc.py)
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. finance_kids.proto

# 3. Terminal 1: Iniciar servidor
python grpc_server.py

# 4. Terminal 2: Iniciar cliente
python grpc_client.py
```

### ── API REST (Adicional) ─────────────────────────────────

```bash
cd rest

# 1. Instalar dependencias
pip install flask requests

# 2. Terminal 1: Iniciar servidor
python rest_server.py

# 3. Terminal 2: Iniciar cliente
python rest_client.py
```

---

## 📡 Servicios gRPC disponibles

| RPC               | Descripción                                      |
|-------------------|--------------------------------------------------|
| `GetLesson`       | Obtener contenido completo de una lección + quiz |
| `ListLessons`     | Ver catálogo de todas las lecciones              |
| `SubmitQuizAnswer`| Enviar respuesta de un quiz y recibir feedback   |
| `GetProgress`     | Ver progreso completo de un estudiante           |
| `GetBadges`       | Ver insignias desbloqueadas y bloqueadas         |

---

## 🌐 Endpoints REST disponibles

| Método | Endpoint                       | Descripción                           |
|--------|--------------------------------|---------------------------------------|
| GET    | `/api/health`                  | Estado del servidor                   |
| GET    | `/api/lecciones`               | Catálogo de lecciones (con filtros)   |
| GET    | `/api/lecciones/<id>`          | Detalle de una lección                |
| POST   | `/api/estudiantes`             | Registrar nuevo estudiante            |
| GET    | `/api/estudiantes/<kid_id>`    | Ver perfil y progreso                 |
| POST   | `/api/respuestas`              | Enviar respuesta de quiz              |
| GET    | `/api/ranking`                 | Tabla de clasificación global         |

### Ejemplo: Registrar estudiante
```json
POST /api/estudiantes
{
  "name": "Camila",
  "age": 9
}
```

### Ejemplo: Enviar respuesta de quiz
```json
POST /api/respuestas
{
  "kid_id":      "kid_001",
  "lesson_id":   "L001",
  "question_id": "L001_Q1",
  "answer":      "B"
}
```

---

## 📚 Lecciones disponibles

| ID   | Título                         | Categoría          | 🪙  | Dificultad |
|------|--------------------------------|--------------------|-----|------------|
| L001 | ¿Qué es el dinero? 💰          | conceptos básicos  | 10  | fácil      |
| L002 | El superpoder del ahorro 🐷    | ahorro             | 15  | fácil      |
| L003 | Necesidades vs. Deseos 🍕🎮   | presupuesto        | 15  | medio      |
| L004 | Mi primer presupuesto 📊       | presupuesto        | 20  | medio      |
| L005 | ¿Qué es un banco? 🏦           | bancos             | 10  | fácil      |

---

## 👤 Estudiantes de prueba

| kid_id   | Nombre    | Monedas | Lecciones completadas |
|----------|-----------|---------|-----------------------|
| kid_001  | Valentina | 35 🪙   | L001, L002            |
| kid_002  | Santiago  | 10 🪙   | L001                  |

---

## 🏅 Sistema de insignias

| Insignia              | Condición                                    |
|-----------------------|----------------------------------------------|
| 🎉 Primera lección   | Completar al menos 1 lección                 |
| ⭐ Ahorrador estrella | Completar lección L002 con 100% de aciertos  |
| 🔥 Racha de 3 días   | Practicar 3 días seguidos                    |
| 📊 Experto presupuesto| Completar lecciones L003 y L004              |
| 🏆 Finance Kids Master| Completar las 5 lecciones disponibles        |

---

*Finance Kids · Proyecto APIs · 2025*
