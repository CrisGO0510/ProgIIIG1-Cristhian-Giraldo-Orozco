% --- Estructura: persona(Nombre, Hijos, Eventos) ---

persona(homer, [bart, lisa], [
    evento(nacimiento, 1956),
    evento(graduacion_secundaria, 1974),
    evento(boda, 1980),
    evento(trabajo_planta_nuclear, 1981),
    evento(torneo_bolos, 1990),
    evento(gira_rock, 1993),
    evento(astronauta, 1994),
    evento(perdio_empleo, 1995)
]).

persona(marge, [bart, lisa], [
    evento(nacimiento, 1958),
    evento(graduacion_secundaria, 1976),
    evento(boda, 1980),
    evento(pintura_burns, 1992),
    evento(arresto, 1993),
    evento(hospital_psiquiatrico, 1997),
    evento(tele_realidad, 2001)
]).

persona(bart, [], [
    evento(nacimiento, 1980),
    evento(castigo_examen, 1990),
    evento(revolucion_escolar, 1991),
    evento(estrella_tv, 1993),
    evento(acto_heroico, 1995),
    evento(campeonato_deportivo, 1999),
    evento(expulsion_escuela, 2000)
]).

persona(lisa, [], [
    evento(nacimiento, 1982),
    evento(saxofon, 1988),
    evento(honores_academicos, 1993),
    evento(conversaciones_bleeding_gums, 1994),
    evento(vegetariana, 1995),
    evento(premio_ambiental, 1997),
    evento(presidenta_eeuu, 2010)
]).




linea_de_descendencia(Nombre, Descendencia) :-
    persona(Nombre, Hijos, _),
    linea_descendencia_rec(Hijos, Descendencia).

linea_descendencia_rec([], []).
linea_descendencia_rec([Hijo|Resto], [Hijo|DescendenciaResto]) :-
    linea_de_descendencia(Hijo, SubDescendencia),
    append(SubDescendencia, DescendenciaTemp, DescendenciaResto),
    linea_descendencia_rec(Resto, DescendenciaTemp).


evento_mas_reciente(Nombre, Evento) :-
    persona(Nombre, _, Eventos),
    max_evento(Eventos, Evento).

max_evento([E], E).
max_evento([evento(T1, A1), evento(_, A2)|Resto], Max) :-
    A1 >= A2,
    max_evento([evento(T1, A1)|Resto], Max).
max_evento([evento(_, A1), evento(T2, A2)|Resto], Max) :-
    A1 < A2,
    max_evento([evento(T2, A2)|Resto], Max).


historia_familiar(Nombre, EventosOrdenados) :-
    persona(Nombre, Hijos, EventosPropios),
    eventos_hijos(Hijos, EventosHijos),
    append(EventosPropios, EventosHijos, Todos),
    sort_eventos_por_anio(Todos, EventosOrdenados).

eventos_hijos([], []).
eventos_hijos([H|R], EventosTotales) :-
    persona(H, _, EventosH),
    eventos_hijos(R, Resto),
    append(EventosH, Resto, EventosTotales).

sort_eventos_por_anio(Eventos, Ordenados) :-
    predsort(comparar_eventos, Eventos, Ordenados).

comparar_eventos(Delta, evento(_, A1), evento(_, A2)) :-
    compare(Delta, A1, A2).
