from grammar import EPSILON, EOF
from first_follow import first_secuencia

def construir_tabla(gramatica, first, follow):
    tabla = {nt: {} for nt in gramatica.no_terminales}
    conflictos = []

    for nt in gramatica.no_terminales:
        for produccion in gramatica.producciones[nt]:
            first_prod = first_secuencia(gramatica, produccion, first)

            for terminal in first_prod:
                if terminal == EPSILON:
                    continue
                if terminal not in tabla[nt]:
                    tabla[nt][terminal] = []
                if produccion not in tabla[nt][terminal]:
                    tabla[nt][terminal].append(produccion)
                    if len(tabla[nt][terminal]) > 1:
                        par = (nt, terminal)
                        if par not in conflictos:
                            conflictos.append(par)

            if EPSILON in first_prod:
                for terminal in follow[nt]:
                    if terminal not in tabla[nt]:
                        tabla[nt][terminal] = []
                    if produccion not in tabla[nt][terminal]:
                        tabla[nt][terminal].append(produccion)
                        if len(tabla[nt][terminal]) > 1:
                            par = (nt, terminal)
                            if par not in conflictos:
                                conflictos.append(par)

    return tabla, conflictos


def imprimir_tabla(gramatica, tabla):
    terminales = sorted(gramatica.get_terminales()) + [EOF]
    ancho_nt = max(len(nt) for nt in gramatica.no_terminales) + 2
    ancho_col = 18

    encabezado = f"{'':>{ancho_nt}}" + "".join(f"{t:^{ancho_col}}" for t in terminales)
    print(encabezado)
    print("-" * len(encabezado))

    for nt in gramatica.no_terminales:
        fila = f"{nt:>{ancho_nt}}"
        for t in terminales:
            prods = tabla[nt].get(t, [])
            if not prods:
                celda = ""
            elif len(prods) == 1:
                celda = f"{nt}→{' '.join(prods[0])}"
            else:
                celda = "[CONFLICTO]"
            fila += f"{celda:^{ancho_col}}"
        print(fila)