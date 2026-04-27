"""
╔══════════════════════════════════════════════════════════════╗
║        FINANCE KIDS — Cliente REST                           ║
║  Plataforma educativa de finanzas para niños (como Duolingo) ║
║  Tipo de API: REST                                           ║
╚══════════════════════════════════════════════════════════════╝

PASOS PARA EJECUTAR:
  1. Asegúrate de que rest_server.py esté corriendo
  2. pip install requests
  3. python rest_client.py
"""

import requests
import sys

BASE_URL = "http://localhost:5000/api"
HEADERS  = {"Content-Type": "application/json"}
TIMEOUT  = 5


# ──────────────────────────────────────────────────────────────────
#  FUNCIÓN AUXILIAR DE REQUEST
# ──────────────────────────────────────────────────────────────────

def request(method: str, endpoint: str, body: dict = None, params: dict = None):
    """Realiza un request HTTP y devuelve el JSON de la respuesta."""
    url = BASE_URL + endpoint
    try:
        if method == "GET":
            r = requests.get(url, headers=HEADERS, params=params, timeout=TIMEOUT)
        elif method == "POST":
            r = requests.post(url, headers=HEADERS, json=body, timeout=TIMEOUT)
        else:
            return None

        icon = "✅" if r.status_code < 400 else "❌"
        print(f"  {icon} HTTP {r.status_code} — {method} {url}")
        return r.json()

    except requests.exceptions.ConnectionError:
        print(f"\n  ❌ Sin conexión al servidor en {BASE_URL}")
        print("     ¿Está corriendo rest_server.py?")
        return None
    except Exception as e:
        print(f"\n  ❌ Error: {e}")
        return None


# ──────────────────────────────────────────────────────────────────
#  FUNCIONES DE CADA ENDPOINT
# ──────────────────────────────────────────────────────────────────

def health_check():
    """GET /api/health"""
    data = request("GET", "/health")
    if data:
        print(f"\n  🟢 Servidor: {data.get('service')}")
        print(f"  📚 Lecciones disponibles: {data.get('lecciones')}")
        print(f"  👤 Estudiantes registrados: {data.get('estudiantes')}")
        print(f"  🕒 {data.get('timestamp')}\n")


def ver_lecciones():
    """GET /api/lecciones con filtros opcionales"""
    print("\n  Filtros (opcional — presiona Enter para omitir):")
    category   = input("  Categoría [conceptos básicos/ahorro/presupuesto/bancos]: ").strip()
    difficulty = input("  Dificultad [fácil/medio]: ").strip()

    params = {}
    if category:
        params["category"] = category
    if difficulty:
        params["difficulty"] = difficulty

    data = request("GET", "/lecciones", params=params)
    if not data:
        return

    lecciones = data.get("lecciones", [])
    print(f"\n  {'─'*62}")
    print(f"  {'ID':<6} {'DIFICULTAD':<10} {'🪙':>4}  LECCIÓN")
    print(f"  {'─'*62}")
    for l in lecciones:
        print(f"  {l['lesson_id']:<6} {l['difficulty']:<10} {l['coins_reward']:>4}  {l['title']}")
        print(f"         └─ {l['description'][:55]}...")
    print(f"  {'─'*62}")
    print(f"  Total: {data['count']} lecciones\n")


def hacer_leccion(kid_id: str):
    """Flujo completo: GET lección → responder preguntas → POST respuestas"""
    lesson_id = input("\n  ID de lección (Ej: L001): ").strip().upper()
    data = request("GET", f"/lecciones/{lesson_id}")

    if not data or "error" in data:
        print(f"\n  ❌ {data.get('error') if data else 'Error de conexión'}")
        return

    print(f"\n  {'═'*58}")
    print(f"  📖 {data['title']}")
    print(f"  {'═'*58}")
    print(f"  {data['description']}")
    print(f"  🏷  Categoría : {data['category']}")
    print(f"  🪙  Recompensa: {data['coins_reward']} monedas")
    input("\n  ¡Presiona Enter cuando estés listo para el quiz! 🎯 ")

    coins_total = 0
    questions   = data.get("questions", [])

    for i, q in enumerate(questions, start=1):
        print(f"\n  {'─'*50}")
        print(f"  Pregunta {i} de {len(questions)}")
        print(f"  {'─'*50}")
        print(f"\n  ❓ {q['question']}\n")
        for letra, texto in q["options"].items():
            print(f"     {letra}) {texto}")
        print()

        answer = input("  Tu respuesta (A/B/C/D): ").strip().upper()

        resp = request("POST", "/respuestas", {
            "kid_id":      kid_id,
            "lesson_id":   lesson_id,
            "question_id": q["question_id"],
            "answer":      answer,
        })

        if not resp:
            continue

        if resp.get("correct"):
            print(f"\n  ✅ ¡CORRECTO! +{resp['coins_earned']} 🪙")
            coins_total += resp["coins_earned"]
        else:
            print(f"\n  ❌ Respuesta incorrecta.")

        print(f"  💡 {resp.get('explanation')}")
        print(f"  {resp.get('encouragement')}")

    print(f"\n  {'═'*50}")
    print(f"  🎉 ¡Lección completada!")
    print(f"  🪙 Monedas ganadas: {coins_total}")
    print(f"  {'═'*50}\n")


def ver_perfil():
    """GET /api/estudiantes/<kid_id>"""
    kid_id = input("\n  ID del estudiante (Ej: kid_001): ").strip()
    data   = request("GET", f"/estudiantes/{kid_id}")

    if not data:
        return

    if "error" in data:
        print(f"\n  ❌ {data['error']}\n")
        return

    barra_llena = "█" * len(data["completed_lessons"])
    barra_vacia = "░" * (5 - len(data["completed_lessons"]))

    print(f"\n  {'═'*50}")
    print(f"  👤 {data['name']} ({data['age']} años)")
    print(f"  {'─'*50}")
    print(f"  🏅 Nivel         : {data['level']}")
    print(f"  🪙 Monedas       : {data['total_coins']}")
    print(f"  🔥 Racha         : {data['streak_days']} días seguidos")
    print(f"  📈 Progreso      : [{barra_llena}{barra_vacia}] {data['progress_percent']}%")
    print(f"  ✅ Completadas   : {', '.join(data['completed_lessons']) or 'Ninguna aún'}")
    print(f"  {'═'*50}\n")


def registrar_estudiante():
    """POST /api/estudiantes"""
    print("\n  📝 Registrar nuevo estudiante")
    print("  " + "─" * 30)
    name = input("  Nombre  : ").strip()
    age  = input("  Edad    : ").strip()

    try:
        age = int(age)
    except ValueError:
        print("\n  ❌ La edad debe ser un número.")
        return

    data = request("POST", "/estudiantes", {"name": name, "age": age})

    if data and data.get("success"):
        print(f"\n  ✅ {data['message']}")
        print(f"  🆔 Tu ID es: {data['kid_id']}  ← Guárdalo para iniciar sesión\n")
    elif data:
        print(f"\n  ❌ {data.get('error')}\n")


def ver_ranking():
    """GET /api/ranking"""
    data = request("GET", "/ranking")

    if not data:
        return

    ranking = data.get("ranking", [])
    print(f"\n  {'═'*52}")
    print(f"  🏆 TABLA DE CLASIFICACIÓN — Finance Kids")
    print(f"  {'═'*52}")
    print(f"  {'POS':<5} {'NOMBRE':<15} {'🪙 MONEDAS':>10} {'NIVEL':>6} {'✅ LECCS':>9}")
    print(f"  {'─'*52}")

    for entry in ranking:
        print(f"  {entry['medal']:<4}  {entry['name']:<15} "
              f"{entry['total_coins']:>10} 🪙  "
              f"Lv.{entry['level']:<3}  "
              f"{entry['completed']:>5} lecs")

    print(f"  {'═'*52}\n")


# ──────────────────────────────────────────────────────────────────
#  MENÚ PRINCIPAL
# ──────────────────────────────────────────────────────────────────

MENU = """
╔══════════════════════════════════════════════╗
║   🐷 FINANCE KIDS — Aprende Finanzas (REST)  ║
╠══════════════════════════════════════════════╣
║  1. Estado del servidor                      ║
║  2. Ver catálogo de lecciones                ║
║  3. Hacer una lección + quiz                 ║
║  4. Ver mi perfil y progreso                 ║
║  5. Registrar nuevo estudiante               ║
║  6. Ver tabla de clasificación               ║
║  7. Salir                                    ║
╚══════════════════════════════════════════════╝
"""

def main():
    kid_id = input("\n  👋 ¡Hola! ¿Cuál es tu ID de estudiante? (Ej: kid_001): ").strip()
    if not kid_id:
        kid_id = "kid_001"

    print(f"\n  ✅ ¡Bienvenido/a! Sesión iniciada como: {kid_id}")

    opciones = {
        "1": health_check,
        "2": ver_lecciones,
        "3": lambda: hacer_leccion(kid_id),
        "4": ver_perfil,
        "5": registrar_estudiante,
        "6": ver_ranking,
    }

    while True:
        print(MENU)
        opcion = input("  ¿Qué quieres hacer? (1-7): ").strip()

        if opcion in opciones:
            opciones[opcion]()
        elif opcion == "7":
            print("\n  🐷 ¡Hasta pronto! ¡Sigue aprendiendo! 🌟\n")
            sys.exit(0)
        else:
            print("\n  ⚠️  Opción inválida. Elige entre 1 y 7.\n")


if __name__ == "__main__":
    main()
