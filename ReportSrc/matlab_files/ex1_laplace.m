syms x(t)
Dx = diff(x);

ode = diff(x,t,2) == -2*diff(x,t,1) -2*x+3*sin(t);
odeLT = laplace(ode, t,s);

syms X_LT
odeLT = subs(odeLT, laplace(x,t,s), X_LT);

X_LT = solve(odeLT, X_LT);
xSol = ilaplace(X_LT, s, t);
xSol = simplify(xSol);
xSol = subs(xSol, [x(0) Dx(0)], [-1 5]);

fplot(xSol, [0 100])