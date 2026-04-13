import sys
from grammar_parser import parsear_gramatica
from first_follow import calcular_first, calcular_follow
from parsing_table import construir_tabla, imprimir_tabla

GRAMATICAS = {
    "Expresiones Aritméticas": """
E -> T E'
E' -> + T E' | ε
T -> F T'
T' -> * F T' | ε
F -> ( E ) | id
""",
    "If-Then-Else": """
S -> if E then S S'
S' -> else S | ε
E -> id
""",
    "Lista de Expresiones": """
L -> E L'
L' -> , E L' | ε
E -> id | num
""",
}


def analizar(nombre, texto):
    gramatica = parsear_gramatica(texto)
    first = calcular_first(gramatica)
    follow = calcular_follow(gramatica, first)
    tabla, conflictos = construir_tabla(gramatica, first, follow)

    print("=" * 60)
    print(f"Gramática: {nombre}")
    print("=" * 60)
    print(gramatica)
    print()

    print("Conjuntos FIRST:")
    for nt in gramatica.no_terminales:
        print(f"  FIRST({nt}) = {{ {', '.join(sorted(first[nt]))} }}")
    print()

    print("Conjuntos FOLLOW:")
    for nt in gramatica.no_terminales:
        print(f"  FOLLOW({nt}) = {{ {', '.join(sorted(follow[nt]))} }}")
    print()

    print("Tabla de análisis sintáctico:")
    imprimir_tabla(gramatica, tabla)
    print()

    if not conflictos:
        print(" La gramática ES LL(1).")
    else:
        print(" La gramática NO es LL(1). Conflictos:")
        for nt, t in conflictos:
            prods = [f"{nt}→{' '.join(p)}" for p in tabla[nt][t]]
            print(f"  [{nt}, {t}]: {' / '.join(prods)}")
    print()


def modo_interactivo():
    print("Ingresa tu gramática (escribe FIN para terminar):")
    lineas = []
    while True:
        linea = input()
        if linea.strip().upper() == "FIN":
            break
        lineas.append(linea)
    analizar("Gramática personalizada", '\n'.join(lineas))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactivo":
        modo_interactivo()
    else:
        for nombre, texto in GRAMATICAS.items():
            analizar(nombre, texto)