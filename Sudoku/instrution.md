Claro, aquí tienes un `README.md` detallado que describe el propósito del proyecto y explica cada función a fondo:

---

# 🧠 Sudoku Solver con Restricciones (CSP)

Este proyecto resuelve sudokus aplicando **Programación con Restricciones (CSP)** utilizando Python. Cada celda se trata como una variable con dominio `{1, ..., 9}`, y se aplican restricciones de fila, columna y subcuadro de 3x3. El archivo de entrada contiene un sudoku con ceros (`0`) como espacios vacíos.

---

## 📄 Estructura del Archivo de Entrada

El archivo `sudoku.txt` debe contener 9 líneas de 9 caracteres (números del 0 al 9), por ejemplo:

```
530070000
600195000
098000060
800060003
400803001
700020006
060000280
000419005
000080079
```

* Los **ceros (`0`)** indican celdas vacías.
* Cada línea representa una **fila del sudoku** de arriba a abajo.

---

## 🧩 Descripción de Funciones

### `init_variables()`

```python
def init_variables():
```

Inicializa todas las celdas posibles del tablero de sudoku como variables. Cada celda es identificada por coordenadas tipo `"A1"`, `"B2"`, etc.

* El dominio inicial de cada celda es `{1,2,...,9}`.
* Se utiliza el producto cartesiano de filas (1-9) y columnas (A-I).

### `load_board(filename)`

```python
def load_board(filename):
```

Lee el archivo de entrada (`sudoku.txt`) y construye un diccionario `board` con las celdas que tienen valores fijos (≠ 0).

* Las claves están en formato `"A1"`, `"B2"`, etc.
* Los valores son enteros del 1 al 9.

### `apply_initial_constraints(vars_dict, board)`

```python
def apply_initial_constraints(vars_dict, board):
```

Aplica las restricciones iniciales del sudoku:

* Reemplaza el dominio de cada celda predefinida por un conjunto unitario `{valor}`.
* Este paso fija los valores dados y reduce el espacio de búsqueda.

### `remove_from_domain(vars_dict, key, value)`

```python
def remove_from_domain(vars_dict, key, value):
```

Elimina un valor específico del dominio de una celda. Esta función es útil para la propagación de restricciones y algoritmos como AC-3 o Forward Checking (aunque no están implementados aún).

### `print_board(board)`

```python
def print_board(board):
```

Imprime el estado actual del tablero en un formato visual tipo sudoku.

* Se reemplazan las celdas vacías con `"."`.
* Agrupa las celdas en regiones de 3x3 con líneas divisorias.

Ejemplo de salida:

```
  A B C   D E F   G H I
1 5 3 . | . 7 . | . . .
2 6 . . | 1 9 5 | . . .
3 . 9 8 | . . . | . 6 .
  ------+-------+------
...
```

### `main(board)`

```python
def main(board):
```

Función principal que:

* Inicializa las variables con dominios `{1..9}`.
* Aplica las restricciones del tablero (`board`).
* Muestra los dominios de cada celda antes y después de aplicar las restricciones.

---

## 🚀 Cómo ejecutar

1. Asegúrate de tener un archivo `sudoku.txt` con un tablero válido.
2. Ejecuta el script:

```bash
python sudoku_solver.py
```

---

## 🔧 Próximas mejoras (sugeridas)

* Implementar propagación de restricciones (AC-3).
* Resolver el sudoku completamente con búsqueda (backtracking).
* Añadir contador de pasos o visualización gráfica del proceso.

---

¿Quieres que también genere un archivo `README.md` listo para guardar o subir a GitHub?
