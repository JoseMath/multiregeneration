R=QQ[{a1, mu1, s1, h1}]**QQ[{a2, mu2, s2, h2}]
for i to 7-1 do value("m"|i|" = "|toString(random(1,19999)))

f0 = -m0*h1*h2 + a1*h2+a2*h1  ;
f1 = -m1*h1^2*h2^2 + (a1*mu1)*h2^2  +(a2*mu2)*h1^2  ;
f2 = -m2*h1^3*h2^3 + a1*(mu1^2 +  s1^2)*h2^3 +       a2*(mu2^2+s2^2)*h1^3  ;
f3 = -m3*h1^4*h2^4 + a1*(mu1^3 +  3*mu1*s1^2)*h2^4 +          a2*(mu2^3+ 3*mu2*s2^2)*h1^4 ;
f4 = -m4*h1^5*h2^5 + a1*(mu1^4 +  6*mu1^2*s1^2+ 3*s1^4)*h2^5+     a2*(mu2^4+ 6*mu2^2*s2^2+ 3*s2^4)*h1^5 ;
f5 = -m5*h1^6*h2^6 + a1*(mu1^5 + 10*mu1^3*s1^2+ 15*mu1*s1^4)*h2^6   +a2*(mu2^5+ 10*mu2^3*s2^2+ 15*mu2*s2^4)*h1^6 ;
getInfo=(I)->(multidegree I;
  D:=decompose I;
  D/multidegree//netList//print;
  return D)
I=ideal(f0,f1)--3
getInfo(I)

I=ideal(f0,f1,f2) --6
getInfo(I)

I=ideal(f0,f1,f2,f3) --21
getInfo(I)

I=ideal(f0,f1,f2,f3,f4) --
getInfo(I)


I=ideal(f1)--2
getInfo(I)

I=ideal(f1,f2) --10
getInfo(I)

I=ideal(f1,f2,f3) --
getInfo(I)

I=ideal(f1,f2,f3,f4) --
getInfo(I)
