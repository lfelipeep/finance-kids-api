"""
╔══════════════════════════════════════════════════════════════╗
║        FINANCE KIDS — Servidor gRPC                          ║
║  Plataforma educativa de finanzas para niños (como Duolingo) ║
║  Tipo de API: gRPC                                           ║
╚══════════════════════════════════════════════════════════════╝

PASOS PARA EJECUTAR:
  1. pip install grpcio grpcio-tools
  2. python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. finance_kids.proto
  3. python grpc_server.py
"""

import grpc
import finance_kids_pb2
import finance_kids_pb2_grpc
from concurrent import futures


# ──────────────────────────────────────────────────────────────────
#  CONTENIDO EDUCATIVO — Base de datos de lecciones y quizzes
# ──────────────────────────────────────────────────────────────────

LECCIONES_DB = {
    "L001": {
        "title":        "¿Qué es el dinero? 💰",
        "description":  "Aprende para qué sirve el dinero y cómo lo usamos todos los días.",
        "category":     "conceptos básicos",
        "coins_reward": 10,
        "questions": [
            {
                "question_id": "L001_Q1",
                "question":    "¿Para qué sirve el dinero?",
                "options":     [
                    "A) Para jugar con él",
                    "B) Para comprar cosas que necesitamos",
                    "C) Para decorar la habitación",
                    "D) Para hacer origami",
                ],
                "correct": "B",
                "explanation": "¡Correcto! El dinero nos permite comprar cosas que necesitamos o queremos, como comida, ropa o juguetes.",
            },
            {
                "question_id": "L001_Q2",
                "question":    "¿Cuál de estos es un ejemplo de ganar dinero?",
                "options":     [
                    "A) Comprar una pizza",
                    "B) Perder tu monedero",
                    "C) Recibir tu mesada por hacer tareas",
                    "D) Gastar en el cine",
                ],
                "correct": "C",
                "explanation": "¡Así es! Hacer tareas en casa y recibir una mesada es una forma de ganarse el dinero, igual que los adultos trabajan para ganar su salario.",
            },
        ],
    },
    "L002": {
        "title":        "El superpoder del ahorro 🐷",
        "description":  "Descubre por qué ahorrar es una de las mejores habilidades financieras que puedes aprender.",
        "category":     "ahorro",
        "coins_reward": 15,
        "questions": [
            {
                "question_id": "L002_Q1",
                "question":    "Si tienes $10.000 y gastas $3.000, ¿cuánto te queda para ahorrar?",
                "options":     [
                    "A) $5.000",
                    "B) $8.000",
                    "C) $7.000",
                    "D) $13.000",
                ],
                "correct": "C",
                "explanation": "¡Muy bien! $10.000 - $3.000 = $7.000. Guardar lo que sobra es exactamente lo que significa ahorrar.",
            },
            {
                "question_id": "L002_Q2",
                "question":    "¿Dónde es más seguro guardar tus ahorros?",
                "options":     [
                    "A) Debajo de la cama",
                    "B) En una alcancía o cuenta bancaria",
                    "C) En el bolsillo del pantalón",
                    "D) Dárselos a tu amigo",
                ],
                "correct": "B",
                "explanation": "¡Correcto! Una alcancía o una cuenta de ahorros en el banco es el lugar más seguro. Los bancos protegen tu dinero.",
            },
        ],
    },
    "L003": {
        "title":        "Necesidades vs. Deseos 🍕🎮",
        "description":  "Aprende a diferenciar lo que realmente necesitas de lo que simplemente quieres.",
        "category":     "presupuesto",
        "coins_reward": 15,
        "questions": [
            {
                "question_id": "L003_Q1",
                "question":    "¿Cuál de estos es una NECESIDAD?",
                "options":     [
                    "A) Un videojuego nuevo",
                    "B) Comida y agua",
                    "C) Zapatos de marca",
                    "D) Un celular de último modelo",
                ],
                "correct": "B",
                "explanation": "¡Excelente! La comida y el agua son necesidades básicas. Sin ellas no podríamos vivir. Los videojuegos y la ropa de moda son deseos.",
            },
            {
                "question_id": "L003_Q2",
                "question":    "Tienes $20.000 para gastar. ¿Qué deberías comprar primero?",
                "options":     [
                    "A) Un libro para el colegio",
                    "B) Dulces",
                    "C) Un sticker pack",
                    "D) Una figura de colección",
                ],
                "correct": "A",
                "explanation": "¡Así es! Primero cubres las necesidades (como útiles del colegio) y con lo que sobre puedes darte un gustico.",
            },
        ],
    },
    "L004": {
        "title":        "Mi primer presupuesto 📊",
        "description":  "Un presupuesto es un plan para tu dinero. ¡Aprende a hacer el tuyo!",
        "category":     "presupuesto",
        "coins_reward": 20,
        "questions": [
            {
                "question_id": "L004_Q1",
                "question":    "¿Qué es un presupuesto?",
                "options":     [
                    "A) Un tipo de moneda",
                    "B) Un plan para saber cuánto gastas y cuánto ahorras",
                    "C) Un juego de matemáticas",
                    "D) El nombre de un banco",
                ],
                "correct": "B",
                "explanation": "¡Correcto! Un presupuesto te ayuda a planear cómo usar tu dinero para que no te quedes sin nada antes de fin de mes.",
            },
            {
                "question_id": "L004_Q2",
                "question":    "Si tu mesada es $50.000, ¿cuánto ahorrarías si guardas el 20%?",
                "options":     [
                    "A) $5.000",
                    "B) $20.000",
                    "C) $10.000",
                    "D) $25.000",
                ],
                "correct": "C",
                "explanation": "¡Muy bien! El 20% de $50.000 es $10.000. Si ahorras $10.000 cada semana, en un mes tendrás $40.000 guardados. ¡Genial!",
            },
        ],
    },
    "L005": {
        "title":        "¿Qué es un banco? 🏦",
        "description":  "Conoce cómo funcionan los bancos y cómo pueden ayudarte a cuidar tu dinero.",
        "category":     "bancos",
        "coins_reward": 10,
        "questions": [
            {
                "question_id": "L005_Q1",
                "question":    "¿Qué hace un banco con el dinero que le confías?",
                "options":     [
                    "A) Lo gasta en viajes",
                    "B) Lo guarda seguro y lo presta a otros cobrando intereses",
                    "C) Lo quema para no perderlo",
                    "D) Lo convierte en oro",
                ],
                "correct": "B",
                "explanation": "¡Exacto! Los bancos guardan el dinero de muchas personas y lo prestan a quienes lo necesitan, cobrando un pequeño porcentaje llamado interés.",
            },
            {
                "question_id": "L005_Q2",
                "question":    "¿Qué es una cuenta de ahorros?",
                "options":     [
                    "A) Una libreta donde anotas cuentas de matemáticas",
                    "B) Un lugar seguro en el banco para guardar tu dinero",
                    "C) Una tarjeta para comprar juguetes",
                    "D) Una aplicación de videojuegos",
                ],
                "correct": "B",
                "explanation": "¡Correcto! Una cuenta de ahorros es como una alcancía gigante y segura en el banco. Además, el banco te puede dar un pequeño premio (interés) por guardar ahí tu dinero.",
            },
        ],
    },
}

# Progreso de niños registrados
PROGRESO_DB = {
    "kid_001": {
        "name":        "Valentina",
        "total_coins": 35,
        "level":       2,
        "streak_days": 3,
        "completed_lessons": {"L001", "L002"},
        "scores": {"L001": 100, "L002": 50},
    },
    "kid_002": {
        "name":        "Santiago",
        "total_coins": 10,
        "level":       1,
        "streak_days": 1,
        "completed_lessons": {"L001"},
        "scores": {"L001": 100},
    },
}

# Insignias disponibles
BADGES_CATALOG = [
    {
        "name":        "Primera lección",
        "description": "Completaste tu primera lección. ¡Bienvenido!",
        "icon":        "🎉",
        "condition":   lambda progress: len(progress["completed_lessons"]) >= 1,
    },
    {
        "name":        "Ahorrador estrella",
        "description": "Completaste la lección de ahorro con 100% de aciertos.",
        "icon":        "⭐",
        "condition":   lambda progress: progress["scores"].get("L002", 0) == 100,
    },
    {
        "name":        "Racha de 3 días",
        "description": "Practicaste 3 días seguidos. ¡Eso es disciplina!",
        "icon":        "🔥",
        "condition":   lambda progress: progress["streak_days"] >= 3,
    },
    {
        "name":        "Experto en presupuesto",
        "description": "Completaste todas las lecciones de presupuesto.",
        "icon":        "📊",
        "condition":   lambda progress: {"L003", "L004"}.issubset(progress["completed_lessons"]),
    },
    {
        "name":        "Finance Kids Master",
        "description": "Completaste todas las lecciones disponibles.",
        "icon":        "🏆",
        "condition":   lambda progress: len(progress["completed_lessons"]) >= 5,
    },
]

# Mensajes motivadores según resultado
MENSAJES_CORRECTO = [
    "¡Increíble! 🌟 ¡Lo sabías!",
    "¡Eso es! 🎉 ¡Eres un genio de las finanzas!",
    "¡Perfecto! 🚀 ¡Sigue así!",
    "¡Brillante! ✨ ¡Tu cerebro financiero está creciendo!",
]

MENSAJES_INCORRECTO = [
    "¡No te rindas! 💪 ¡Sigue intentando!",
    "¡Casi! 🌈 Lee la explicación y lo lograrás.",
    "¡Error, pero aprendemos de ellos! 😊",
    "¡Tú puedes! 🌟 ¡Un error más y llegas a la respuesta!",
]

import random


# ──────────────────────────────────────────────────────────────────
#  IMPLEMENTACIÓN DEL SERVICIO gRPC
# ──────────────────────────────────────────────────────────────────

class FinanceKidsServicer(finance_kids_pb2_grpc.FinanceKidsServiceServicer):
    """
    Implementa todos los RPCs definidos en finance_kids.proto.
    Simula el backend de una app educativa de finanzas para niños.
    """

    def GetLesson(self, request, context):
        """
        RPC: Devuelve el contenido completo de una lección (explicación + quiz).
        Parámetro: lesson_id (ej: 'L001')
        """
        lesson_id = request.lesson_id.upper()

        if lesson_id not in LECCIONES_DB:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"La lección '{lesson_id}' no existe.")
            return finance_kids_pb2.LessonResponse()

        data = LECCIONES_DB[lesson_id]

        questions = [
            finance_kids_pb2.QuizQuestion(
                question_id=q["question_id"],
                question=q["question"],
                options=q["options"],
            )
            for q in data["questions"]
        ]

        print(f"[SERVER] GetLesson → {lesson_id}: '{data['title']}'")

        return finance_kids_pb2.LessonResponse(
            lesson_id=lesson_id,
            title=data["title"],
            description=data["description"],
            category=data["category"],
            coins_reward=data["coins_reward"],
            questions=questions,
        )

    def ListLessons(self, request, context):
        """
        RPC: Lista todas las lecciones disponibles con un resumen.
        """
        summaries = [
            finance_kids_pb2.LessonSummary(
                lesson_id=lid,
                title=data["title"],
                category=data["category"],
                coins_reward=data["coins_reward"],
                completed=False,  # Sin contexto de usuario, se muestra False
            )
            for lid, data in LECCIONES_DB.items()
        ]

        print(f"[SERVER] ListLessons → {len(summaries)} lecciones disponibles")
        return finance_kids_pb2.LessonListResponse(lessons=summaries)

    def SubmitQuizAnswer(self, request, context):
        """
        RPC: Recibe la respuesta de un niño a una pregunta del quiz.
        Valida si es correcta, da monedas, y responde con explicación y ánimo.
        """
        lesson_id   = request.lesson_id.upper()
        question_id = request.question_id
        answer      = request.answer.upper()
        kid_id      = request.kid_id

        if lesson_id not in LECCIONES_DB:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Lección '{lesson_id}' no encontrada.")
            return finance_kids_pb2.QuizAnswerResponse()

        # Buscar la pregunta
        lesson    = LECCIONES_DB[lesson_id]
        question  = next((q for q in lesson["questions"] if q["question_id"] == question_id), None)

        if not question:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Pregunta '{question_id}' no encontrada.")
            return finance_kids_pb2.QuizAnswerResponse()

        is_correct  = (answer == question["correct"])
        coins       = lesson["coins_reward"] // len(lesson["questions"]) if is_correct else 0
        encourage   = random.choice(MENSAJES_CORRECTO if is_correct else MENSAJES_INCORRECTO)

        # Actualizar progreso si el niño existe
        if kid_id in PROGRESO_DB:
            if is_correct:
                PROGRESO_DB[kid_id]["total_coins"] += coins

        resultado = "✅ CORRECTA" if is_correct else "❌ INCORRECTA"
        print(f"[SERVER] SubmitQuizAnswer → {kid_id} | {question_id} = {answer} | {resultado}")

        return finance_kids_pb2.QuizAnswerResponse(
            correct=is_correct,
            explanation=question["explanation"],
            coins_earned=coins,
            encouragement=encourage,
        )

    def GetProgress(self, request, context):
        """
        RPC: Devuelve el progreso completo de aprendizaje de un niño.
        """
        kid_id = request.kid_id

        if kid_id not in PROGRESO_DB:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Niño/a con ID '{kid_id}' no encontrado/a.")
            return finance_kids_pb2.ProgressResponse()

        prog = PROGRESO_DB[kid_id]

        lessons_progress = [
            finance_kids_pb2.LessonProgress(
                lesson_id=lid,
                title=LECCIONES_DB[lid]["title"],
                completed=lid in prog["completed_lessons"],
                score=prog["scores"].get(lid, 0),
            )
            for lid in LECCIONES_DB
        ]

        print(f"[SERVER] GetProgress → {kid_id} ({prog['name']}): {prog['total_coins']} monedas")

        return finance_kids_pb2.ProgressResponse(
            kid_id=kid_id,
            name=prog["name"],
            total_coins=prog["total_coins"],
            level=prog["level"],
            streak_days=prog["streak_days"],
            lessons_progress=lessons_progress,
        )

    def GetBadges(self, request, context):
        """
        RPC: Devuelve las insignias desbloqueadas y bloqueadas de un niño.
        """
        kid_id = request.kid_id

        if kid_id not in PROGRESO_DB:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Niño/a con ID '{kid_id}' no encontrado/a.")
            return finance_kids_pb2.BadgeResponse()

        prog   = PROGRESO_DB[kid_id]
        badges = [
            finance_kids_pb2.Badge(
                name=b["name"],
                description=b["description"],
                icon=b["icon"],
                unlocked=b["condition"](prog),
            )
            for b in BADGES_CATALOG
        ]

        unlocked = sum(1 for b in badges if b.unlocked)
        print(f"[SERVER] GetBadges → {kid_id}: {unlocked}/{len(badges)} insignias")

        return finance_kids_pb2.BadgeResponse(kid_id=kid_id, badges=badges)


# ──────────────────────────────────────────────────────────────────
#  INICIO DEL SERVIDOR
# ──────────────────────────────────────────────────────────────────

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    finance_kids_pb2_grpc.add_FinanceKidsServiceServicer_to_server(
        FinanceKidsServicer(), server
    )

    server.add_insecure_port("[::]:50051")
    server.start()

    print("=" * 58)
    print("  🐷 FINANCE KIDS — Servidor gRPC iniciado")
    print("  📡 Puerto: 50051")
    print("  📚 Servicios disponibles:")
    print("     • GetLesson        → Contenido de una lección")
    print("     • ListLessons      → Catálogo de lecciones")
    print("     • SubmitQuizAnswer → Enviar respuesta del quiz")
    print("     • GetProgress      → Progreso del estudiante")
    print("     • GetBadges        → Insignias desbloqueadas")
    print("  ⏹  Ctrl+C para detener")
    print("=" * 58)

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\n[SERVER] Servidor detenido correctamente.")
        server.stop(0)


if __name__ == "__main__":
    serve()
