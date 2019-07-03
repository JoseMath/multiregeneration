restart
--This M2 code produces a system of likelihood equations
--This formulation is the homogeneous local kernel formulation

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


getOrtho = n ->(
    (S1,U1,V1) := SVD(matrix for i to n-1 list for j to n-1 list random RR);
    return V1)

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
homogeneousSymLocalKernelFormulation=(n,r,s)->(
    hadamard=(A,B)->matrix for i to numRows A-1 list for j to numColumns A-1 list A_(i,j)*B_(i,j);
    if n>9 then print("error n is too large") else(
        P =for i to r-1 list for j to r-1 list if i<j then "p"|i|j else "p"|j|i;
        U =for i to n-1 list for j to n-1 list if i<j then "u"|i|j else "u"|j|i;
        Lam = for i to n-r-1 list for j to n-r-1 list if i<j then "lam"|i|j else "lam"|j|i;
        L = for i to n-r-1 list for j to r-1 list "L"|i|j;
        kk = CC ;
        R = kk[ {uplus}|flatten flatten U]**kk[ (flatten flatten P)|{ps}]**kk[ (flatten flatten Lam)|{a}]**kk[ (flatten flatten L)|{Lz}];
--        O1 = O2 = sub(getOrtho(r),R) ;
--        O3 = O4 = sub(getOrtho(n),R) ;
        O1 = O2 = diagonalMatrix for i to r-1 list 1_R ;
        O3 = O4 = diagonalMatrix for i to n-1 list 1_R ;
        scale=(A)->matrix for i to numRows A-1 list for j to numRows A list if i==j then 2_R else 1_R;
        (P,Lam,L,U) = toSequence apply({P,Lam,L,U},i->matrix value toString i);
        P = hadamard(P,scale(P));
        print(P,Lam,L,U);
        J = L;
        bigP = O3*(matrix{
            {P,  P*transpose J},
            {L*P,L*P*transpose J}})*transpose O4;
        bigL = (matrix{{L,diagonalMatrix for i to n-r-1 list -1_R}});
        bigJ = bigL;
        print(bigL,bigP);
        M = hadamard(bigP,(transpose bigL)*Lam*bigJ)+uplus*bigP-hadamard(U,scale(U));
--        uSub = flatten for i to numRows U-1 list for j from i to numRows U-1 list U_(i,j)=>random(1,100);
--        uAll = sum flatten for i to numRows U-1 list for j to numRows U-1 list U_(i,j);
--        M = sub(sub(M,{uplus=>uAll}),uSub);
        F = flatten for i to numRows M-1 list for j from i+1 to numRows M-1 list homog({1,ps,a,Lz},M_(i,j));
        DF = for i to numRows M-1 list if member(i,s) then homog({1,ps,a,Lz}, bigP_(i,i)) else homog({1,ps,a,Lz},((transpose bigL)*Lam*bigJ)_(i,i) + uplus);
        F =DF|F;
        printU=()->(
            print("");
            u := support (product flatten entries U);
            p1 := "constant ii, ";
            p1 = p1|demark(",",u/toString)|" ; ";
            print("ii = I ;");
            print(p1);
            scan(u,i->if not member(i,{u00,u11,u22,u33}) then print(toString(i)|" = "|toString(2*random CC-random CC)|" ; ")  else print(toString(i)|" = "|toString(0)|" ; ")   );
            print(toString(uplus)|" = "|demark("+",u/toString)|" ; ")
            );
        printVarGroups=()->(print("");scan( {P,Lam,L},{ps,a,Lz},(i,j)->print("hom_variable_group "|demark(",",toString\((support product flatten entries i)|{j}))|" ;")));
        return F
        ))


(n,r,s)=(5,2,{1,2,3,4})
F = homogeneousSymLocalKernelFormulation(n,r,s)

printVarGroups()
printU()
printBertiniFunction("f",F)
printDegrees(F)
