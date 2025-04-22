% 1. Elementos repetidos

% Caso base
sin_repetidos([]).

sin_repetidos([Cabeza|Cola]) :-
    \+ member(Cabeza, Cola),
    sin_repetidos(Cola).         

% 2. Conjunto vacío

vacio([]).

% 3. Unión de dos conjuntos

% Caso base
union([], Conjunto, Conjunto).

union([Cabeza|Cola], Conjunto, Union) :-
    member(Cabeza, Conjunto),
    union(Cola, Conjunto, Union).

union([Cabeza|Cola], Conjunto, [Cabeza|Union]) :-
    \+ member(Cabeza, Conjunto),
    union(Cola, Conjunto, Union).

% 4. Intersección de dos conuntos

% Caso base
interseccion([], _, []).

interseccion([Cabeza|Cola], Conjunto, [Cabeza|Interseccion]) :-
    member(Cabeza, Conjunto),
    interseccion(Cola, Conjunto, Interseccion).

interseccion([_|Cola], Conjunto, Interseccion) :-
    interseccion(Cola, Conjunto, Interseccion).

