ultimo([Result], Result).						% Base
ultimo([_|L], Result) :- ultimo(L, Result).		% Recursividad

%ultimo([a, [b,c], 2], Ultimo).
