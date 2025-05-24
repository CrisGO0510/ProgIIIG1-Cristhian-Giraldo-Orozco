from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Tuple, cast
import itertools
import json

BOARD_ROWS = 9
BOARD_COLS = 9


class Cell:
    """Clase base para las celdas del tablero."""

    def is_blocked(self) -> bool:
        return False

    def is_clue(self) -> bool:
        return False

    def is_empty(self) -> bool:
        return False


@dataclass
class BlockedCell(Cell):
    def is_blocked(self) -> bool:
        return True


@dataclass
class ClueCell(Cell):
    right: Optional[int] = None
    down: Optional[int] = None

    def is_clue(self) -> bool:
        return True


@dataclass
class EmptyCell(Cell):
    value: Optional[int] = None

    def is_empty(self) -> bool:
        return True

    def set_value(self, val: Optional[int]) -> None:
        self.value = val


@dataclass
class Board:
    cells: Dict[str, Cell] = field(default_factory=dict)

    def get_cell(self, coord: str) -> Cell:
        """Obtiene una celda dado su coordenada. Devuelve BlockedCell si no existe."""
        return self.cells.get(coord, BlockedCell())

    def set_cell(self, coord: str, cell: Cell) -> None:
        self.cells[coord] = cell

    def load_from_json(self, json_data):
        for row in range(9):
            for col in range(1, 10):
                coord = f"{chr(ord('A') + col - 1)}{row + 1}"
                self.cells[coord] = EmptyCell()

        for coord, data in json_data.items():
            if "blockedCell" in data and data["blockedCell"] is True:
                self.cells[coord] = BlockedCell()
            elif "clueCell" in data:
                clue = data["clueCell"]
                right = clue.get("right")
                down = clue.get("down")
                self.cells[coord] = ClueCell(right=right, down=down)

    def display(self):
        print("    " + "   ".join(chr(ord("A") + i) for i in range(9)))
        print("   ┌" + "───┬" * 8 + "───┐")

        for row in range(9):
            row_number = f"{row + 1:>2}"
            l1, l2, l3 = [], [], []

            for col in range(1, 10):
                coord = f"{chr(ord('A') + col - 1)}{row + 1}"
                cell = self.cells.get(coord, BlockedCell())

                if cell.is_blocked():
                    l1.append("███")
                    l2.append("███")
                    l3.append("███")
                elif cell.is_clue():
                    right = f"{cell.right:0>2}" if cell.right is not None else "  "
                    down = f"{cell.down:0>2}" if cell.down is not None else "  "
                    l1.append(f"\\{right}")
                    l2.append(" \\ ")
                    l3.append(f"{down}\\")
                elif cell.is_empty():
                    val = str(cell.value) if cell.value is not None else " "
                    l1.append("   ")
                    l2.append(f" {val} ")
                    l3.append("   ")

            print(f"{row_number} │" + "│".join(l1) + "│")
            print("   │" + "│".join(l2) + "│")
            print("   │" + "│".join(l3) + "│")

            if row < 8:
                print("   ├" + "───┼" * 8 + "───┤")
            else:
                print("   └" + "───┴" * 8 + "───┘")

    def generate_run_options(self, length: int, total: int) -> List[Tuple[int, ...]]:
        """Todas las asignaciones posibles (permutaciones sin repetición) que sumen `total`."""
        # Primero saco las combinaciones únicas y luego genero sus permutaciones:
        combos = [
            comb
            for comb in itertools.combinations(range(1, 10), length)
            if sum(comb) == total
        ]
        # Permuto cada combinación para cubrir todas las órdenes posibles en la run
        options = []
        for comb in combos:
            options.extend(itertools.permutations(comb))
        return options

    def find_runs(self) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
        """
        Devuelve dos diccionarios:
        - horizontal_runs: clave = coordenada de la ClueCell con atributo right != None,
          valor = lista de coordenadas de EmptyCell a la derecha hasta el siguiente bloque.
        - vertical_runs: clave = coordenada de la ClueCell con atributo down != None,
          valor = lista de coordenadas de EmptyCell hacia abajo hasta el siguiente bloque.
        """
        horiz = {}
        vert = {}
        for coord, cell in self.cells.items():
            if isinstance(cell, ClueCell):
                row = int(coord[1:])
                col = coord[0]

                if cell.right is not None:
                    seq = []
                    c = ord(col) + 1
                    while True:
                        key = f"{chr(c)}{row}"
                        if self.get_cell(key).is_empty():
                            seq.append(key)
                            c += 1
                        else:
                            break
                    horiz[coord] = seq

                if cell.down is not None:
                    seq = []
                    r = row + 1
                    while True:
                        key = f"{col}{r}"
                        if self.get_cell(key).is_empty():
                            seq.append(key)
                            r += 1
                        else:
                            break
                    vert[coord] = seq

        return horiz, vert

    def generate_combinations(
        self, length: int, total: int | None
    ) -> List[Tuple[int, ...]]:
        """
        Devuelve todas las tuplas de longitud `length` de dígitos 1–9,
        sin repetición, que sumen `total`.
        """
        return [
            comb
            for comb in itertools.permutations(range(1, 10), length)
            if sum(comb) == total
        ]

    def solve(self) -> bool:
        """
        Solver optimizado:
         - Cada run es (coord, 'H'|'V').
         - MRV dinámico + forward-checking incremental.
        """

        # 1) Detectar runs por separado
        horiz_runs, vert_runs = self.find_runs()

        # 2) Construyo un dict unificado de runs con claves (coord, direc)
        runs: Dict[Tuple[str, str], List[str]] = {}
        targets: Dict[Tuple[str, str], int] = {}

        for coord, cells in horiz_runs.items():
            runs[(coord, "H")] = cells
            targets[(coord, "H")] = cast(ClueCell, self.cells[coord]).right  # type: ignore
        for coord, cells in vert_runs.items():
            runs[(coord, "V")] = cells
            targets[(coord, "V")] = cast(ClueCell, self.cells[coord]).down  # type: ignore

        # 3) Precalcular dominios (permutaciones) para cada run
        run_options: Dict[Tuple[str, str], List[Tuple[int, ...]]] = {}
        for run_key, cells in runs.items():
            length = len(cells)
            total = targets[run_key]
            run_options[run_key] = self.generate_run_options(length, total)

        # 4) Mapear cada celda a las runs que la tocan
        cell_to_runs: Dict[str, List[Tuple[str, str]]] = {}
        for run_key, cells in runs.items():
            for c in cells:
                cell_to_runs.setdefault(c, []).append(run_key)

        # 5) Conjunto de runs sin asignar
        unassigned: Set[Tuple[str, str]] = set(runs)

        # 6) Backtracking con MRV dinámico y forward-checking ligero
        def backtrack() -> bool:
            if not unassigned:
                return True

            # Elijo la run con MENOS opciones (MRV)
            run_key = min(unassigned, key=lambda r: len(run_options[r]))
            cells = runs[run_key]

            for comb in run_options[run_key]:
                # 6.1) Compruebo consistencia con celdas ya fijadas
                valid = True
                for val, coord in zip(comb, cells):
                    existing = cast(EmptyCell, self.cells[coord]).value
                    if existing is not None and existing != val:
                        valid = False
                        break
                if not valid:
                    continue

                # 6.2) Asignación provisional
                for val, coord in zip(comb, cells):
                    self.cells[coord].value = val

                # 6.3) Forward‐checking: recorto dominios de runs vecinas
                changed: Dict[Tuple[str, str], List[Tuple[int, ...]]] = {}
                failure = False
                for coord in cells:
                    for other_run in cell_to_runs[coord]:
                        if other_run in unassigned and other_run is not run_key:
                            if other_run not in changed:
                                # guardo copia
                                changed[other_run] = run_options[other_run]
                                # filtro sólo opciones compatibles con los valores nuevos
                                new_dom = []
                                for oc in run_options[other_run]:
                                    ok = True
                                    for v, cc in zip(oc, runs[other_run]):
                                        ev = cast(EmptyCell, self.cells[cc]).value
                                        if ev is not None and ev != v:
                                            ok = False
                                            break
                                    if ok:
                                        new_dom.append(oc)
                                run_options[other_run] = new_dom
                            if not run_options[other_run]:
                                failure = True
                                break
                    if failure:
                        break

                # 6.4) Recurro si no fallo
                if not failure:
                    unassigned.remove(run_key)
                    if backtrack():
                        return True
                    unassigned.add(run_key)

                # 6.5) Deshago asignación y domino
                for other, old_dom in changed.items():
                    run_options[other] = old_dom
                for _, coord in zip(comb, cells):
                    self.cells[coord].value = None

            return False

        return backtrack()


def load_board_from_file(filename: str) -> Board:
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    board = Board()
    board.load_from_json(data)
    return board


if __name__ == "__main__":
    board = load_board_from_file("KK5IFCNZ.json")
    board.display()

    if board.solve():
        print("Solución encontrada:")
        board.display()
    else:
        print("No se encontró solución.")
