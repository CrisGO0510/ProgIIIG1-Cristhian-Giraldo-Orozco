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
progenitor(abraham, homero).
progenitor(abraham, herbert).
progenitor(mona, homero).
progenitor(mona, herbert).

progenitor(clancy, marge).
progenitor(clancy, patty).
progenitor(clancy, selma).
progenitor(jacqueline, marge).
progenitor(jacqueline, patty).
progenitor(jacqueline, selma).

progenitor(homero, bart).
progenitor(homero, lisa).
progenitor(homero, maggie).
progenitor(marge, bart).
progenitor(marge, lisa).
progenitor(marge, maggie).

progenitor(selma, ling).

% Reglas

% Abuelo y abuela
es_abuelo(X, Y) :- progenitor(X, Z), progenitor(Z, Y), hombre(X).
es_abuela(X, Y) :- progenitor(X, Z), progenitor(Z, Y), mujer(X).

% Hermanos y hermanas
es_hermano(X, Y) :- progenitor(Z, X), progenitor(Z, Y), hombre(X), X \== Y.
es_hermana(X, Y) :- progenitor(Z, X), progenitor(Z, Y), mujer(X), X \== Y.

% Tíos y tías
es_tio(X, Y) :- progenitor(Z, Y), es_hermano(X, Z).
es_tia(X, Y) :- progenitor(Z, Y), es_hermana(X, Z).

% Primos y primas
es_primo(X, Y) :- progenitor(Z, X), progenitor(W, Y), es_hermano(Z, W), hombre(X).
es_prima(X, Y) :- progenitor(Z, X), progenitor(W, Y), es_hermana(Z, W), mujer(X).

% Nietos y nietas
es_nieto(X, Y) :- progenitor(Y, Z), progenitor(Z, X), hombre(X).
es_nieta(X, Y) :- progenitor(Y, Z), progenitor(Z, X), mujer(X).

% Sobrinos y sobrinas
es_sobrino(X, Y) :- progenitor(Z, X), es_hermano(Z, Y), hombre(X).
es_sobrina(X, Y) :- progenitor(Z, X), es_hermana(Z, Y), mujer(X).
