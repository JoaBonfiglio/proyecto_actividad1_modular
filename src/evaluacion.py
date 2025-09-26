# src/evaluacion.py — versión clara y simple (sin 'typing')

# Estructuras esperadas (referencia):
# - Registro (por equipo en una ronda): {"innovacion": int, "presentacion": int, "errores": bool}
# - Ronda completa: {"EquipoA": <registro>, "EquipoB": <registro>, ...}
# - Acumulados: {"EquipoA": {"innovacion": 0, "presentacion": 0, "errores": 0, "mejores": 0, "total": 0}, ...}

def calcular_puntaje(reg):
    """
    Calcula el puntaje de un equipo en una ronda.
    Fórmula: 3*innovacion + presentacion - (1 si errores == True)
    """
    inn = int(reg.get('innovacion', 0))
    pre = int(reg.get('presentacion', 0))
    err = bool(reg.get('errores', False))
    return 3 * inn + pre - (1 if err else 0)


def inicializar_acumulados(evaluaciones):
    """
    Crea el diccionario de acumulados para todos los equipos que aparezcan en las rondas.
    """
    equipos = set()
    for ronda in evaluaciones:
        equipos.update(ronda.keys())

    acum = {
        eq: {"innovacion": 0, "presentacion": 0, "errores": 0, "mejores": 0, "total": 0}
        for eq in equipos
    }
    return acum


def procesar_ronda(ronda, acum):
    """
    Procesa una ronda:
      - Calcula los puntos de cada equipo usando calcular_puntaje
      - Actualiza acumulados (innovación, presentación, errores, total)
      - Determina el/los Mejores de la Ronda (soporta empates) y suma 1 en 'mejores' a cada uno
    return: (mer_equipos, mer_puntos, puntajes) -> (list[str], int, dict[str,int])
    """
    # 1) Puntajes de ESTA ronda por equipo
    puntajes = {}
    for eq, reg in ronda.items():
        puntajes[eq] = calcular_puntaje(reg)

    # 2) Actualizar acumulados
    for eq, reg in ronda.items():
        acum[eq]["innovacion"]   += int(reg.get("innovacion", 0))
        acum[eq]["presentacion"] += int(reg.get("presentacion", 0))
        if bool(reg.get("errores", False)):
            acum[eq]["errores"] += 1
        acum[eq]["total"] += puntajes[eq]

    # 3) Mejores de la Ronda (MER) con empate
    max_puntos = max(puntajes.values())
    mer_equipos = [eq for eq, pts in puntajes.items() if pts == max_puntos]

    # Contar "mejores" a todos los empatados
    for eq in mer_equipos:
        acum[eq]["mejores"] += 1

    return mer_equipos, max_puntos, puntajes


def tabla_ordenada(acum):
    """
    Convierte 'acum' en lista de filas y la ordena por 'total' descendente.
    return: lista de tuplas (equipo, innovacion, presentacion, errores, mejores, total)
    """
    filas = []
    for eq, d in acum.items():
        filas.append((eq, d["innovacion"], d["presentacion"], d["errores"], d["mejores"], d["total"]))
    filas.sort(key=lambda x: x[-1], reverse=True)  # ordenar por Total desc
    return filas


def imprimir_tabla(acum):
    """
    Imprime la tabla de ACUMULADOS ordenada por puntaje total (desc).
    """
    filas = tabla_ordenada(acum)
    cab = ("Equipo", "Innovación", "Presentación", "Errores", "Mejores", "Total")

    # ancho dinámico para la columna Equipo
    w0 = max(len(cab[0]), max((len(f[0]) for f in filas), default=0))
    print(f"{cab[0]:<{w0}}  {cab[1]:>10}  {cab[2]:>13}  {cab[3]:>7}  {cab[4]:>7}  {cab[5]:>5}")
    print("-" * (w0 + 10 + 13 + 7 + 7 + 5 + 10))
    for e, inn, pre, err, mej, tot in filas:
        print(f"{e:<{w0}}  {inn:>10}  {pre:>13}  {err:>7}  {mej:>7}  {tot:>5}")


# ---------- utilidades para resultados por ronda (independientes del acumulado) ----------

def tabla_ronda(ronda):
    """
    Convierte una RONDA en una lista de filas y la ordena por el puntaje de ESA ronda (desc).
    return: lista de tuplas (equipo, innovacion, presentacion, errores(int), total_ronda)
    """
    filas = []
    for eq, reg in ronda.items():
        inn = int(reg.get("innovacion", 0))
        pre = int(reg.get("presentacion", 0))
        err = 1 if bool(reg.get("errores", False)) else 0
        tot_r = calcular_puntaje(reg)
        filas.append((eq, inn, pre, err, tot_r))
    filas.sort(key=lambda x: x[-1], reverse=True)
    return filas

def imprimir_tabla_ronda(ronda):
    """
    Imprime la tabla de resultados de la RONDA (independiente del acumulado).
    """
    filas = tabla_ronda(ronda)
    cab = ("Equipo", "Innovación", "Presentación", "Errores", "Total Ronda")
    w0 = max(len(cab[0]), max((len(f[0]) for f in filas), default=0))
    print(f"{cab[0]:<{w0}}  {cab[1]:>10}  {cab[2]:>13}  {cab[3]:>7}  {cab[4]:>12}")
    print("-" * (w0 + 10 + 13 + 7 + 12 + 10))
    for e, inn, pre, err, tot_r in filas:
        print(f"{e:<{w0}}  {inn:>10}  {pre:>13}  {err:>7}  {tot_r:>12}")

def equipos_ganadores(acum):
    """
    Devuelve (lista_de_ganadores, max_total) en el ACUMULADO, soportando empates.
    """
    if not acum:
        return [], 0
    max_total = max(d["total"] for d in acum.values())
    ganadores = [eq for eq, d in acum.items() if d["total"] == max_total]
    return ganadores, max_total
