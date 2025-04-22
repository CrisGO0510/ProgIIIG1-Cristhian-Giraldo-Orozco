% Piezas basicas
pieza(llanta, []).
pieza(radios, []).
pieza(eje, []).
pieza(manillar, []).
pieza(sillin, []).
pieza(plato, []).
pieza(pedales, []).
pieza(cadena, []).
pieza(pinones, []).

% Piezas compuestas
pieza(traccion, [eje, plato, pedales, cadena]).
pieza(rueda_delantera, [llanta, radios, eje]).
pieza(cuadro, [manillar, sillin, traccion]).
pieza(rueda_trasera, [llanta, radios, eje, pinones]).
pieza(bicicleta, [rueda_delantera, cuadro, rueda_trasera]).

% Caso base: Si la lista de componentes esta vacia, es una pieza basica
obtener_piezas_basicas([], []).

obtener_piezas_basicas([Componente | Resto], ListaBasicosFinal) :-
  (pieza(Componente, []) ->
    obtener_piezas_basicas(Resto, RestoBasicas),
    ListaBasicosFinal = [Componente | RestoBasicas]
; 
    % Si no es básico, explorar sus hijos recursivamente
    componentes(Componente, SubBasicos),
    obtener_piezas_basicas(Resto, RestoBasicos),
    append(SubBasicos, RestoBasicos, ListaBasicosFinal)
  ).

% Obtener solo los componentes basicos (hojas del arbol)
componentes(Pieza, ComponentesBasicos) :-
    pieza(Pieza, Hijos),
    obtener_piezas_basicas(Hijos, ComponentesBasicos).

