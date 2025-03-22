factorial(0, 1). %caso base
factorial(X, F):-
  X > 0,
  X1 is X - 1,
  factorial(X1, F1),
  F is X * F1.

sumancubos(1, 1). %caso base
sumancubos(X, S):-
  X > 0,
  X1 is X - 1,
  sumancubos(X1, S1),
  S is X^3 + S1.
