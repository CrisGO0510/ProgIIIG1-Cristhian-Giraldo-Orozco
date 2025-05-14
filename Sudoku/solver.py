import itertools

# Dominios y nombres de columnas
Dom = set(range(1, 10))
IdCols = "ABCDEFGHI"


# Inicializar todas las variables del tablero con su dominio completo
def init_variables():
    keys = list(itertools.product(range(1, 10), IdCols))
    strKeys = [f"{col}{row}" for row, col in keys]
    return {key: Dom.copy() for key in strKeys}


# Cargar valores iniciales del archivo de texto
def load_board(filename):
    board = {}
    rows = "123456789"
    cols = "ABCDEFGHI"
    with open(filename, "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            line = line.strip()
            for j, char in enumerate(line):
                if char != "0":
                    key = cols[j] + rows[i]
                    board[key] = int(char)
    return board


# Aplicar restricciones iniciales al dominio de las celdas
def apply_initial_constraints(vars_dict, board):
    for key, value in board.items():
        vars_dict[key] = {value}
    return vars_dict


# Construir red de vecinos para cada celda (fila, columna, bloque 3x3)
def get_neighbors():
    rows = "123456789"
    cols = "ABCDEFGHI"
    squares = [c + r for r in rows for c in cols]

    units = []

    for r in rows:
        units.append([c + r for c in cols])
    for c in cols:
        units.append([c + r for r in rows])
    for rs in ("123", "456", "789"):
        for cs in ("ABC", "DEF", "GHI"):
            units.append([c + r for r in rs for c in cs])

    neighbors = {}
    for square in squares:
        neighbors[square] = set(sum([unit for unit in units if square in unit], [])) - {
            square
        }
    return neighbors


# Imprimir tablero en formato visual
def print_board(board):
    rows = "123456789"
    cols = "ABCDEFGHI"

    def cell(key):
        return str(board.get(key, "."))

    print("\n  A B C   D E F   G H I")
    for i, r in enumerate(rows):
        row = [cell(c + r) for c in cols]
        if i % 3 == 0 and i != 0:
            print("  ------+-------+------")
        print(
            r
            + " "
            + " ".join(row[0:3])
            + " | "
            + " ".join(row[3:6])
            + " | "
            + " ".join(row[6:9])
        )


# Verifica si un valor puede asignarse a una celda sin violar restricciones
def is_consistent(var, value, assignment, neighbors):
    for neighbor in neighbors[var]:
        if neighbor in assignment and assignment[neighbor] == value:
            return False
    return True


# Seleccionar la siguiente celda no asignada (MRV)
def select_unassigned_variable(vars_dict, assignment):
    unassigned = [v for v in vars_dict if v not in assignment]
    return min(unassigned, key=lambda var: len(vars_dict[var]))


# Algoritmo de backtracking con forward checking
def backtrack(assignment, vars_dict, neighbors):
    if len(assignment) == len(vars_dict):
        return assignment

    var = select_unassigned_variable(vars_dict, assignment)
    for value in vars_dict[var]:
        if is_consistent(var, value, assignment, neighbors):
            assignment[var] = value
            removed = {}

            for neighbor in neighbors[var]:
                if neighbor not in assignment and value in vars_dict[neighbor]:
                    vars_dict[neighbor].remove(value)
                    removed[neighbor] = value

            result = backtrack(assignment, vars_dict, neighbors)
            if result:
                return result

            del assignment[var]
            for n, v in removed.items():
                vars_dict[n].add(v)

    return None


# Función principal
def main(board):
    vars_dict = init_variables()
    vars_dict = apply_initial_constraints(vars_dict, board)
    neighbors = get_neighbors()

    # Asignaciones iniciales
    assignment = {k: list(v)[0] for k, v in vars_dict.items() if len(v) == 1}

    # Resolver el sudoku
    result = backtrack(assignment, vars_dict, neighbors)

    # Mostrar resultados
    if result:
        print("\n✅ Sudoku resuelto:\n")
        print_board(result)
    else:
        print("\n❌ No se pudo resolver el Sudoku.")


# Punto de entrada
if __name__ == "__main__":
    filename = "sudoku.txt"
    board = load_board(filename)
    main(board)
