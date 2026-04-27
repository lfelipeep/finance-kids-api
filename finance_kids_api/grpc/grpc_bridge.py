"""
╔══════════════════════════════════════════════════════════════╗
║        FINANCE KIDS — Puente gRPC (datos integrados)         ║
║  Simula las respuestas del servidor gRPC directamente        ║
║  Compatible con Render (plan gratuito)                       ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import random
from flask import Flask, jsonify, request

app = Flask(__name__)

# ── CORS ──────────────────────────────────────────────────────
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


# ── BASE DE DATOS INTEGRADA ───────────────────────────────────

LECCIONES_DB = {
    "L001": {
        "title":       "¿Qué es el dinero? 💰",
        "category":    "conceptos básicos",
        "description": "Aprende para qué sirve el dinero y cómo lo usamos todos los días.",
        "coins_reward": 10,
        "questions": [
            {
                "question_id": "L001_Q1",
                "question":    "¿Para qué sirve el dinero?",
                "options":     ["A) Para jugar con él", "B) Para comprar cosas que necesitamos", "C) Para decorar la habitación", "D) Para hacer origami"],
                "correct":     "B",
                "explanation": "El dinero nos permite comprar cosas que necesitamos o queremos.",
            },
            {
                "question_id": "L001_Q2",
                "question":    "¿Cuál de estos es un ejemplo de ganar dinero?",
                "options":     ["A) Comprar una pizza", "B) Perder tu monedero", "C) Recibir tu mesada por hacer tareas", "D) Gastar en el cine"],
                "correct":     "C",
                "explanation": "Hacer tareas en casa y recibir una mesada es una forma de ganarse el dinero.",
            },
        ],
    },
    "L002": {
        "title":       "El superpoder del ahorro 🐷",
        "category":    "ahorro",
        "description": "Descubre por qué ahorrar es una de las mejores habilidades financieras.",
        "coins_reward": 15,
        "questions": [
            {
                "question_id": "L002_Q1",
                "question":    "Si tienes $10.000 y gastas $3.000, ¿cuánto te queda para ahorrar?",
                "options":     ["A) $5.000", "B) $8.000", "C) $7.000", "D) $13.000"],
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
        "questions": [
            {
                "question_id": "L003_Q1",
                "question":    "¿Cuál de estos es una NECESIDAD?",
                "options":     ["A) Un videojuego nuevo", "B) Comida y agua", "C) Zapatos de marca", "D) Un celular de último modelo"],
                "correct":     "B",
                "explanation": "La comida y el agua son necesidades básicas. Los videojuegos son deseos.",
            },
        ],
    },
    "L004": {
        "title":       "Mi primer presupuesto 📊",
        "category":    "presupuesto",
        "description": "Un presupuesto es un plan para tu dinero. ¡Aprende a hacer el tuyo!",
        "coins_reward": 20,
        "questions": [
            {
                "question_id": "L004_Q1",
                "question":    "¿Qué es un presupuesto?",
                "options":     ["A) Un tipo de moneda", "B) Un plan para saber cuánto gastas y cuánto ahorras", "C) Un juego de matemáticas", "D) El nombre de un banco"],
                "correct":     "B",
                "explanation": "Un presupuesto te ayuda a planear cómo usar tu dinero.",
            },
        ],
    },
    "L005": {
        "title":       "¿Qué es un banco? 🏦",
        "category":    "bancos",
        "description": "Conoce cómo funcionan los bancos y cómo pueden ayudarte a cuidar tu dinero.",
        "coins_reward": 10,
        "questions": [
            {
                "question_id": "L005_Q1",
                "question":    "¿Qué hace un banco con el dinero que le confías?",
                "options":     ["A) Lo gasta en viajes", "B) Lo guarda seguro y lo presta a otros cobrando intereses", "C) Lo quema para no perderlo", "D) Lo convierte en oro"],
                "correct":     "B",
                "explanation": "Los bancos guardan el dinero de muchas personas y lo prestan a quienes lo necesitan.",
            },
        ],
    },
}

PROGRESO_DB = {
    "kid_001": {"name": "Valentina", "total_coins": 35, "level": 2, "streak_days": 3, "completed_lessons": {"L001", "L002"}, "scores": {"L001": 100, "L002": 50}},
    "kid_002": {"name": "Santiago",  "total_coins": 10, "level": 1, "streak_days": 1, "completed_lessons": {"L001"},         "scores": {"L001": 100}},
}

BADGES_CATALOG = [
    {"name": "Primera lección",      "icon": "🎉", "description": "Completaste tu primera lección.",          "condition": lambda p: len(p["completed_lessons"]) >= 1},
    {"name": "Ahorrador estrella",   "icon": "⭐", "description": "Completaste L002 con 100% de aciertos.",  "condition": lambda p: p["scores"].get("L002", 0) == 100},
    {"name": "Racha de 3 días",      "icon": "🔥", "description": "Practicaste 3 días seguidos.",            "condition": lambda p: p["streak_days"] >= 3},
    {"name": "Experto presupuesto",  "icon": "📊", "description": "Completaste todas las lecciones de presupuesto.", "condition": lambda p: {"L003","L004"}.issubset(p["completed_lessons"])},
    {"name": "Finance Kids Master",  "icon": "🏆", "description": "Completaste todas las lecciones.",        "condition": lambda p: len(p["completed_lessons"]) >= 5},
]

MENSAJES_OK  = ["¡Increíble! 🌟", "¡Eso es! 🎉", "¡Perfecto! 🚀", "¡Brillante! ✨"]
MENSAJES_ERR = ["¡No te rindas! 💪", "¡Casi! 🌈 Lee la explicación.", "¡Sigue intentando! 😊"]


# ── ENDPOINTS ────────────────────────────────────────────────

@app.route("/bridge/health", methods=["GET"])
def health():
    return jsonify({"ok": True, "status": "conectado ✅", "mode": "datos integrados"}), 200


@app.route("/bridge/lecciones", methods=["GET"])
def list_lessons():
    lecciones = [
        {"lesson_id": lid, "title": d["title"], "category": d["category"],
         "coins_reward": d["coins_reward"], "completed": False}
        for lid, d in LECCIONES_DB.items()
    ]
    return jsonify({"ok": True, "lecciones": lecciones}), 200


@app.route("/bridge/lecciones/<lesson_id>", methods=["GET"])
def get_lesson(lesson_id):
    lesson_id = lesson_id.upper()
    if lesson_id not in LECCIONES_DB:
        return jsonify({"ok": False, "error": f"Lección '{lesson_id}' no existe."}), 404

    data = LECCIONES_DB[lesson_id]
    questions = [
        {"question_id": q["question_id"], "question": q["question"], "options": q["options"]}
        for q in data["questions"]
    ]
    return jsonify({
        "ok": True, "lesson_id": lesson_id, "title": data["title"],
        "description": data["description"], "category": data["category"],
        "coins_reward": data["coins_reward"], "questions": questions,
    }), 200


@app.route("/bridge/responder", methods=["POST"])
def submit_answer():
    body       = request.get_json()
    lesson_id  = body.get("lesson_id", "").upper()
    qid        = body.get("question_id", "")
    answer     = body.get("answer", "").upper()
    kid_id     = body.get("kid_id", "")

    if lesson_id not in LECCIONES_DB:
        return jsonify({"ok": False, "error": "Lección no encontrada."}), 404

    question = next((q for q in LECCIONES_DB[lesson_id]["questions"] if q["question_id"] == qid), None)
    if not question:
        return jsonify({"ok": False, "error": "Pregunta no encontrada."}), 404

    is_correct = (answer == question["correct"])
    coins      = LECCIONES_DB[lesson_id]["coins_reward"] // len(LECCIONES_DB[lesson_id]["questions"]) if is_correct else 0
    encourage  = random.choice(MENSAJES_OK if is_correct else MENSAJES_ERR)

    if kid_id in PROGRESO_DB and is_correct:
        PROGRESO_DB[kid_id]["total_coins"] += coins

    return jsonify({
        "ok": True, "correct": is_correct,
        "explanation": question["explanation"],
        "coins_earned": coins, "encouragement": encourage,
    }), 200


@app.route("/bridge/progreso/<kid_id>", methods=["GET"])
def get_progress(kid_id):
    if kid_id not in PROGRESO_DB:
        return jsonify({"ok": False, "error": f"Estudiante '{kid_id}' no encontrado."}), 404

    prog = PROGRESO_DB[kid_id]
    lessons = [
        {"lesson_id": lid, "title": LECCIONES_DB[lid]["title"],
         "completed": lid in prog["completed_lessons"], "score": prog["scores"].get(lid, 0)}
        for lid in LECCIONES_DB
    ]
    return jsonify({
        "ok": True, "kid_id": kid_id, "name": prog["name"],
        "total_coins": prog["total_coins"], "level": prog["level"],
        "streak_days": prog["streak_days"], "lessons_progress": lessons,
    }), 200


@app.route("/bridge/insignias/<kid_id>", methods=["GET"])
def get_badges(kid_id):
    if kid_id not in PROGRESO_DB:
        return jsonify({"ok": False, "error": f"Estudiante '{kid_id}' no encontrado."}), 404

    prog   = PROGRESO_DB[kid_id]
    badges = [
        {"name": b["name"], "description": b["description"],
         "icon": b["icon"], "unlocked": b["condition"](prog)}
        for b in BADGES_CATALOG
    ]
    return jsonify({"ok": True, "kid_id": kid_id, "badges": badges}), 200


# ── INICIO ───────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    print(f"🔌 Finance Kids Bridge corriendo en puerto {port}")
    app.run(host="0.0.0.0", port=port, debug=False)