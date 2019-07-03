
--R=QQ[t]
R=QQ[t]**QQ[x1]

R=QQ[x,y]
loadPackage"Bertini"
f=random({3},R)+random({3},R)+random({1},R)+1
f=f+sub(f,{x=>y,y=>x})

g=random({3},R)+random({3},R)+random({1},R)+1
g=f+sub(g,{x=>y,y=>x})
netList bertiniZeroDimSolve (ideal(g,f))_*

r00=x-2
r01=x-3
r02=x-5
A=product{r00,r01,r02}
A=A*sub(A,{x=>y,y=>x})

S=R**QQ[t]


h=(1-t)*sub(g,S)+(t)*sub(A,S)
I=sub(ideal f,S)+ideal(h)
decompose sub(I,{t=>0})
degree ideal(f,A)
degree ideal(f,g)
decompose ideal (f,A)
oo/degree
