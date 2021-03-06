restart
dir="/Users/jo/Documents/GoodGit/multiregeneration/bertini-version/unsolved"
--This M2 code produces a system of likelihood equations
--This formulation is the homogeneous local kernel formulation

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
homogeneousSymLocalKernelFormulation=(n,r)->(
    fn := openOut(dir|"/bertiniInput_variablesAndConstants");
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
        colsumM = (uplus*bigP-hadamard(U,scale(U)))*transpose matrix {for i to numRows M-1 list 1_R};
--        uSub = flatten for i to numRows U-1 list for j from i to numRows U-1 list U_(i,j)=>random(1,100);
--        uAll = sum flatten for i to numRows U-1 list for j to numRows U-1 list U_(i,j);
--        M = sub(sub(M,{uplus=>uAll}),uSub);
        F = flatten for i to numRows M-1 list for j from i+1 to numRows M-1 list homog({1,ps,a,Lz},M_(i,j));
        DF = flatten for i to numRows M-1 list homog({1,ps,a,Lz},M_(i,i));
        CF = flatten for i to numRows M-1 list homog({1,ps,a,Lz},colsumM_(i,0));
        G = apply(subsets(1+numRows M,2),i->(
            if i_1==numRows M
            then homog({1,ps,a,Lz},colsumM_(i_0,0))
            else homog({1,ps,a,Lz},M_(i_0,-1+i_1))));
        G = flatten apply(subsets(1+numRows M,2),i->(
            if i_0==-1+i_1
            then {}
            else homog({1,ps,a,Lz},M_(i_0,-1+i_1))));
--        F=DF|F;
--        F = G ;
--        F=F|CF;
        F=CF|F;
        u := support (product flatten entries U);
        p1 := "constant ii, ";
        p1 = p1|demark(",",u/toString)|" ; ";
        scan( {P,Lam,L},{ps,a,Lz},(i,j)->(
            fn<<("hom_variable_group "|demark(",",toString\((support product flatten entries i)|{j}))|" ;") ;
            fn <<endl;
            ));
        fn<<close;
        fn=openOut(dir|"/bertiniInput_equations");
        print("");
        fn<< p1;
        fn<<endl;
        fn<<("ii = I ;");
        fn<<endl;
        scan(u,i->(fn<<(toString(i)|" = "|toString(2*random CC-random CC)|" ; ");fn<<endl));
        fn<<endl;
        fn<<(toString(uplus)|" = "|demark("+",u/toString)|" ; ");
        fn<<endl;
        p1 := "function ";
        sf="f";
        p1 = p1|demark(",",apply(#F,i->sf|i))|" ; ";
        print(p1);
        fn<<p1;
        fn<<endl;
        scan(#F,i->print(sf|i|" = "|toString(F_i)|" ; ")   );
        scan(#F,i->(fn<<(sf|i|" = "|toString(F_i)|" ; "); fn<<endl; fn<<endl)   );
        fn <<close;
        return F
        ))

(n,r)=(6,3)
F = homogeneousSymLocalKernelFormulation(n,r)
printDegrees(F)

S=QQ[p,a,LZ]
irr=ideal(p^7,a^7,LZ^10)
degX=degX//toList/toList
degY = apply(degX,i->p*(i_0)+a*(i_1)+LZ*(i_2))
B=1;scan(#degY,d->(B=(B*degY_d) %irr;print(d=>sub(B,{p=>1,LZ=>1,a=>1}));print B));



1 2544	.
3 depth_0
5 depth_1
5 depth_2
4 depth_3
13 depth_4
35 depth_5
60 depth_6
87 depth_7
78 depth_8
38 depth_9
