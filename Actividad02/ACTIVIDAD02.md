# Solución al Problema de Conexiones en Prolog

Este documento describe la implementación de un sistema en Prolog para determinar conexiones entre ciudades y calcular el costo total de un camino.

---

## 📂 **Contenido del Archivo `conexiones.pl`**

El archivo `conexiones.pl` define hechos y reglas relacionadas con conexiones entre ciudades y sus costos definido en [👉 **Click para ir al PDF**](03-Backtracking%20y%20SLD.pdf).

#### 1️⃣ Determinar si hay una conexión entre dos ciudades (directa o indirecta)
```prolog
hay_conexion(X, Y) :-
    conexion(X, Y, _).

hay_conexion(X, Y) :-
    conexion(X, Z, _),
    hay_conexion(Z, Y).
```

#### 2️⃣ Calcular el costo total de un camino entre dos ciudades
```prolog
costo_camino(X, Y, Costo) :-
    conexion(X, Y, Costo).

costo_camino(X, Y, Costo) :-
    conexion(X, Z, C1),
    costo_camino(Z, Y, C2),
    Costo is C1 + C2.
```

---

## ⚡ **Ejemplo de Uso**

1. **Cargar el archivo en Prolog:**
   ```prolog
   ?- consult('conexiones.pl').
   true.
   ```

2. **Verificar si hay conexión entre Vancouver y Winnipeg:**
   ```prolog
   ?- hay_conexion(vancouver, winnipeg).
   true.
   ```

3. **Calcular el costo de viajar de Vancouver a Winnipeg:**
   ```prolog
   ?- costo_camino(vancouver, winnipeg, Costo).
   Costo = 48.
   ```

---

## 🎯 **Conclusión**
Este programa en Prolog permite determinar si dos ciudades están conectadas directa o indirectamente y calcular el costo total del camino entre ellas. Es útil para aplicaciones de rutas y planificación de viajes.

