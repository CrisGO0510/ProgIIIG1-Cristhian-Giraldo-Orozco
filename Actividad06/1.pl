% Padres y sus hijos
progenitor(abraham, herbert).
progenitor(abraham, homero).
progenitor(clancy, marge).
progenitor(clancy, patyy).
progenitor(clancy, selma).
progenitor(homero, bart).
progenitor(homero, lisa).
progenitor(homero, maggie).
progenitor(mona, herbert).
progenitor(mona, homero).
progenitor(jacqueline, marge).
progenitor(jacqueline, patyy).
progenitor(jacqueline, selma).
progenitor(marge, bart).
progenitor(marge, lisa).
progenitor(marge, maggie).
progenitor(selma, lingBouvier).

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

% Abuelo y abuela
abuelo_de(Abuelo, Nieto) :- 
    progenitor(Abuelo, Padre),
    progenitor(Padre, Nieto).

abuela_de(Abuela, Nieto) :- 
    progenitor(Abuela, Padre),
    progenitor(Padre, Nieto).

% Hermanos y hermanas
hermano_de(X, Y) :- 
    progenitor(P, X), 
    progenitor(P, Y), 
    X \= Y.

hermana_de(X, Y) :- 
    progenitor(P, X), 
    progenitor(P, Y), 
    X \= Y.

% Tíos y tías
tio_de(Tio, Sobrino) :- 
    progenitor(P, Sobrino),
    hermano_de(Tio, P).

tia_de(Tia, Sobrino) :- 
    progenitor(P, Sobrino),
    hermana_de(Tia, P).

% Primos
primo_de(Primo, Persona) :- 
    progenitor(P1, Primo),
    progenitor(P2, Persona),
    hermano_de(P1, P2).

prima_de(Prima, Persona) :- 
    progenitor(P1, Prima),
    progenitor(P2, Persona),
    hermana_de(P1, P2).
