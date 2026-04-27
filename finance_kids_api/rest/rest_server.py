"""
╔══════════════════════════════════════════════════════════════╗
║        FINANCE KIDS — Servidor REST                          ║
║  Plataforma educativa de finanzas para niños (como Duolingo) ║
║  Tipo de API: REST                                           ║
╚══════════════════════════════════════════════════════════════╝

PASOS PARA EJECUTAR:
  1. pip install flask
  2. python rest_server.py

ENDPOINTS DISPONIBLES:
  GET  /api/lecciones                  → Catálogo de lecciones
  GET  /api/lecciones/<id>             → Detalle de una lección
  GET  /api/estudiantes/<kid_id>       → Perfil del estudiante
  POST /api/estudiantes                → Registrar nuevo estudiante
  POST /api/respuestas                 → Enviar respuesta del quiz
  GET  /api/ranking                    → Tabla de clasificación global
  GET  /api/health                     → Estado del servidor
"""

import uuid
import random
from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

# CORS: permite que el HTML (file:// o cualquier origen) consuma la API
@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"]  = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

@app.route("/", defaults={"path": ""}, methods=["OPTIONS"])
@app.route("/<path:path>", methods=["OPTIONS"])
def options_handler(path):
    return jsonify({}), 200


# ──────────────────────────────────────────────────────────────────
#  BASE DE DATOS EN MEMORIA
# ──────────────────────────────────────────────────────────────────

LECCIONES_DB = {
    "L001": {
        "title":       "¿Qué es el dinero? 💰",
        "category":    "conceptos básicos",
        "description": "Aprende para qué sirve el dinero y cómo lo usamos todos los días.",
        "coins_reward": 10,
        "difficulty":  "fácil",
        "questions": [
            {
                "question_id": "L001_Q1",
                "question":    "¿Para qué sirve el dinero?",
                "options": {
                    "A": "Para jugar con él",
                    "B": "Para comprar cosas que necesitamos",
                    "C": "Para decorar la habitación",
                    "D": "Para hacer origami",
                },
                "correct":     "B",
                "explanation": "El dinero nos permite comprar cosas que necesitamos o queremos, como comida, ropa o juguetes.",
            },
            {
                "question_id": "L001_Q2",
                "question":    "¿Cuál de estos es un ejemplo de ganar dinero?",
                "options": {
                    "A": "Comprar una pizza",
                    "B": "Perder tu monedero",
                    "C": "Recibir tu mesada por hacer tareas",
                    "D": "Gastar en el cine",
                },
                "correct":     "C",
                "explanation": "Hacer tareas en casa y recibir una mesada es una forma de ganarse el dinero.",
            },
        ],
    },
    "L002": {
        "title":       "El superpoder del ahorro 🐷",
        "category":    "ahorro",
        "description": "Descubre por qué ahorrar es una de las mejores habilidades financieras que puedes aprender.",
        "coins_reward": 15,
        "difficulty":  "fácil",
        "questions": [
            {
                "question_id": "L002_Q1",
                "question":    "Si tienes $10.000 y gastas $3.000, ¿cuánto te queda para ahorrar?",
                "options": {"A": "$5.000", "B": "$8.000", "C": "$7.000", "D": "$13.000"},
                "correct":     "C",
                "explanation": "$10.000 - $3.000 = $7.000. Guardar lo que sobra es exactamente lo que significa ahorrar.",
            },
        ],
    },
    "L003": {
        "title":       "Necesidades vs. Deseos 🍕🎮",
        "category":    "presupuesto",
        "description": "Aprende a diferenciar lo que realmente necesitas de lo que simplemente quieres.",
        "coins_reward": 15,
        "difficulty":  "medio",
        "questions": [
            {
                "question_id": "L003_Q1",
                "question":    "¿Cuál de estos es una NECESIDAD?",
                "options": {
                    "A": "Un videojuego nuevo",
                    "B": "Comida y agua",
                    "C": "Zapatos de marca",
                    "D": "Un celular de último modelo",
                },
                "correct":     "B",
                "explanation": "La comida y el agua son necesidades básicas. Los videojuegos y la ropa de moda son deseos.",
            },
        ],
    },
    "L004": {
        "title":       "Mi primer presupuesto 📊",
        "category":    "presupuesto",
        "description": "Un presupuesto es un plan para tu dinero. ¡Aprende a hacer el tuyo!",
        "coins_reward": 20,
        "difficulty":  "medio",
        "questions": [
            {
                "question_id": "L004_Q1",
                "question":    "¿Qué es un presupuesto?",
                "options": {
                    "A": "Un tipo de moneda",
                    "B": "Un plan para saber cuánto gastas y cuánto ahorras",
                    "C": "Un juego de matemáticas",
                    "D": "El nombre de un banco",
                },
                "correct":     "B",
                "explanation": "Un presupuesto te ayuda a planear cómo usar tu dinero para que no te quedes sin nada antes de fin de mes.",
            },
        ],
    },
    "L005": {
        "title":       "¿Qué es un banco? 🏦",
        "category":    "bancos",
        "description": "Conoce cómo funcionan los bancos y cómo pueden ayudarte a cuidar tu dinero.",
        "coins_reward": 10,
        "difficulty":  "fácil",
        "questions": [
            {
                "question_id": "L005_Q1",
                "question":    "¿Qué hace un banco con el dinero que le confías?",
                "options": {
                    "A": "Lo gasta en viajes",
                    "B": "Lo guarda seguro y lo presta a otros cobrando intereses",
                    "C": "Lo quema para no perderlo",
                    "D": "Lo convierte en oro",
                },
                "correct":     "B",
                "explanation": "Los bancos guardan el dinero de muchas personas y lo prestan a quienes lo necesitan.",
            },
        ],
    },
}

ESTUDIANTES_DB = {
    "kid_001": {
        "name":              "Valentina",
        "age":               10,
        "total_coins":       35,
        "level":             2,
        "streak_days":       3,
        "completed_lessons": ["L001", "L002"],
        "answers_history":   [],
    },
    "kid_002": {
        "name":              "Santiago",
        "age":               9,
        "total_coins":       10,
        "level":             1,
        "streak_days":       1,
        "completed_lessons": ["L001"],
        "answers_history":   [],
    },
}


# ──────────────────────────────────────────────────────────────────
#  ENDPOINTS REST
# ──────────────────────────────────────────────────────────────────

@app.route("/api/health", methods=["GET"])
def health():
    """
    GET /api/health
    Verifica que el servidor esté funcionando.
    """
    return jsonify({
        "status":    "ok",
        "service":   "Finance Kids REST API",
        "version":   "1.0.0",
        "lecciones": len(LECCIONES_DB),
        "estudiantes": len(ESTUDIANTES_DB),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }), 200


@app.route("/api/lecciones", methods=["GET"])
def listar_lecciones():
    """
    GET /api/lecciones
    Devuelve el catálogo completo de lecciones (sin las respuestas correctas).
    Query params opcionales:
      ?category=ahorro       → filtra por categoría
      ?difficulty=fácil      → filtra por dificultad
    """
    category   = request.args.get("category")
    difficulty = request.args.get("difficulty")

    lecciones = []
    for lid, data in LECCIONES_DB.items():
        if category and data["category"] != category:
            continue
        if difficulty and data["difficulty"] != difficulty:
            continue

        lecciones.append({
            "lesson_id":    lid,
            "title":        data["title"],
            "category":     data["category"],
            "description":  data["description"],
            "difficulty":   data["difficulty"],
            "coins_reward": data["coins_reward"],
            "num_questions": len(data["questions"]),
        })

    return jsonify({
        "count":     len(lecciones),
        "lecciones": lecciones,
    }), 200


@app.route("/api/lecciones/<string:lesson_id>", methods=["GET"])
def obtener_leccion(lesson_id):
    """
    GET /api/lecciones/<lesson_id>
    Devuelve el contenido completo de una lección (sin respuestas correctas).
    """
    lesson_id = lesson_id.upper()

    if lesson_id not in LECCIONES_DB:
        return jsonify({
            "error": f"La lección '{lesson_id}' no existe.",
            "disponibles": list(LECCIONES_DB.keys()),
        }), 404

    data = LECCIONES_DB[lesson_id]

    # Enviamos preguntas SIN la respuesta correcta (el cliente no debe verla)
    preguntas = [
        {
            "question_id": q["question_id"],
            "question":    q["question"],
            "options":     q["options"],
        }
        for q in data["questions"]
    ]

    return jsonify({
        "lesson_id":    lesson_id,
        "title":        data["title"],
        "category":     data["category"],
        "description":  data["description"],
        "difficulty":   data["difficulty"],
        "coins_reward": data["coins_reward"],
        "questions":    preguntas,
    }), 200


@app.route("/api/estudiantes", methods=["POST"])
def registrar_estudiante():
    """
    POST /api/estudiantes
    Registra un nuevo estudiante en la plataforma.

    Body JSON esperado:
    {
      "name": "Camila",
      "age":  8
    }
    """
    body = request.get_json()

    if not body:
        return jsonify({"error": "El cuerpo debe ser JSON."}), 400

    name = body.get("name", "").strip()
    age  = body.get("age")

    if not name:
        return jsonify({"error": "El campo 'name' es requerido."}), 400

    if not isinstance(age, int) or age < 4 or age > 18:
        return jsonify({"error": "'age' debe ser un número entre 4 y 18."}), 400

    kid_id = f"kid_{str(uuid.uuid4())[:4]}"
    ESTUDIANTES_DB[kid_id] = {
        "name":              name,
        "age":               age,
        "total_coins":       0,
        "level":             1,
        "streak_days":       0,
        "completed_lessons": [],
        "answers_history":   [],
    }

    print(f"[REST SERVER] Nuevo estudiante: {kid_id} — {name} ({age} años)")

    return jsonify({
        "success": True,
        "message": f"¡Bienvenido/a, {name}! Tu cuenta ha sido creada.",
        "kid_id":  kid_id,
        "student": ESTUDIANTES_DB[kid_id],
    }), 201


@app.route("/api/estudiantes/<string:kid_id>", methods=["GET"])
def obtener_estudiante(kid_id):
    """
    GET /api/estudiantes/<kid_id>
    Devuelve el perfil completo y progreso de un estudiante.
    """
    if kid_id not in ESTUDIANTES_DB:
        return jsonify({"error": f"Estudiante '{kid_id}' no encontrado."}), 404

    est = ESTUDIANTES_DB[kid_id]

    # Calcular porcentaje de avance
    total     = len(LECCIONES_DB)
    completed = len(est["completed_lessons"])
    pct       = round((completed / total) * 100, 1)

    return jsonify({
        "kid_id":            kid_id,
        "name":              est["name"],
        "age":               est["age"],
        "level":             est["level"],
        "total_coins":       est["total_coins"],
        "streak_days":       est["streak_days"],
        "completed_lessons": est["completed_lessons"],
        "progress_percent":  pct,
    }), 200


@app.route("/api/respuestas", methods=["POST"])
def enviar_respuesta():
    """
    POST /api/respuestas
    Envía la respuesta de un estudiante a una pregunta del quiz.
    Valida la respuesta, da monedas y devuelve explicación.

    Body JSON esperado:
    {
      "kid_id":      "kid_001",
      "lesson_id":   "L001",
      "question_id": "L001_Q1",
      "answer":      "B"
    }
    """
    body = request.get_json()

    if not body:
        return jsonify({"error": "El cuerpo debe ser JSON."}), 400

    required = ["kid_id", "lesson_id", "question_id", "answer"]
    missing  = [f for f in required if f not in body]
    if missing:
        return jsonify({"error": f"Campos faltantes: {missing}"}), 400

    kid_id      = body["kid_id"]
    lesson_id   = body["lesson_id"].upper()
    question_id = body["question_id"]
    answer      = body["answer"].upper()

    # Validar existencia
    if lesson_id not in LECCIONES_DB:
        return jsonify({"error": f"Lección '{lesson_id}' no existe."}), 404

    if kid_id not in ESTUDIANTES_DB:
        return jsonify({"error": f"Estudiante '{kid_id}' no encontrado."}), 404

    leccion   = LECCIONES_DB[lesson_id]
    question  = next((q for q in leccion["questions"] if q["question_id"] == question_id), None)

    if not question:
        return jsonify({"error": f"Pregunta '{question_id}' no existe en '{lesson_id}'."}), 404

    # Evaluar respuesta
    is_correct  = (answer == question["correct"])
    coins       = leccion["coins_reward"] // len(leccion["questions"]) if is_correct else 0

    mensajes_ok  = ["¡Increíble! 🌟", "¡Eso es! 🎉", "¡Perfecto! 🚀", "¡Brillante! ✨"]
    mensajes_err = ["¡No te rindas! 💪", "¡Casi! 🌈 Lee la explicación.", "¡Sigue intentando! 😊"]
    encourage    = random.choice(mensajes_ok if is_correct else mensajes_err)

    # Actualizar progreso del estudiante
    est = ESTUDIANTES_DB[kid_id]
    if is_correct:
        est["total_coins"] += coins
        if lesson_id not in est["completed_lessons"]:
            est["completed_lessons"].append(lesson_id)

    # Guardar historial
    est["answers_history"].append({
        "lesson_id":   lesson_id,
        "question_id": question_id,
        "answer":      answer,
        "correct":     is_correct,
        "timestamp":   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })

    resultado = "CORRECTA ✅" if is_correct else "INCORRECTA ❌"
    print(f"[REST SERVER] {kid_id} | {question_id} = {answer} | {resultado}")

    return jsonify({
        "correct":      is_correct,
        "explanation":  question["explanation"],
        "coins_earned": coins,
        "encouragement": encourage,
        "total_coins":  est["total_coins"],
    }), 200


@app.route("/api/ranking", methods=["GET"])
def ranking():
    """
    GET /api/ranking
    Devuelve la tabla de clasificación de todos los estudiantes ordenada por monedas.
    """
    tabla = sorted(
        [
            {
                "kid_id":      kid_id,
                "name":        est["name"],
                "total_coins": est["total_coins"],
                "level":       est["level"],
                "streak_days": est["streak_days"],
                "completed":   len(est["completed_lessons"]),
            }
            for kid_id, est in ESTUDIANTES_DB.items()
        ],
        key=lambda x: x["total_coins"],
        reverse=True,
    )

    # Agregar posición
    for i, entry in enumerate(tabla, start=1):
        entry["position"] = i
        if i == 1:
            entry["medal"] = "🥇"
        elif i == 2:
            entry["medal"] = "🥈"
        elif i == 3:
            entry["medal"] = "🥉"
        else:
            entry["medal"] = f"#{i}"

    return jsonify({
        "ranking":   tabla,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }), 200


# ──────────────────────────────────────────────────────────────────
#  MANEJADORES DE ERROR
# ──────────────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Ruta no encontrada."}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Método HTTP no permitido."}), 405


# ──────────────────────────────────────────────────────────────────
#  INICIO
# ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 58)
    print("  🐷 FINANCE KIDS — Servidor REST iniciado")
    print("  📡 URL base: http://localhost:5000")
    print("  📌 Endpoints:")
    print("     GET  /api/health")
    print("     GET  /api/lecciones")
    print("     GET  /api/lecciones/<id>")
    print("     POST /api/estudiantes       ← Registrar niño")
    print("     GET  /api/estudiantes/<id>  ← Ver progreso")
    print("     POST /api/respuestas        ← Enviar respuesta quiz")
    print("     GET  /api/ranking           ← Tabla de clasificación")
    print("  ⏹  Ctrl+C para detener")
    print("=" * 58)
    import os 
    port = int(os.environ.get("PORT", 5000)) 
    app.run(host="0.0.0.0", port=port, debug=False)
