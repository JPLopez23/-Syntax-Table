from grammar import Gramatica, EPSILON, EOF

def first_secuencia(gramatica, simbolos, conjuntos_first):
    resultado = set()

    if not simbolos or simbolos == [EPSILON]:
        return {EPSILON}

    for simbolo in simbolos:
        if simbolo == EPSILON:
            resultado.add(EPSILON)
            break
        elif gramatica.es_terminal(simbolo):
            resultado.add(simbolo)
            break
        else:
            first_simbolo = conjuntos_first.get(simbolo, set())
            resultado |= first_simbolo - {EPSILON}
            if EPSILON not in first_simbolo:
                break
    else:
        resultado.add(EPSILON)

    return resultado


def calcular_first(gramatica):
    first = {nt: set() for nt in gramatica.no_terminales}

    cambio = True
    while cambio:
        cambio = False
        for nt in gramatica.no_terminales:
            for produccion in gramatica.producciones[nt]:
                nuevos = first_secuencia(gramatica, produccion, first)
                antes = len(first[nt])
                first[nt] |= nuevos
                if len(first[nt]) != antes:
                    cambio = True

    return first


def calcular_follow(gramatica, first):
    follow = {nt: set() for nt in gramatica.no_terminales}
    follow[gramatica.simbolo_inicial].add(EOF)

    cambio = True
    while cambio:
        cambio = False
        for nt in gramatica.no_terminales:
            for produccion in gramatica.producciones[nt]:
                for i, simbolo in enumerate(produccion):
                    if simbolo not in gramatica.producciones:
                        continue
                    resto = produccion[i + 1:]
                    first_resto = first_secuencia(gramatica, resto, first)
                    antes = len(follow[simbolo])
                    follow[simbolo] |= first_resto - {EPSILON}
                    if EPSILON in first_resto or not resto:
                        follow[simbolo] |= follow[nt]
                    if len(follow[simbolo]) != antes:
                        cambio = True

    return follow