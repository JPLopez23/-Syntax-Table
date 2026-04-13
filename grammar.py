from dataclasses import dataclass, field

EPSILON = 'ε'
EOF = '$'

class Gramatica:
    def __init__(self):
        self.producciones = {}
        self.no_terminales = []
        self.simbolo_inicial = None

    def agregar_produccion(self, no_terminal, produccion):
        if no_terminal not in self.producciones:
            self.producciones[no_terminal] = []
            self.no_terminales.append(no_terminal)
        if self.simbolo_inicial is None:
            self.simbolo_inicial = no_terminal
        self.producciones[no_terminal].append(produccion)

    def es_terminal(self, simbolo):
        return simbolo != EPSILON and simbolo not in self.producciones

    def get_terminales(self):
        terminales = set()
        for prods in self.producciones.values():
            for prod in prods:
                for s in prod:
                    if s != EPSILON and s not in self.producciones:
                        terminales.add(s)
        return terminales

    def __str__(self):
        lineas = []
        for nt in self.no_terminales:
            alternativas = ' | '.join(' '.join(p) for p in self.producciones[nt])
            lineas.append(f"{nt} → {alternativas}")
        return '\n'.join(lineas)