from typing import Dict, Tuple, List

Equipo = str
Registro = Dict[str, object]              # {'innovacion': int, 'presentacion': int, 'errores': bool}
Ronda = Dict[Equipo, Registro]            # {'EquipoA': {...}, 'EquipoB': {...}}
Acumulado = Dict[Equipo, Dict[str, int]]  # totales por equipo

def calcular_puntaje(reg: Registro) -> int:
    """+3*innovacion +1*presentacion -1 si errores True"""
    inn = int(reg.get('innovacion', 0))
    pre = int(reg.get('presentacion', 0))
    err = bool(reg.get('errores', False))
    return 3*inn + pre - (1 if err else 0)

def inicializar_acumulados(evaluaciones: List[Ronda]) -> Acumulado:
    equipos = set()
    for ronda in evaluaciones:
        equipos.update(ronda.keys())
    return {eq: {"innovacion":0, "presentacion":0, "errores":0, "mejores":0, "total":0}
            for eq in equipos}

def procesar_ronda(ronda: Ronda, acum: Acumulado) -> Tuple[Equipo, int, Dict[Equipo, int]]:
    # map(): aplica calcular_puntaje a cada equipo de la ronda
    puntajes = dict(map(lambda kv: (kv[0], calcular_puntaje(kv[1])), ronda.items()))

    # actualizar acumulados
    for eq, reg in ronda.items():
        acum[eq]["innovacion"]   += int(reg.get("innovacion", 0))
        acum[eq]["presentacion"] += int(reg.get("presentacion", 0))
        # filter(): contar 1 si hubo error True
        acum[eq]["errores"]      += len(list(filter(lambda x: x, [reg.get("errores", False)])))
        acum[eq]["total"]        += puntajes[eq]

    # MER
    mer_eq, mer_pts = max(puntajes.items(), key=lambda x: x[1])
    acum[mer_eq]["mejores"] += 1
    return mer_eq, mer_pts, puntajes

def tabla_ordenada(acum: Acumulado) -> List[Tuple]:
    filas = [(eq, d["innovacion"], d["presentacion"], d["errores"], d["mejores"], d["total"])
             for eq, d in acum.items()]
    filas.sort(key=lambda x: x[-1], reverse=True)  # ordenar por Total desc
    return filas

def imprimir_tabla(acum: Acumulado) -> None:
    filas = tabla_ordenada(acum)
    cab = ("Equipo", "Innovación", "Presentación", "Errores", "Mejores", "Total")
    w0 = max(len(cab[0]), max(len(f[0]) for f in filas)) if filas else len(cab[0])
    print(f"{cab[0]:<{w0}}  {cab[1]:>10}  {cab[2]:>13}  {cab[3]:>7}  {cab[4]:>7}  {cab[5]:>5}")
    print("-" * (w0 + 10 + 13 + 7 + 7 + 5 + 10))
    for e, inn, pre, err, mej, tot in filas:
        print(f"{e:<{w0}}  {inn:>10}  {pre:>13}  {err:>7}  {mej:>7}  {tot:>5}")
