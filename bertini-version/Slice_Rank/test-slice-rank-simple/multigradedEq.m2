
-* Used to create the L1,L2,L3
replace("K","3","LK=matrix{
    {p11K,p12K,p13K},
    {p21K,p22K,p23K},
    {p31K,p32K,p33K}}"    )
*-

--We start with 27 unknowns and 2 parameters (r,s)
R=QQ[flatten {
    {p111, p112, p113, p121, p122, p123, p131, p132, p133},
    {p211, p212, p213, p221, p222, p223, p231, p232, p233},
    {p311, p312, p313, p321, p322, p323, p331, p332, p333}}]**QQ[r,s]
gens R
L1=matrix{
           {p111,p121,p131},
           {p211,p221,p231},
           {p311,p321,p331}}
L2=matrix{
           {p112,p122,p132},
           {p212,p222,p232},
           {p312,p322,p332}}
L3=matrix{
          {p113,p123,p133},
          {p213,p223,p233},
          {p313,p323,p333}}

(M12,M13,M23)=toSequence apply(subsets({1,2,3},2),i-> (value("L"|i_0)||value("L"|i_1))|((diagonalMatrix{r,r,r})||(diagonalMatrix{s,s,s})))
(M11,M22,M33)=toSequence apply({1,2,3},i-> (value("L"|i)||value("L"|i))|((diagonalMatrix{r,r,r})||(diagonalMatrix{s,s,s})))
loadPackage"Bertini"
degMatrixEq=(M,s)->(
	S:=for i to numRows M-1 list (s|i);
	return(S,	for c in entries transpose M list makeB'Section(c,B'NumberCoefficients=>S))
	);
newEq=apply({M12,M13,M23},{"Lam12_","Lam13_","Lam23_"},(i,j)->degMatrixEq(i,j));
newEq/(i->print("hom_variable_group "|demark(",",first i)|" ; "))
allEq=newEq/last//flatten;
count=0;
scan(#allEq,i->print("f"|i+count|" = "|(allEq#i#B'SectionString)|" ; "))


newEq=apply({M11,M22,M33,M12,M13,M23},{"Lam11_","Lam22_","Lam33_","Lam12_","Lam13_","Lam23_"},(i,j)->degMatrixEq(i,j));
newEq/(i->print("hom_variable_group "|demark(",",first i)|" ; "))
allEq=newEq/last//flatten;
count=0;
scan(#allEq,i->print("f"|i+count|" = "|(allEq#i#B'SectionString)|" ; "))



f0 = (Lam11_0)*(p111)+(Lam11_1)*(p211)+(Lam11_2)*(p311)+(Lam11_3)*(p111)+(Lam11_4)*(p211)+(Lam11_5)*(p311) ;
f1 = (Lam11_0)*(p121)+(Lam11_1)*(p221)+(Lam11_2)*(p321)+(Lam11_3)*(p121)+(Lam11_4)*(p221)+(Lam11_5)*(p321) ;
f2 = (Lam11_0)*(p131)+(Lam11_1)*(p231)+(Lam11_2)*(p331)+(Lam11_3)*(p131)+(Lam11_4)*(p231)+(Lam11_5)*(p331) ;
f3 = (Lam11_0)*(r)+(Lam11_1)*(0)+(Lam11_2)*(0)+(Lam11_3)*(s)+(Lam11_4)*(0)+(Lam11_5)*(0) ;
f4 = (Lam11_0)*(0)+(Lam11_1)*(r)+(Lam11_2)*(0)+(Lam11_3)*(0)+(Lam11_4)*(s)+(Lam11_5)*(0) ;
f5 = (Lam11_0)*(0)+(Lam11_1)*(0)+(Lam11_2)*(r)+(Lam11_3)*(0)+(Lam11_4)*(0)+(Lam11_5)*(s) ;
f6 = (Lam22_0)*(p112)+(Lam22_1)*(p212)+(Lam22_2)*(p312)+(Lam22_3)*(p112)+(Lam22_4)*(p212)+(Lam22_5)*(p312) ;
f7 = (Lam22_0)*(p122)+(Lam22_1)*(p222)+(Lam22_2)*(p322)+(Lam22_3)*(p122)+(Lam22_4)*(p222)+(Lam22_5)*(p322) ;
f8 = (Lam22_0)*(p132)+(Lam22_1)*(p232)+(Lam22_2)*(p332)+(Lam22_3)*(p132)+(Lam22_4)*(p232)+(Lam22_5)*(p332) ;
f9 = (Lam22_0)*(r)+(Lam22_1)*(0)+(Lam22_2)*(0)+(Lam22_3)*(s)+(Lam22_4)*(0)+(Lam22_5)*(0) ;
f10 = (Lam22_0)*(0)+(Lam22_1)*(r)+(Lam22_2)*(0)+(Lam22_3)*(0)+(Lam22_4)*(s)+(Lam22_5)*(0) ;
f11 = (Lam22_0)*(0)+(Lam22_1)*(0)+(Lam22_2)*(r)+(Lam22_3)*(0)+(Lam22_4)*(0)+(Lam22_5)*(s) ;
f12 = (Lam33_0)*(p113)+(Lam33_1)*(p213)+(Lam33_2)*(p313)+(Lam33_3)*(p113)+(Lam33_4)*(p213)+(Lam33_5)*(p313) ;
f13 = (Lam33_0)*(p123)+(Lam33_1)*(p223)+(Lam33_2)*(p323)+(Lam33_3)*(p123)+(Lam33_4)*(p223)+(Lam33_5)*(p323) ;
f14 = (Lam33_0)*(p133)+(Lam33_1)*(p233)+(Lam33_2)*(p333)+(Lam33_3)*(p133)+(Lam33_4)*(p233)+(Lam33_5)*(p333) ;
f15 = (Lam33_0)*(r)+(Lam33_1)*(0)+(Lam33_2)*(0)+(Lam33_3)*(s)+(Lam33_4)*(0)+(Lam33_5)*(0) ;
f16 = (Lam33_0)*(0)+(Lam33_1)*(r)+(Lam33_2)*(0)+(Lam33_3)*(0)+(Lam33_4)*(s)+(Lam33_5)*(0) ;
f17 = (Lam33_0)*(0)+(Lam33_1)*(0)+(Lam33_2)*(r)+(Lam33_3)*(0)+(Lam33_4)*(0)+(Lam33_5)*(s) ;
f18 = (Lam12_0)*(p111)+(Lam12_1)*(p211)+(Lam12_2)*(p311)+(Lam12_3)*(p112)+(Lam12_4)*(p212)+(Lam12_5)*(p312) ;
f19 = (Lam12_0)*(p121)+(Lam12_1)*(p221)+(Lam12_2)*(p321)+(Lam12_3)*(p122)+(Lam12_4)*(p222)+(Lam12_5)*(p322) ;
f20 = (Lam12_0)*(p131)+(Lam12_1)*(p231)+(Lam12_2)*(p331)+(Lam12_3)*(p132)+(Lam12_4)*(p232)+(Lam12_5)*(p332) ;
f21 = (Lam12_0)*(r)+(Lam12_1)*(0)+(Lam12_2)*(0)+(Lam12_3)*(s)+(Lam12_4)*(0)+(Lam12_5)*(0) ;
f22 = (Lam12_0)*(0)+(Lam12_1)*(r)+(Lam12_2)*(0)+(Lam12_3)*(0)+(Lam12_4)*(s)+(Lam12_5)*(0) ;
f23 = (Lam12_0)*(0)+(Lam12_1)*(0)+(Lam12_2)*(r)+(Lam12_3)*(0)+(Lam12_4)*(0)+(Lam12_5)*(s) ;
f24 = (Lam13_0)*(p111)+(Lam13_1)*(p211)+(Lam13_2)*(p311)+(Lam13_3)*(p113)+(Lam13_4)*(p213)+(Lam13_5)*(p313) ;
f25 = (Lam13_0)*(p121)+(Lam13_1)*(p221)+(Lam13_2)*(p321)+(Lam13_3)*(p123)+(Lam13_4)*(p223)+(Lam13_5)*(p323) ;
f26 = (Lam13_0)*(p131)+(Lam13_1)*(p231)+(Lam13_2)*(p331)+(Lam13_3)*(p133)+(Lam13_4)*(p233)+(Lam13_5)*(p333) ;
f27 = (Lam13_0)*(r)+(Lam13_1)*(0)+(Lam13_2)*(0)+(Lam13_3)*(s)+(Lam13_4)*(0)+(Lam13_5)*(0) ; 
f28 = (Lam13_0)*(0)+(Lam13_1)*(r)+(Lam13_2)*(0)+(Lam13_3)*(0)+(Lam13_4)*(s)+(Lam13_5)*(0) ;
f29 = (Lam13_0)*(0)+(Lam13_1)*(0)+(Lam13_2)*(r)+(Lam13_3)*(0)+(Lam13_4)*(0)+(Lam13_5)*(s) ;
f30 = (Lam23_0)*(p112)+(Lam23_1)*(p212)+(Lam23_2)*(p312)+(Lam23_3)*(p113)+(Lam23_4)*(p213)+(Lam23_5)*(p313) ;
f31 = (Lam23_0)*(p122)+(Lam23_1)*(p222)+(Lam23_2)*(p322)+(Lam23_3)*(p123)+(Lam23_4)*(p223)+(Lam23_5)*(p323) ;
f32 = (Lam23_0)*(p132)+(Lam23_1)*(p232)+(Lam23_2)*(p332)+(Lam23_3)*(p133)+(Lam23_4)*(p233)+(Lam23_5)*(p333) ;
f33 = (Lam23_0)*(r)+(Lam23_1)*(0)+(Lam23_2)*(0)+(Lam23_3)*(s)+(Lam23_4)*(0)+(Lam23_5)*(0) ;
f34 = (Lam23_0)*(0)+(Lam23_1)*(r)+(Lam23_2)*(0)+(Lam23_3)*(0)+(Lam23_4)*(s)+(Lam23_5)*(0) ;
f35 = (Lam23_0)*(0)+(Lam23_1)*(0)+(Lam23_2)*(r)+(Lam23_3)*(0)+(Lam23_4)*(0)+(Lam23_5)*(s) ;
