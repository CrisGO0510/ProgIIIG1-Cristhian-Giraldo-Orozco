# Solución al Taller 1: Uso de Archivos `1.pl`

Este documento presenta la **solución a los problemas planteados en el Taller 1**. [👉 **Click para ir al PDF**](Taller%201.pdf) pero esta vez usando listas, cambiando el enfoque de las reglas

---

## 📂 **Contenido del Archivo `1.pl`**

El archivo `1.pl` define hechos y reglas relacionados con relaciones familiares.

### 🔹 **Hechos**
- Definen información básica como género y relaciones de progenitores.

### 🔹 **Reglas**
- Determinan relaciones familiares derivadas, como abuelos, hermanos, tíos, primos.

### ⚡ **Ejemplo de Uso**

1. **Cargar el archivo en Prolog:**
   ```prolog
   ?- consult('1.pl').
   true.
   ```

2. **Consultas básicas:**
   ```prolog
    ?- es_abuelo(abraham, bart).
    true.
    ?- es_abuela(jacqueline, lisa).
    true.
    ?- es_abuela(jacqueline, ling).
    true.
   ```

   ```prolog
    ?- es_tio(herbert, bart).
    true .
    ?- es_tia(patty, maggie).
    true.
    ?- es_tia(marge, ling).
    true.
   ```

   ```prolog
    ?- es_hermano(bart, lisa).
    true.
    ?- es_hermana(lisa, bart).
    true.
    ?- es_hermana(lisa, ling).
    false.
   ```

   ```prolog
    ?- es_primo(bart, ling).
    true .
    ?- es_primo(ling, maggie).
    false.
    ?- es_prima(ling, maggie).
    true .
    ?- es_prima(ling, bart).
    true .
   ```
---