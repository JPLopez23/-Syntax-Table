# FIRST, FOLLOW y Tabla de Análisis Sintáctico Predictivo

## Descripción

Implementación en Python de los algoritmos FIRST, FOLLOW y construcción de tabla de análisis sintáctico predictivo LL(1) para gramáticas libres de contexto.

## Uso

```bash
# Ejecutar con las gramáticas de ejemplo incluidas
python main.py

# Modo interactivo: ingresa tu propia gramática
python main.py --interactive
```

## Formato de gramáticas

```
E -> T E'
E' -> + T E' | ε
T -> F T'
T' -> * F T' | ε
F -> ( E ) | id
```

- Usar `->` o `→` como separador
- Separar alternativas con `|`
- Usar `ε` o `eps` para producciones epsilon
- Los no-terminales se detectan automáticamente como los símbolos que aparecen a la izquierda de `→`

## Gramáticas probadas

### 1. Expresiones aritméticas (vista en clase)
```
E → T E'
E' → + T E' | ε
T → F T'
T' → * F T' | ε
F → ( E ) | id
```
**¿Es LL(1)?** Sí — no hay conflictos en la tabla.  
Esta gramática se eligió por ser el ejemplo canónico de gramática LL(1), ideal para verificar la corrección del algoritmo.

### 2. Sentencias condicionales (if-then-else)
```
S → if E then S S'
S' → else S | ε
E → id
```
**¿Es LL(1)?** No — conflicto en [S', else]: el famoso problema del "dangling else".  
Cuando el parser ve `else`, no puede decidir si aplica `S' → else S` o `S' → ε`. Esta gramática se eligió para demostrar que el programa detecta correctamente gramáticas no-LL(1) y reporta los conflictos.

### 3. Lista de expresiones separadas por comas
```
L → E L'
L' → , E L' | ε
E → id | num
```
**¿Es LL(1)?** Sí — no hay conflictos.  
Esta gramática representa un patrón muy común y se eligió para mostrar que el algoritmo maneja correctamente múltiples terminales en FIRST(E).

## Algoritmos implementados

### FIRST
El conjunto FIRST(X) contiene todos los terminales que pueden aparecer al inicio de una cadena derivable de X.

**Reglas:**
1. Si X es terminal: FIRST(X) = {X}
2. Si X → ε: ε ∈ FIRST(X)
3. Si X → Y₁Y₂...Yₖ: se agrega FIRST(Y₁) - {ε}. Si ε ∈ FIRST(Y₁), se agrega FIRST(Y₂) - {ε}, y así sucesivamente.

### FOLLOW
El conjunto FOLLOW(A) contiene todos los terminales que pueden aparecer inmediatamente después de A en alguna forma sentencial.

**Reglas:**
1. $ ∈ FOLLOW(S) donde S es el símbolo inicial
2. Si A → αBβ: FIRST(β) - {ε} ⊆ FOLLOW(B)
3. Si A → αBβ y ε ∈ FIRST(β): FOLLOW(A) ⊆ FOLLOW(B)
4. Si A → αB: FOLLOW(A) ⊆ FOLLOW(B)

### Tabla de análisis sintáctico LL(1)
Para cada producción A → α:
- Para cada terminal a ∈ FIRST(α): agregar A → α a tabla[A][a]
- Si ε ∈ FIRST(α): para cada terminal b ∈ FOLLOW(A), agregar A → α a tabla[A][b]

Una gramática es **LL(1)** si y sólo si no hay conflictos (cada celda tiene máximo una producción).
