syms x(t)
Dx = diff(x);

ode = diff(x,t,2) == -2*diff(x,t,1) -2*x+3*sin(t);
cond1 = x(0) == -1;
cond2 = Dx(0) == 5;
conds = [cond1 cond2];
xSol(t) = dsolve(ode,conds);
xSol = simplify(xSol)

a = 0;
b = 100;

fplot(xSol, [a b])