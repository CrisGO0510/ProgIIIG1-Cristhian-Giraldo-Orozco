% Definición de conexiones (hechos)
conexion(vancouver, edmonton, 16).
conexion(vancouver, calgary, 13).
conexion(edmonton, saskatoon, 12).
conexion(calgary, edmonton, 4).
conexion(calgary, regina, 14).
conexion(saskatoon, calgary, 9).
conexion(regina, saskatoon, 7).
conexion(saskatoon, winnipeg, 20).
conexion(regina, winnipeg, 4).


% Regla para determinar si hay una conexión directa o indirecta
hay_conexion(X, Y) :- 
    conexion(X, Y, _).

hay_conexion(X, Y) :- 
    conexion(X, Z, _),
    hay_conexion(Z, Y).

% Regla para obtener el costo total de un camino
costo_camino(X, Y, Costo) :-
    conexion(X, Y, Costo).

costo_camino(X, Y, Costo) :-
    conexion(X, Z, C1),
    costo_camino(Z, Y, C2),
    Costo is C1 + C2.
