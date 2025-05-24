---

# 📝 **Instrucciones del Juego Kakuro (Solver Python)**

Este proyecto implementa un **solucionador automático** de Kakuro en Python, utilizando un tablero que se define a través de un archivo JSON. Kakuro es un puzzle numérico similar al crucigrama, pero usando números y sumas.

---

## 🧩 **¿Qué es Kakuro?**

Kakuro es un puzzle donde debes rellenar las casillas vacías con números del 1 al 9. Cada fila o columna (llamadas **runs**) tiene un número objetivo, que es la suma que deben alcanzar las casillas vacías de esa fila o columna.

**Reglas:**

* Usa números del 1 al 9.
* No repitas números dentro de una misma suma.
* Las casillas bloqueadas están marcadas y no se pueden usar.
* Las casillas de pista muestran la suma objetivo para las celdas a su derecha y/o debajo.

---

## 📄 **Estructura del archivo JSON**

El tablero del juego se carga desde un archivo JSON. Cada casilla del tablero se identifica mediante coordenadas, desde `A1` hasta `I9`.

El archivo JSON describe tres tipos de celdas:

### 1. Celda Bloqueada (`BlockedCell`):

```json
"A1": {
  "blockedCell": true
}
```

* Estas celdas son inaccesibles.

### 2. Celda con Pista (`ClueCell`):

```json
"C1": {
  "clueCell": {
    "right": null,
    "down": 28
  }
}
```

* Indican la suma objetivo para las celdas inmediatamente a su derecha (`right`) y/o debajo (`down`).
* `null` significa que no hay pista en esa dirección.

### 3. Celda Vacía (implícita):

* Las celdas vacías no necesitan definirse en el JSON, ya que se generan automáticamente cuando no están especificadas como bloqueadas o con pista.

---

## 🚀 **Cómo Ejecutar el Solver**

Para ejecutar el solucionador, debes seguir estos pasos:

### **Paso 1**: Crea o edita tu archivo JSON con la estructura anterior.

Ejemplo:

```json
{
  "A1": { "blockedCell": true },
  "B1": { "blockedCell": true },
  "C1": { "clueCell": { "right": null, "down": 28 } },
  "D1": { "clueCell": { "right": null, "down": 14 } },
  "E1": { "blockedCell": true },
  "...": "..."
}
```

Guarda este archivo con un nombre, por ejemplo: `mi_tablero.json`.

---

### **Paso 2**: Ejecuta el script Python.

En tu terminal:

```bash
python solver.py
```

Asegúrate que el archivo Python tenga esta línea apuntando a tu archivo JSON:

```python
if __name__ == "__main__":
    board = load_board_from_file("mi_tablero.json")  # cambia aquí el nombre del archivo
    board.display()

    if board.solve():
        print("Solución encontrada:")
        board.display()
    else:
        print("No se encontró solución.")
```

---

## 🔍 **Cómo funciona el solver internamente**

Este solver implementa un algoritmo avanzado de Backtracking optimizado, usando:

* **Minimum Remaining Values (MRV)**: Escoge siempre la fila o columna más restringida (menos opciones posibles) para avanzar más rápido en la solución.
* **Forward-checking**: Antes de continuar, elimina opciones inconsistentes, reduciendo el espacio de búsqueda.
* **Precalcula combinaciones** de sumas y permutaciones posibles.

Esto garantiza eficiencia y rapidez al resolver el puzzle.

---

## ✅ **Ejemplo de Uso**

Al ejecutar el solver verás inicialmente:

```
    A   B   C   D   E   F   G   H   I
   ┌───┬───┬───┬───┬───┬───┬───┬───┬───┐
 1 │███│███│\  │\  │███│\  │\  │███│███│
   │███│███│ \ │ \ │███│ \ │ \ │███│███│
   │███│███│28\│14\│███│22\│35\│███│███│
   ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
...
```

Después de resolver, muestra algo como:

```
Solución encontrada:
    A   B   C   D   E   F   G   H   I
   ┌───┬───┬───┬───┬───┬───┬───┬───┬───┐
 1 │███│███│\  │\  │███│\  │\  │███│███│
   │███│███│ \ │ \ │███│ \ │ \ │███│███│
   │███│███│28\│14\│███│22\│35\│███│███│
   ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
...
 2 │███│\11│ 8 │ 3 │\17│ 9 │ 8 │\  │███│
...
```

---

## 📌 **Notas Importantes**

* El solver es eficiente, pero puzzles extremadamente grandes podrían tomar un tiempo considerable.
* Siempre asegúrate de que el archivo JSON esté correctamente formateado para evitar errores.

---
