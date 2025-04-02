Aquí tienes el documento actualizado para que coincida con la nueva estructura basada en estructuras en `1.pl`:

---

# **Solución al Taller 1: Uso de estructuras en `1.pl`**

Este documento presenta la **solución a los problemas planteados en el Taller 1**, ahora con un enfoque basado en **estructuras**.  

---

## 📂 **Contenido del Archivo `1.pl`**

El archivo `1.pl` define hechos y reglas relacionadas con la genealogía de la familia Simpson, utilizando **estructuras** para representar relaciones de parentesco.

### 🔹 **Hechos**
- Se utilizan **estructuras** para almacenar los hijos de cada progenitor.
- Se evita la repetición de estructuras padre/madre con datos más organizados.

### 🔹 **Reglas**
- Se definen relaciones familiares **dinámicamente** mediante recorridos de estructuras.
- Se mantiene el código más limpio y eficiente.

---

## **⚡ Ejemplo de Uso**

### 📌 **Cargar el archivo en Prolog**
```prolog
?- consult('1.pl').
true.
```

### 📌 **Consultas básicas**

#### **👴👵 Consultando Abuelos**
```prolog
?- abuelo_de(abraham, bart).
true.
?- abuela_de(jacqueline, lisa).
true.
?- abuela_de(jacqueline, ling).
true.
```

#### **👨‍👩‍👧‍👦 Consultando Tíos y Tías**
```prolog
?- tio_de(herbert, bart).
true.
?- tia_de(patty, maggie).
true.
?- tia_de(marge, ling).
true.
```

#### **👦👧 Consultando Hermanos**
```prolog
?- hermano_de(bart, lisa).
true.
?- hermana_de(lisa, bart).
true.
?- hermana_de(lisa, ling).
false.
```

#### **👬 Consultando Primos**
```prolog
?- primo_de(bart, ling).
true.
?- primo_de(ling, maggie).
false.
?- prima_de(ling, maggie).
true.
?- prima_de(ling, bart).
true.
```

---

## 🎯 **Beneficios del Nuevo Enfoque con estructuras**
✅ **Código más estructurado y limpio.**  
✅ **Menos redundancia en la representación de datos.**  
✅ **Consultas más eficientes y fáciles de entender.**  

Este nuevo enfoque permite un **mejor manejo de la información genealógica** y facilita **futuras extensiones** del programa. 🚀