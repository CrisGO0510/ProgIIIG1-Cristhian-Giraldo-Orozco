% Hechos

% Género
hombre(abraham).
hombre(clancy).
hombre(herbert).
hombre(homero).
hombre(bart).

mujer(mona).
mujer(jacqueline).
mujer(marge).
mujer(patty).
mujer(selma).
mujer(lisa).
mujer(maggie).
mujer(ling).

% Progenitores
progenitor(abraham, [herbert, homero]).

progenitor(mona, [herbert, homero]).

progenitor(clancy, [marge, patty, selma]).

progenitor(jacqueline, [marge, patty, selma]).

progenitor(homero, [bart, lisa, maggie]).

progenitor(marge, [bart, lisa, maggie]).

progenitor(selma, [ling]).

% Reglas

% Padre y madre
es_padre(X, Y) :-
    hombre(X),
    progenitor(X, Z),
    member(Y, Z).

es_madre(X, Y) :-
    mujer(X),
    progenitor(X, Z),
    member(Y, Z).

% Función auxiliar
es_progenitor([Head | Tail], Hijo) :-
    ( progenitor(Head, Hijos), member(Hijo, Hijos) ) -> true;
    es_progenitor(Tail, Hijo).

obtener_progenitores(Lista, Hijo) :-
    findall(Progenitor, (progenitor(Progenitor, Hijos), member(Hijo, Hijos)), Lista).

% Abuelo y abuela
es_abuelo(Abuelo, Nieto) :- 
    hombre(Abuelo),
    progenitor(Abuelo, ListaPadres),
    es_progenitor(ListaPadres, Nieto).

es_abuela(Abuela, Nieto) :- 
    mujer(Abuela),
    progenitor(Abuela, ListaPadres),
    es_progenitor(ListaPadres, Nieto).

% Hermanos y hermanas
es_hermano(X, Y) :- 
    hombre(X),
    X \== Y,
    obtener_progenitores(Z, X),
    es_progenitor(Z, Y).

es_hermana(X, Y) :- 
    mujer(X),
    X \== Y,
    obtener_progenitores(Z, X),
    es_progenitor(Z, Y).

    
% Tíos y tías
es_tio(X, Y) :- obtener_progenitores(L1, Y), 
    member(Z, L1),
    es_hermano(X, Z).

es_tia(X, Y) :- obtener_progenitores(L1, Y), 
    member(Z, L1),
    es_hermana(X, Z).

% Primos y primas
es_primo(X, Y) :- 
    hombre(X),
    obtener_progenitores(Z, X),
    obtener_progenitores(W, Y),
    member(Z1, Z),
    member(W1, W),
    (es_hermana(Z1, W1) ; es_hermano(Z1, W1)).

es_prima(X, Y) :- 
    mujer(X),
    obtener_progenitores(Z, X),
    obtener_progenitores(W, Y),
    member(Z1, Z),
    member(W1, W),
    (es_hermana(Z1, W1) ; es_hermano(Z1, W1)).