restart
--This M2 code produces a system of likelihood equations
--This formulation is the homogeneous--multilinear local kernel formulation

printBertiniFunction = (sf,F) ->(
    print("");
    p1 := "function ";
    p1 = p1|demark(",",apply(#F,i->sf|i))|" ; ";
    print(p1);
    scan(#F,i->print(sf|i|" = "|toString(F_i)|" ; ")   )
    )
printDegrees = F ->(
    D := F/degree/(i->new Array from drop(i,1));
    print("degrees = "|toString (new Array from D))
    )


homog = (H,p) -> ( --H= {x0,y0,z0} homogenizing variables, p=polynomial
    T = terms p;
    D =  apply( T,i->degree i);
    m = max\transpose D;
    print m;
    q = 0;
    scan(D,T,(d,t)->(
        q=q+t*product apply(#m,a->(H_a)^((m-d)_a));
        ));
    return q
    )

--Four variable groups.
homogeneousMultilinearLocalKernelFormulation=(n,r)->(
    hadamard=(A,B)->matrix for i to numRows A-1 list for j to numColumns A-1 list A_(i,j)*B_(i,j);
    if n>9 then print("error n is too large") else(
        P =for i to r-1 list for j to r-1 list if i<j then "p"|i|j else "p"|j|i;
        U =for i to n-1 list for j to n-1 list if i<j then "u"|i|j else "u"|j|i;
        Lam = for i to n-r-1 list for j to n-r-1 list if i<j then "lam"|i|j else "lam"|j|i;
        L = for i to n-r-1 list for j to r-1 list "L"|i|j;
        J = for i to n-r-1 list for j to r-1 list "J"|i|j;
        R = QQ[ {uplus}|flatten flatten U]**QQ[ (flatten flatten P)|{ps}]**QQ[ (flatten flatten Lam)|{a}]**QQ[ (flatten flatten L)|{Lz}]**QQ[ (flatten flatten J)|{Jz}];
        scale=(A)->matrix for i to numRows A-1 list for j to numRows A list if i==j then 2_R else 1_R;
        (P,Lam,L,U,J) = toSequence apply({P,Lam,L,U,J},i->matrix value toString i);
        P=hadamard(P,scale(P));
        print(P,Lam,L,U);
        bigP = matrix{
            {P,  P*transpose J},
            {L*P,L*P*transpose J}};
        bigL = matrix{{L,diagonalMatrix for i to n-r-1 list 1_R}};
        bigJ = matrix{{J,diagonalMatrix for i to n-r-1 list 1_R}};
        M = hadamard(bigP,(transpose bigL)*Lam*bigJ)+uplus*bigP-hadamard(U,scale(U));
--        uSub = flatten for i to numRows U-1 list for j from i to numRows U-1 list U_(i,j)=>random(1,100);
--        uAll = sum flatten for i to numRows U-1 list for j to numRows U-1 list U_(i,j);
--        M = sub(sub(M,{uplus=>uAll}),uSub);
        F = flatten for i to numRows M-1 list for j from i to numRows M-1 list homog({1,ps,a,Lz,Jz},M_(i,j));
        printU=()->(
            print("");
            u := support (product flatten entries U);
            p1 := "constant ";
            p1 = p1|demark(",",u/toString)|" ; ";
            print(p1);
            scan(u,i->print(toString(i)|" = "|toString(2*random CC-random CC)|" ; ")   );
            print(toString(uplus)|" = "|demark("+",u/toString)|" ; ")
            );
        printVarGroups=()->(print("");scan( {P,Lam,L,J},{ps,a,Lz,Jz},(i,j)->print("hom_variable_group "|demark(",",toString\((support product flatten entries i)|{j}))|" ;")));
        return F
        ))


(n,r)=(4,2)
F = homogeneousMultilinearLocalKernelFormulation(n,r)
G=flatten entries gens minors(2,matrix{support( Lz*product flatten entries L),support (Jz*product flatten entries J)})
printBertiniFunction("f",G|F)
printDegrees(G|F)
printVarGroups()
printU()
