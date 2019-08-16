
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
newEq=apply(reverse{L1,L2,L3,M12,M13,M23},reverse{"Lam11_","Lam22_","Lam33_","Lam12_","Lam13_","Lam23_"},(i,j)->degMatrixEq(i,j));
newEq/(i->print("hom_variable_group "|demark(",",first i)|" ; "))
allEq=newEq/last//flatten//reverse;
count=0;
scan(#allEq,i->print("f"|i+count|" = "|(allEq#i#B'SectionString)|" ; "))
