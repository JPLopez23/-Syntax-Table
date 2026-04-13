from grammar import Gramatica, EPSILON

def parsear_gramatica(texto):
    g = Gramatica()
    lineas = [l.strip() for l in texto.strip().splitlines()
              if l.strip() and not l.strip().startswith('#')]

    for linea in lineas:
        if '→' in linea:
            partes = linea.split('→', 1)
        elif '->' in linea:
            partes = linea.split('->', 1)
        else:
            continue

        no_terminal = partes[0].strip()
        alternativas = [alt.strip() for alt in partes[1].split('|')]

        for alt in alternativas:
            simbolos = alt.split()
            produccion = [EPSILON if s in ('ε', 'eps', 'epsilon') else s
                          for s in simbolos]
            g.agregar_produccion(no_terminal, produccion if produccion else [EPSILON])

    return g