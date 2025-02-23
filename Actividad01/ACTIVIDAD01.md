# Solución al Taller 1: Uso de Archivos `1.pl` y `2.pl`

Este documento presenta la **solución a los problemas planteados en el Taller 1**. [👉 **Click para ir al PDF**](Taller%201.pdf) donde se explica cómo utilizar los archivos `1.pl` y `2.pl`. Estos archivos contienen hechos y reglas en Prolog, con ejemplos prácticos para ejecutar consultas y entender su funcionamiento.

---

## 📂 **Contenido del Archivo `1.pl`**

El archivo `1.pl` define hechos y reglas relacionados con relaciones familiares.

### 🔹 **Hechos**
- Definen información básica como género y relaciones de progenitores.

### 🔹 **Reglas**
- Determinan relaciones familiares derivadas, como abuelos, hermanos, tíos, primos, nietos y sobrinos.

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
   ```

   ```prolog
   ?- es_tia(patty, maggie).
   true.
   ```

   ```prolog
   ?- es_primo(bart, ling).
   true.
   ```

   ```prolog
   ?- es_sobrino(lisa, selma).
   true.
   ```

---

## 📂 **Contenido del Archivo `2.pl`**

El archivo `2.pl` describe un escenario legal donde se determina si una persona es criminal con base en hechos sobre la venta de armas.

### 🔹 **Hechos**
- Indican nacionalidad, venta de armas y naciones hostiles.

### 🔹 **Regla Principal**
- `es_criminal/1`: Determina si una persona es criminal si, siendo estadounidense, vende armas a una nación hostil.

### ⚡ **Ejemplo de Uso**

1. **Cargar el archivo en Prolog:**
   ```prolog
   ?- consult('2.pl').
   true.
   ```

2. **Realizar la consulta:**
   ```prolog
   ?- es_criminal(west).
   west vendió misiles a nacion_hostil.
   true.
   ```

   ```prolog
   ?- es_criminal(lucas).
   false.
   ```

## 📝 **Consejos Adicionales**
- Asegúrate de que los archivos `.pl` estén en el mismo directorio desde donde cargas Prolog.
- Usa `listing.` para ver los predicados cargados:
  ```prolog
  ?- listing.
  ```
- Emplea `halt.` para salir de Prolog:
  ```prolog
  ?- halt.
  ```

---

## 🎯 **Conclusión**

Con estos ejemplos y explicaciones, se presenta la **solución completa al Taller 1**, mostrando cómo los archivos `1.pl` y `2.pl` representan conocimientos y reglas en Prolog, y cómo realizar consultas para obtener resultados basados en la lógica definida.

