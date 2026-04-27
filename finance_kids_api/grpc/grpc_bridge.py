"""
╔══════════════════════════════════════════════════════════════╗
║        FINANCE KIDS — Puente gRPC ↔ HTTP                     ║
║  Traduce peticiones HTTP del navegador a llamadas gRPC        ║
║  Corre en puerto 5001                                         ║
╚══════════════════════════════════════════════════════════════╝

PASOS PARA EJECUTAR:
  1. Asegúrate de que grpc_server.py esté corriendo (puerto 50051)
  2. pip install flask grpcio grpcio-tools
  3. python grpc_bridge.py
"""

import grpc
import finance_kids_pb2
import finance_kids_pb2_grpc
from flask import Flask, jsonify, request

app   = Flask(__name__)
GRPC_ADDR = "localhost:50051"


# ──────────────────────────────────────────────────────────
#  CORS: permite que el HTML abra estos endpoints
# ──────────────────────────────────────────────────────────

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


# ──────────────────────────────────────────────────────────
#  HELPER: conexión al servidor gRPC
# ──────────────────────────────────────────────────────────

def get_stub():
    channel = grpc.insecure_channel(GRPC_ADDR)
    return finance_kids_pb2_grpc.FinanceKidsServiceStub(channel)


# ──────────────────────────────────────────────────────────
#  ENDPOINTS DEL PUENTE
# ──────────────────────────────────────────────────────────

@app.route("/bridge/lecciones", methods=["GET"])
def list_lessons():
    """Puente → gRPC ListLessons"""
    try:
        stub     = get_stub()
        response = stub.ListLessons(finance_kids_pb2.EmptyRequest())
        lecciones = [
            {
                "lesson_id":    l.lesson_id,
                "title":        l.title,
                "category":     l.category,
                "coins_reward": l.coins_reward,
                "completed":    l.completed,
            }
            for l in response.lessons
        ]
        return jsonify({"ok": True, "lecciones": lecciones}), 200
    except grpc.RpcError as e:
        return jsonify({"ok": False, "error": e.details(), "code": str(e.code())}), 500


@app.route("/bridge/lecciones/<lesson_id>", methods=["GET"])
def get_lesson(lesson_id):
    """Puente → gRPC GetLesson"""
    try:
        stub     = get_stub()
        response = stub.GetLesson(finance_kids_pb2.LessonRequest(lesson_id=lesson_id.upper()))
        questions = [
            {
                "question_id": q.question_id,
                "question":    q.question,
                "options":     list(q.options),
            }
            for q in response.questions
        ]
        return jsonify({
            "ok":           True,
            "lesson_id":    response.lesson_id,
            "title":        response.title,
            "description":  response.description,
            "category":     response.category,
            "coins_reward": response.coins_reward,
            "questions":    questions,
        }), 200
    except grpc.RpcError as e:
        return jsonify({"ok": False, "error": e.details(), "code": str(e.code())}), 404


@app.route("/bridge/responder", methods=["POST"])
def submit_answer():
    """Puente → gRPC SubmitQuizAnswer"""
    body = request.get_json()
    try:
        stub     = get_stub()
        response = stub.SubmitQuizAnswer(finance_kids_pb2.QuizAnswerRequest(
            kid_id=body.get("kid_id", ""),
            lesson_id=body.get("lesson_id", "").upper(),
            question_id=body.get("question_id", ""),
            answer=body.get("answer", "").upper(),
        ))
        return jsonify({
            "ok":            True,
            "correct":       response.correct,
            "explanation":   response.explanation,
            "coins_earned":  response.coins_earned,
            "encouragement": response.encouragement,
        }), 200
    except grpc.RpcError as e:
        return jsonify({"ok": False, "error": e.details()}), 500


@app.route("/bridge/progreso/<kid_id>", methods=["GET"])
def get_progress(kid_id):
    """Puente → gRPC GetProgress"""
    try:
        stub     = get_stub()
        response = stub.GetProgress(finance_kids_pb2.ProgressRequest(kid_id=kid_id))
        lessons  = [
            {
                "lesson_id": lp.lesson_id,
                "title":     lp.title,
                "completed": lp.completed,
                "score":     lp.score,
            }
            for lp in response.lessons_progress
        ]
        return jsonify({
            "ok":              True,
            "kid_id":          response.kid_id,
            "name":            response.name,
            "total_coins":     response.total_coins,
            "level":           response.level,
            "streak_days":     response.streak_days,
            "lessons_progress": lessons,
        }), 200
    except grpc.RpcError as e:
        return jsonify({"ok": False, "error": e.details()}), 404


@app.route("/bridge/insignias/<kid_id>", methods=["GET"])
def get_badges(kid_id):
    """Puente → gRPC GetBadges"""
    try:
        stub     = get_stub()
        response = stub.GetBadges(finance_kids_pb2.BadgeRequest(kid_id=kid_id))
        badges   = [
            {
                "name":        b.name,
                "description": b.description,
                "icon":        b.icon,
                "unlocked":    b.unlocked,
            }
            for b in response.badges
        ]
        return jsonify({"ok": True, "kid_id": response.kid_id, "badges": badges}), 200
    except grpc.RpcError as e:
        return jsonify({"ok": False, "error": e.details()}), 404


@app.route("/bridge/health", methods=["GET"])
def health():
    try:
        stub = get_stub()
        stub.ListLessons(finance_kids_pb2.EmptyRequest())
        return jsonify({"ok": True, "grpc_server": GRPC_ADDR, "status": "conectado ✅"}), 200
    except grpc.RpcError as e:
        return jsonify({"ok": False, "status": "sin conexión ❌", "error": e.details()}), 500


if __name__ == "__main__":
    print("=" * 55)
    print("  🔌 FINANCE KIDS — Puente gRPC↔HTTP")
    print(f"  📡 HTTP:  http://localhost:5001")
    print(f"  📡 gRPC:  {GRPC_ADDR}")
    print("  📌 Endpoints del puente:")
    print("     GET  /bridge/health")
    print("     GET  /bridge/lecciones")
    print("     GET  /bridge/lecciones/<id>")
    print("     POST /bridge/responder")
    print("     GET  /bridge/progreso/<kid_id>")
    print("     GET  /bridge/insignias/<kid_id>")
    print("  ⏹  Ctrl+C para detener")
    print("=" * 55)
    import os 
    port = int(os.environ.get("PORT", 5001)) 
    app.run(host="0.0.0.0", port=port, debug=False)
    