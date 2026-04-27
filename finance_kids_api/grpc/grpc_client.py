"""
╔══════════════════════════════════════════════════════════════╗
║        FINANCE KIDS — Cliente gRPC                           ║
║  Plataforma educativa de finanzas para niños (como Duolingo) ║
║  Tipo de API: gRPC                                           ║
╚══════════════════════════════════════════════════════════════╝

PASOS PARA EJECUTAR:
  1. Asegúrate de que grpc_server.py esté corriendo
  2. python grpc_client.py
"""

import grpc
import finance_kids_pb2
import finance_kids_pb2_grpc


SERVER_ADDR = "localhost:50051"


# ──────────────────────────────────────────────────────────────────
#  FUNCIONES DE CADA RPC
# ──────────────────────────────────────────────────────────────────

def ver_catalogo(stub):
    """
    Llama a ListLessons → muestra todas las lecciones disponibles.
    """
    try:
        response = stub.ListLessons(finance_kids_pb2.EmptyRequest())
        lecciones = response.lessons

        print(f"\n  {'─'*58}")
        print(f"  📚 CATÁLOGO DE LECCIONES — Finance Kids")
        print(f"  {'─'*58}")
        print(f"  {'ID':<6} {'CATEGORÍA':<16} {'MONEDAS':>8}  LECCIÓN")
        print(f"  {'─'*58}")

        for l in lecciones:
            estado = "✅" if l.completed else "🔒"
            print(f"  {estado} {l.lesson_id:<5} {l.category:<16} "
                  f"🪙{l.coins_reward:>4}    {l.title}")

        print(f"  {'─'*58}")
        print(f"  Total: {len(lecciones)} lecciones disponibles\n")

    except grpc.RpcError as e:
        print(f"\n  ❌ Error gRPC [{e.code()}]: {e.details()}")


def hacer_leccion(stub, kid_id):
    """
    Llama a GetLesson para cargar la lección y luego SubmitQuizAnswer
    por cada pregunta. Simula la experiencia de aprendizaje completa.
    """
    lesson_id = input("\n  ID de la lección (Ej: L001): ").strip().upper()

    try:
        # 1. Obtener la lección
        response = stub.GetLesson(finance_kids_pb2.LessonRequest(lesson_id=lesson_id))

        print(f"\n  {'═'*55}")
        print(f"  📖 {response.title}")
        print(f"  {'═'*55}")
        print(f"  {response.description}")
        print(f"  🏷  Categoría: {response.category}")
        print(f"  🪙  Recompensa: {response.coins_reward} monedas al completar")
        print(f"  {'─'*55}")
        input("\n  ¡Presiona Enter cuando estés listo para el quiz! 🎯 ")

        # 2. Hacer el quiz pregunta por pregunta
        total_coins = 0

        for i, q in enumerate(response.questions, start=1):
            print(f"\n  {'─'*50}")
            print(f"  Pregunta {i} de {len(response.questions)}")
            print(f"  {'─'*50}")
            print(f"\n  ❓ {q.question}\n")
            for opt in q.options:
                print(f"     {opt}")
            print()

            respuesta = input("  Tu respuesta (A/B/C/D): ").strip().upper()

            # 3. Enviar respuesta al servidor
            resultado = stub.SubmitQuizAnswer(finance_kids_pb2.QuizAnswerRequest(
                kid_id=kid_id,
                lesson_id=lesson_id,
                question_id=q.question_id,
                answer=respuesta,
            ))

            if resultado.correct:
                print(f"\n  ✅ ¡CORRECTO! +{resultado.coins_earned} 🪙")
                total_coins += resultado.coins_earned
            else:
                print(f"\n  ❌ Respuesta incorrecta.")

            print(f"  💡 {resultado.explanation}")
            print(f"  {resultado.encouragement}")

        # Resumen final
        print(f"\n  {'═'*50}")
        print(f"  🎉 ¡Lección completada!")
        print(f"  🪙 Monedas ganadas esta lección: {total_coins}")
        print(f"  {'═'*50}\n")

    except grpc.RpcError as e:
        print(f"\n  ❌ Error gRPC [{e.code()}]: {e.details()}")


def ver_progreso(stub):
    """
    Llama a GetProgress → muestra el progreso completo de un niño.
    """
    kid_id = input("\n  ID del estudiante (Ej: kid_001): ").strip()

    try:
        response = stub.GetProgress(finance_kids_pb2.ProgressRequest(kid_id=kid_id))

        print(f"\n  {'═'*55}")
        print(f"  👤 Hola, {response.name}! 👋")
        print(f"  {'─'*55}")
        print(f"  🪙 Monedas totales : {response.total_coins}")
        print(f"  🏅 Nivel           : {response.level}")
        print(f"  🔥 Racha actual    : {response.streak_days} días seguidos")
        print(f"  {'─'*55}")
        print(f"  📚 PROGRESO DE LECCIONES:")
        print(f"  {'─'*55}")

        for lp in response.lessons_progress:
            estado = "✅ Completada" if lp.completed else "⬜ Pendiente "
            score  = f"  | Puntaje: {lp.score}%" if lp.completed else ""
            print(f"  {estado}  {lp.lesson_id}  {lp.title}{score}")

        completadas = sum(1 for lp in response.lessons_progress if lp.completed)
        total       = len(response.lessons_progress)
        barra       = "█" * completadas + "░" * (total - completadas)

        print(f"\n  Progreso: [{barra}] {completadas}/{total} lecciones\n")

    except grpc.RpcError as e:
        print(f"\n  ❌ Error gRPC [{e.code()}]: {e.details()}")


def ver_insignias(stub):
    """
    Llama a GetBadges → muestra las insignias de un niño.
    """
    kid_id = input("\n  ID del estudiante (Ej: kid_001): ").strip()

    try:
        response = stub.GetBadges(finance_kids_pb2.BadgeRequest(kid_id=kid_id))

        print(f"\n  {'═'*50}")
        print(f"  🏆 INSIGNIAS DE {kid_id}")
        print(f"  {'═'*50}")

        for badge in response.badges:
            if badge.unlocked:
                print(f"\n  {badge.icon} {badge.name}  ✅ DESBLOQUEADA")
            else:
                print(f"\n  🔒 {badge.name}  (bloqueada)")
            print(f"     {badge.description}")

        unlocked = sum(1 for b in response.badges if b.unlocked)
        print(f"\n  Total: {unlocked}/{len(response.badges)} insignias desbloqueadas\n")

    except grpc.RpcError as e:
        print(f"\n  ❌ Error gRPC [{e.code()}]: {e.details()}")


# ──────────────────────────────────────────────────────────────────
#  MENÚ PRINCIPAL
# ──────────────────────────────────────────────────────────────────

MENU = """
╔══════════════════════════════════════════════╗
║   🐷 FINANCE KIDS — Aprende Finanzas         ║
╠══════════════════════════════════════════════╣
║  1. Ver catálogo de lecciones                ║
║  2. Hacer una lección + quiz                 ║
║  3. Ver mi progreso                          ║
║  4. Ver mis insignias                        ║
║  5. Salir                                    ║
╚══════════════════════════════════════════════╝
"""

def main():
    kid_id = input("\n  👋 ¡Hola! ¿Cuál es tu ID de estudiante? (Ej: kid_001): ").strip()
    if not kid_id:
        kid_id = "kid_001"

    with grpc.insecure_channel(SERVER_ADDR) as channel:
        stub = finance_kids_pb2_grpc.FinanceKidsServiceStub(channel)
        print(f"\n  ✅ Conectado al servidor Finance Kids ({SERVER_ADDR})")
        print(f"  🎓 ¡Bienvenido, {kid_id}! Vamos a aprender sobre finanzas.\n")

        while True:
            print(MENU)
            opcion = input("  ¿Qué quieres hacer? (1-5): ").strip()

            if opcion == "1":
                ver_catalogo(stub)
            elif opcion == "2":
                hacer_leccion(stub, kid_id)
            elif opcion == "3":
                ver_progreso(stub)
            elif opcion == "4":
                ver_insignias(stub)
            elif opcion == "5":
                print("\n  🐷 ¡Hasta pronto! Sigue aprendiendo sobre finanzas. 🌟\n")
                break
            else:
                print("\n  ⚠️  Opción inválida. Elige entre 1 y 5.\n")


if __name__ == "__main__":
    main()
