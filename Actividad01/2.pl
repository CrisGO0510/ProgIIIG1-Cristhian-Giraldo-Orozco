% Hechos
estadounidense(west).
nacion_hostil(corea_del_norte).
vende_arma(west, corea_del_norte, misiles).

% Reglas
es_criminal(Persona) :- 
    (   estadounidense(Persona), 
        vende_arma(Persona, NacionHostil, Arma), 
        nacion_hostil(NacionHostil)
    ->  write(Persona), write(' vendió '), write(Arma), write(' a '), write(NacionHostil), nl
        ;   write(Persona), write(' no es un criminal.'), nl, fail
    ).
