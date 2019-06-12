
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

--I is the subset of cubics we consider
I={M12,M13,M23}/det/(f->ideal last coefficients(f,Variables=>{r,s}))//flatten//sum
I=ideal {I_1,I_2,I_5,I_6,I_9}+ideal({L1,L2,L3}/det)
(numcols mingens I,numcols gens I)




---Now we want to test if another polynomial is in the ideal of I.
--Elina's tensor determinant
newMon=(sigma,tau,sigmaSign,tauSign)->(-1)^sigmaSign*(-1)^tauSign*value(
    "p1"|(sigma_0)|tau_(0))*value("p2"|(sigma_1)|tau_(1))*value("p3"|(sigma_2)|tau_(2))
newMon({1,2,3},{3,2,1},0,1)
P=permutations({1,2,3})
theSigns={0,1,1,2,2,1}
elina=sum sum apply(6,i->apply(6,j->newMon(P_i,P_j,theSigns_i,theSigns_j)))
size elina
elina % I
--The polynomial in our paper.
paper=sum sum apply(6,i->apply(6,j->newMon(P_i,P_j,theSigns_i,0)))
thursday=sum sum apply(6,i->apply(6,j->newMon(P_i,P_j,0,theSigns_j)))

paper=sum sum apply(6,i->apply(6,j->newMon(P_i,P_j,theSigns_i,0)))


size paper
paper % (I+ideal elina)
elina % (I+ideal paper)
--I+ideal paper==I+ideal elina

--Searching for a polynomial.
newMon2=(sigma,tau,sigmaSign,tauSign)->(-1)^sigmaSign*(-1)^tauSign * value(
    "p"|tau_(0)|"1"|(sigma_0))*value("p"|tau_(1)|"2"|(sigma_1))*value("p"|tau_(2)|"3"|(sigma_2))
thursday=sum sum apply(6,i->apply(6,j->newMon2(P_i,P_j,0,theSigns_j)))
sub(thursday,pSub)
ideal thursday==ideal paper

3+9+1+3+9-1-1


----Let's make a general point.

rp=(f)->(
    A1:=transpose matrix{for i to 3-1 list f()}*matrix{for i to 9-1 list f()};
    M:=matrix for i to 3-1 list for j to 3-1 list f();
    A2:=M|f()*M|f()*M;
    A1+A2
    )
newPoint=rp(()->random(1,1000))
pSub = apply(drop(gens R,-2),flatten entries newPoint,(i,j)->i=>j)
sub(mingens I, pSub)
sub(elina,pSub)
sub(paper,pSub)
sub(thursday,pSub)

---Let's find a generic point.
fixPFunction=(L,f)->apply(L,i->i=>f())
27-18
keep=apply({0,4,6,9,14,16,19,23,26},i->(gens R)_i)
#keep
fixP=fixPFunction(select(drop(gens R,-2),i->not member(i,keep)),()->random(1,10000))
I1=I+ideal paper
--decWin=decompose  ideal mingens sub(I1,fixP)
M13
---Stuck so we switch to numerics
loadPackage"Bertini"
hvg=transpose {
    {p111, p112, p113, p121, p122, p123, p131, p132, p133},
    {p211, p212, p213, p221, p222, p223, p231, p232, p233},
    {p311, p312, p313, p321, p322, p323, p331, p332, p333}}
--nineSlices=(L1||L2||L3)//entries/(i->makeB'Section i)
--nineMoreSlices={M12,M13,M23}/(i->submatrix(i,{0,1,2}))/transpose/entries //flatten/(i->makeB'Section i)
I={M12,M13,M23}/det/(f->ideal last coefficients(f,Variables=>{r,s}))//flatten//sum
I1=select(I_*,(i)->18==size i)
I=ideal {I1_0,I1_1,I1_2,I1_3,I1_4}+ideal({L1,L2,L3}/det)
makeB'InputFile(theDir,
    HomVariableGroup=> flatten hvg,
    B'Configs=>{UseRegeneration=>1,TrackType=>1,PrintPathProgress=>100,MultOneOnly=>1},
    B'Polynomials=>(I_*)/reverse
    )


--TWO
I={M12,M13,M23}/det/(f->ideal last coefficients(f,Variables=>{r,s}))//flatten//sum
I=ideal {I_1,I_2,I_5,I_6,I_9}+ideal({L1,L2,L3}/det)
makeB'InputFile(theDir|"2",
    HomVariableGroup=> flatten hvg,
    B'Configs=>{UseRegeneration=>1,TrackType=>1,PrintPathProgress=>100,MultOneOnly=>1,MAXNUMMONLINEARS=>500},
    B'Polynomials=>(I_*)/reverse
    )

--THREE
I={M12,M13,M23}/det/(f->ideal last coefficients(f,Variables=>{r,s}))//flatten//sum
I=ideal {I_1,I_2,I_5,I_6,I_9,I_10}+ideal({L1,L2}/det)+ideal paper
makeB'InputFile(theDir|"3",
    HomVariableGroup=> flatten hvg,
    B'Configs=>{UseRegeneration=>1,TrackType=>1,PrintPathProgress=>100,MultOneOnly=>1,MAXCODIMENSION=>8},
    B'Polynomials=>(I_*)
    )

printingPrecision=300
win=sortMainDataComponents importMainDataFile(theDir|"3");
pcoordinates=win#2#0//coordinates
apply(flatten hvg,pcoordinates,(i,j)->i=>j)
S=QQ[a1,a2,a3,b1,b2,b3,b4,b5,b6,b7,b8,b9,c1,c2,c3,d1,d2,d3,d4,d5,d6,d7,d8,d9]
V1=transpose matrix{{a1,a2,a3}}*matrix{{b1,b2,b3,b4,b5,b6,b7,b8,b9}};
V2=matrix{{d1,d2,d3},{d4,d5,d6},{d7,d8,d9}}
V2=c1*V2|c2*V2|c3*V2

evalJac=(F,v,p)->sub(
    diff(transpose matrix {v},matrix {F}),
     apply(flatten entries sub((V1+V2),matrix{p}),v,(i,j)->j=>i)
     )
p={99,2,0,1,0,0,0,0,0,0,0,0,1,0,0,1,2,3,5,13,17,19,23,29}
p=for i to 24-1 list random(1,1000)
v=drop(gens R,-2)
F=I_*
rank evalJac(F,v,p)
binomial(27,8)
coefficientRing R
evalJac(,
    I_*)
    help drop

fiberSolve=flatten entries transpose (V1+V2)-win#2#0//coordinates




makeB'InputFile(theDir,
    AffVariableGroup=> gens S,
    B'Configs=>{TrackType=>1,PrintPathProgress=>100,MultOneOnly=>1},
    B'Polynomials=>(fiberSolve)
    )


SL=apply(#gens S-(18+1),i->makeB'Section(gens S|{1}))

makeB'InputFile(theDir|"2",
    AffVariableGroup=> gens S,
    B'Configs=>{UseRegeneration=>1,TrackType=>0,PrintPathProgress=>100,MultOneOnly=>1},
    B'Polynomials=>SL|(fiberSolve)
    )





makeB'InputFile(theDir,
    HomVariableGroup=> hvg,
    B'Configs=>{UseRegeneration=>1},
--    B'Functions=>fixP,
    B'Polynomials=>drop(nineSlices,1)|drop(nineMoreSlices,1)|(I1_*)
    )
runBertini(store)


printingPrecision=300
loadPackage"Bertini"
importSolutionsFile(theDir,NameSolutionsFile=>"member_points")
sols=importSolutionsFile(theDir,NameSolutionsFile=>"member_points")
T=QQ[X_1..X_(#first sols)]
basis(2,T)
(B0,B1,B2) = toSequence for i to 2 list basis(i,T)
M = matrix for i in sols list { sub(B0|B1|B2,matrix{i}) }
print SVD M



--We want to test the multidimension.
-- scan(subsets(27,8),i->print (i=>rank submatrix(M,i,)))

computeMultidimension=(name,M)->(
    if fileExists(theDir|"/"|name) then error "File already exists";
    fn = openOut( theDir|"/"|name);
    scan(subsets(27,8),i->(
	fn << toString(rank submatrix(M,i,) => i);
	fn<< endl));
     close fn)

 scanLines(i->if first i ==="4" then print (i|" , "),"/Users/jo/Desktop/Dump/sr2_Dimension")
 help scanLines
 L/last

 apply(subsets(toList(0..26),1),i->apply( L/last,j->if (i<=j) then i else null));
 apply(subsets(toList(0..26),25),i->apply( L/last,j->if (i<=j) then i else null));
oo//flatten//tally

 L/last

 /()//flatten//tally

help subset






 ----OLD WORK
 restart
theK=3
sizeA={3,3,3}
pickType={1,1,0}
varSymbols=for i to #pickType-1 list i+1
theParameterization=apply(pickType,varSymbols,(s,v)->{
	for i to s-1 list for j from s to sizeA_(v-1)-1 list value("a"|v|"v"|i+1|"v"|j+1 ),
	for i to s-1 list for j to s-1 list value("c"|v|"v"|i+1|"v"|j+1 )	,
	for i to s-1 list for j from s to replace(v-1,1,sizeA)//product-1 list value("b"|v|"v"|i+1|"v"|j+1 )
	})
netList oo
R=QQ[flatten flatten flatten theParameterization,flatten flatten for i to sizeA_0-1 list for j to sizeA_1-1 list for k to sizeA_2-1 list value("p"|i+1|j+1|k+1),w]
pVars=flatten flatten for i to sizeA_0-1 list for j to sizeA_1-1 list for k to sizeA_2-1 list value("p"|i+1|j+1|k+1)
eVars=apply(pickType,varSymbols,(s,v)->{
	for i to s-1 list for j from s to sizeA_(v-1)-1 list value("a"|v|"v"|i+1|"v"|j+1 ),
	for i to s-1 list for j from s to replace(v-1,1,sizeA)//product-1 list value("b"|v|"v"|i+1|"v"|j+1 ),
	for i to s-1 list for j to s-1 list value("c"|v|"v"|i+1|"v"|j+1 )	})

theParameterization=apply(pickType,varSymbols,(s,v)->{
	transpose((diagonalMatrix for i to s-1 list 1)|matrix for i to s-1 list for j from s to sizeA_(v-1)-1 list value("a"|v|"v"|i+1|"v"|j+1 )),
	matrix for i to s-1 list for j to s-1 list value("c"|v|"v"|i+1|"v"|j+1 )	,
	(diagonalMatrix for i to s-1 list 1)|(matrix for i to s-1 list for j from s to replace(v-1,1,sizeA)//product-1 list value("b"|v|"v"|i+1|"v"|j+1 ))
	})
netList theParameterization

M0=matrix for i to sizeA_0-1 list flatten for j to sizeA_1-1 list for k to sizeA_2-1 list value("p"|i+1|j+1|k+1)

allM=for i to #pickType-1 list ((theParameterization_i)_0)*((theParameterization_i)_1)*((theParameterization_i)_2)
M1=((theParameterization_0)_0)*((theParameterization_0)_1)*((theParameterization_0)_2)
M2=((theParameterization_1)_0)*((theParameterization_1)_1)*((theParameterization_1)_2)


bigM=sum {
	matrix for i to sizeA_0-1 list flatten for j to sizeA_1-1 list for k to sizeA_2-1 list M1_(i,j+sizeA_1*k),
	w*matrix for i to sizeA_0-1 list flatten for j to sizeA_1-1 list for k to sizeA_2-1 list M2_(j,i+sizeA_2*k)}
I=ideal(M0-bigM)

---OK we want to get some determinants out of this.
matrix {
    {p111, p112, p113, p121, p122, p123, p131, p132, p133},
    {p211, p212, p213, p221, p222, p223, p231, p232, p233},
    {p311, p312, p313, p321, p322, p323, p331, p332, p333}}
theSubs=apply(flatten entries M0,flatten entries bigM,(i,j)->i=>j)
det sub(matrix {
    {p111, p121, p131},
    {p211, p221, p231},
    {p311, p321, p331}},theSubs)

--Our determinants
sm1="matrix {
    {p11y, p12y, p13y},
    {p21y, p22y, p23y},
    {p31z, p32z, p33z}}"
sm2="matrix {
    {p11y, p12y, p13y},
    {p21z, p22z, p23z},
    {p31y, p32y, p33y}}"
sm3="matrix {
    {p11z, p12z, p13z},
    {p21y, p22y, p23y},
    {p31y, p32y, p33y}}"

theS= apply({sm1,sm2,sm3},sm->apply({{1, 2}, {1, 3}, {2, 3},{2, 1},{3, 1}, {3, 2}},i->value replace("z",toString last i,replace("y",toString first i,sm))))
 theS//flatten/(i->det sub(i,theSubs))




theS_1_0
netList oo
elinasM=(matrix{
    {p111,p121,p131,p112,p122,p132,p113,p123,p133},
    {p211,p221,p231,p212,p222,p232,p213,p223,p233},
    {p311,p321,p331,p312,p322,p332,p313,p323,p333}})||matrix{{p112,p122,p132},
    {p212,p222,p232},
    {p312,p322,p332},
    {p112,p123,p133},
    {p213,p223,p233},
    {p313,p323,p333}
    }|diagonalMatrix{1,1,1,1,1,1}


replace("1","2","111")







matrix {
    {p111, p112, p113},
    {p211, p212, p213},
    {p311, p312, p313}}
matrix {
    {p111, p112, p113},
    {p211, p212, p213},
    {p311, p312, p313}}



M0

allVars=append(flatten flatten eVars,w)

--E=eliminate(I,drop(flatten flatten flatten eVars,20));
--E=eliminate(I,drop(flatten flatten flatten eVars,0));
{*
needsPackage"Bertini"
degenSlice=2
slice1=apply(#flatten flatten flatten pVars-1-degenSlice,i->makeB'Section({1}|flatten entries bigM))
slice2=apply(degenSlice,i->makeB'Section({1}|flatten allVars))
--slice2={}
theSlice=slice2|slice1
#slice1
#flatten allVars
makeB'InputFile(storeBM2Files,
    AffVariableGroup=>flatten allVars,
    B'Configs=>{MPType=>2,UseRegeneration=>1},
    B'Polynomials=>theSlice
    )
runBertini(storeBM2Files)
*}

S=QQ[pVars]
gens S
setDegree=3

pVals=()->apply(flatten entries M0,flatten entries sub(bigM,apply(flatten allVars,i->i=>first random({1,1,-1,1,-1,2,-2}))),(p,v)->sub(p,R)=>v)


npWin=matrix{delete(null,apply(flatten entries basis(setDegree,S),i->if (max first exponents i)>1 then null else i))};
theParameterization
veroneseP=()->    sub(sub(basis(setDegree,S),R),pVals())
veroneseP=()->    sub( sub(npWin,R),pVals())
integerMatrix=veroneseP();
--for i to numcols veroneseP()-2 do integerMatrix=integerMatrix||veroneseP();
integerMatrix=matrix for i to numcols veroneseP()-1 list flatten entries veroneseP();
--win=kernel sub(integerMatrix,ZZ);
-- (S,U,V)=SVD sub(integerMatrix,RR);

T=CC[pVars]
win=eigenvectors sub(integerMatrix,RR);
first win/abs//min

numEV=1
F=submatrix(win_1,,reverse for i to numEV-1 list (numrows win)-i-1);
F=clean(1e-6,F);
--F*inverse diagonalMatrix{.143747,   .00282934,  -.187009,            -.187009     }
F
win=ideal(sub(npWin,T)*F);
npWin=first for i in win_* list monomials i

--npWin=first coefficients ((basis(setDegree,T)*F)_(0,0))
--npWin=matrix {{p131*p221*p311, p132*p221*p311, p131*p222*p311, p132*p222*p311, p121*p231*p311, p122*p231*p311, p121*p232*p311, p122*p232*p311, p131*p221*p312, p132*p221*p312, p131*p222*p312, p132*p222*p312, p121*p231*p312, p122*p231*p312, p121*p232*p312, p122*p232*p312, p131*p211*p321, p132*p211*p321, p131*p212*p321, p132*p212*p321, p111*p231*p321, p112*p231*p321, p111*p232*p321, p112*p232*p321, p131*p211*p322, p132*p211*p322, p131*p212*p322, p132*p212*p322, p111*p231*p322, p112*p231*p322, p111*p232*p322, p112*p232*p322, p121*p211*p331, p122*p211*p331, p121*p212*p331, p122*p212*p331, p111*p221*p331, p112*p221*p331, p111*p222*p331, p112*p222*p331, p121*p211*p332, p122*p211*p332, p121*p212*p332, p122*p212*p332, p111*p221*p332, p112*p221*p332, p111*p222*p332, p112*p222*p332}}
use R
npWin=value toString npWin;
pVals=()->apply(flatten entries M0,flatten entries sub(bigM,apply(flatten allVars,i->i=>first random({1,1,-1,1,-1,2,-2,3,-3}))),(p,v)->sub(p,R)=>v)
sparseVeroneseP=()->    sub( npWin,pVals())
sparseVeroneseP()
smallIntegerMatrix=matrix for i to numcols sparseVeroneseP()-1 list flatten entries sparseVeroneseP();
theGens=  ideal((npWin)*generators kernel smallIntegerMatrix)
printGens theGens
codim theGens


   support( + p131*(p211*p321- p221*p311) +p121*(p231*p311- p211*p331) + p111*(p221*p331- *p231*p321 ))


g1=det   matrix{
       {p111,p121,p131},
       {p211,p221,p231},
       {p311,p321,p331}}

g2=   det   matrix{
       {p112,p122,p132},
       {p212,p222,p232},
       {p312,p322,p332}}
---(3,3,3) (1,1,0)
win={
(p131*p221*p311-p121*p231*p311-p131*p211*p321+p111*p231*p321+p121*p211*p331-p111*p221*p331)*(-1),
(p132*p221*p311+p131*p222*p311-p122*p231*p311-p121*p232*p311+p131*p221*p312-p121*p231*p312-p132*p211*p321-p131*p212*p321+p112*p231*p321+p111*p232*p321-p131*p211*p322+p111*p231*p322+p122*p211*p331+p121*p212*p331-p112*p221*p331-p111*p222*p331+p121*p211*p332-p111*p221*p332)*(-1),
(p132*p222*p311-p122*p232*p311+p132*p221*p312+p131*p222*p312-p122*p231*p312-p121*p232*p312-p132*p212*p321+p112*p232*p321-p132*p211*p322-p131*p212*p322+p112*p231*p322+p111*p232*p322+p122*p212*p331-p112*p222*p331+p122*p211*p332+p121*p212*p332-p112*p221*p332-p111*p222*p332)*(-1),
(p132*p222*p312-p122*p232*p312-p132*p212*p322+p112*p232*p322+p122*p212*p332-p112*p222*p332)*(-1),
(p133*p221*p311+p131*p223*p311-p123*p231*p311-p121*p233*p311+p131*p221*p313-p121*p231*p313-p133*p211*p321-p131*p213*p321+p113*p231*p321+p111*p233*p321-p131*p211*p323+p111*p231*p323+p123*p211*p331+p121*p213*p331-p113*p221*p331-p111*p223*p331+p121*p211*p333-p111*p221*p333)*(-1),
(p133*p222*p311+p132*p223*p311-p123*p232*p311-p122*p233*p311+p133*p221*p312+p131*p223*p312-p123*p231*p312-p121*p233*p312+p132*p221*p313+p131*p222*p313-p122*p231*p313-p121*p232*p313-p133*p212*p321-p132*p213*p321+p113*p232*p321+p112*p233*p321-p133*p211*p322-p131*p213*p322+p113*p231*p322+p111*p233*p322-p132*p211*p323-p131*p212*p323+p112*p231*p323+p111*p232*p323+p123*p212*p331+p122*p213*p331-p113*p222*p331-p112*p223*p331+p123*p211*p332+p121*p213*p332-p113*p221*p332-p111*p223*p332+p122*p211*p333+p121*p212*p333-p112*p221*p333-p111*p222*p333)*(-1),
(p133*p222*p312+p132*p223*p312-p123*p232*p312-p122*p233*p312+p132*p222*p313-p122*p232*p313-p133*p212*p322-p132*p213*p322+p113*p232*p322+p112*p233*p322-p132*p212*p323+p112*p232*p323+p123*p212*p332+p122*p213*p332-p113*p222*p332-p112*p223*p332+p122*p212*p333-p112*p222*p333)*(-1),
(p133*p223*p311-p123*p233*p311+p133*p221*p313+p131*p223*p313-p123*p231*p313-p121*p233*p313-p133*p213*p321+p113*p233*p321-p133*p211*p323-p131*p213*p323+p113*p231*p323+p111*p233*p323+p123*p213*p331-p113*p223*p331+p123*p211*p333+p121*p213*p333-p113*p221*p333-p111*p223*p333)*(-1),
(p133*p223*p312-p123*p233*p312+p133*p222*p313+p132*p223*p313-p123*p232*p313-p122*p233*p313-p133*p213*p322+p113*p233*p322-p133*p212*p323-p132*p213*p323+p113*p232*p323+p112*p233*p323+p123*p213*p332-p113*p223*p332+p123*p212*p333+p122*p213*p333-p113*p222*p333-p112*p223*p333)*(-1),
(p133*p223*p313-p123*p233*p313-p133*p213*p323+p113*p233*p323+p123*p213*p333-p113*p223*p333)*(-1)}
