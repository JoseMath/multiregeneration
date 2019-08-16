restart
dirStart="/Users/jo/Documents/GoodGit/multiregeneration/bertini-version/Subsection-MLE"
--This M2 code produces a system of likelihood equations
--This formulation is the homogeneous local kernel formulation

printDegrees = F ->(
    D := F/degree/(i->new Array from drop(i,1));
    print("degrees = "|toString (new Array from delete(D,[])))
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
--Three variable groups.
homogeneousSymLocalKernelFormulation=(n,r,z)->(
    dir = dirStart|"/A_n_"|n|"_r_"|r|"_z_"|z;
    if not fileExists dir then mkdir dir;
    fn := openOut(dir|"/bertiniInput_variables");
    hadamard=(A,B)->matrix for i to numRows A-1 list for j to numColumns A-1 list A_(i,j)*B_(i,j);
    if n>9 then print("error n is too large") else(
        P =for i to r-1 list for j to r-1 list if i<j then "p"|i|j else "p"|j|i;
        U =for i to n-1 list for j to n-1 list if i<j then "u"|i|j else "u"|j|i;
        Lam = for i to n-r-1 list for j to n-r-1 list if i<j then "lam"|i|j else "lam"|j|i;
        L = for i to n-r-1 list for j to r-1 list "L"|i|j;
        kk = QQ ;
        R = kk[ {uplus}|flatten flatten U]**kk[ (flatten flatten P)|{ps}]**kk[ (flatten flatten Lam)|{a}]**kk[ (flatten flatten L)|{Lz}];
        uz ={};
        scan(gens R,i->if member(toString i,{"u00","u11","u22"}) then uz=uz|{i});
        pz ={};
        scan(gens R,i->if member(toString i,{"p00","p11","p22"}) then pz=pz|{i});
        pz =drop(pz,-3+z);
        I =ideal(uz)+ideal(pz);
        print(toString I);
        scale=(A)->matrix for i to numRows A-1 list for j to numRows A list if i==j then 2_R else 1_R;
        (P,Lam,L,U) = toSequence apply({P,Lam,L,U},i->matrix value toString i);
        P = hadamard(P,scale(P));
        print(P,Lam,L,U);
        J = L;
        bigP = matrix{
            {P,  P*transpose J},
            {L*P,L*P*transpose J}};
        bigL = matrix{{L,diagonalMatrix for i to n-r-1 list -1_R}};
        bigJ = bigL;
        print(bigL,bigP);
        M = hadamard(bigP,(transpose bigL)*Lam*bigJ)+uplus*bigP-hadamard(U,scale(U));
        colsumM = (uplus*bigP-hadamard(U,scale(U)))*transpose matrix {for i to numRows M-1 list 1_R};
--        uSub = flatten for i to numRows U-1 list for j from i to numRows U-1 list U_(i,j)=>random(1,100);
--        uAll = sum flatten for i to numRows U-1 list for j to numRows U-1 list U_(i,j);
--        M = sub(sub(M,{uplus=>uAll}),uSub);
        print 1;
        --F is off diagonal and not the last column.
        F = flatten for i to numRows M-1 list for j from i+1 to numRows M-2 list homog({1,ps,a,Lz},M_(i,j));
        --DF is diagonal equations
        DF = drop(flatten for i to numRows M-1 list homog({1,ps,a,Lz},M_(i,i)),-1);
        --CF is the column sum conditions
        CF = flatten for i to numRows M-1 list homog({1,ps,a,Lz},colsumM_(i,0));
        F=CF|DF|F;
        F=F/(i->(i%I));
        F=apply(#F,i->(
            g:=toList factor F_i;
            sg:=g/(i->size(sub(value i,R)))//maxPosition;
            (g_sg)   ));
        F=F/(i->if degree value i=!=-infinity then i else null);
        F=delete(null,F);
        u := support (product flatten entries U);
        p1 := "constant ii, ";
        p1 = p1|demark(",",u/toString)|" ; ";
        rP=toString\support product flatten entries P;
        scan(pz,i->rP=delete(toString i,rP));
        fn<<("hom_variable_group "|demark(",",append(rP,"ps"))|" ;") ;
        fn<<endl;
        scan( {Lam,L},{a,Lz},(i,j)->(
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
        print u;
        scan(u,i->(
            if not member(toString i,{"u00","u11","u22"})
            then ( fn<<(toString(i)|" = "|toString(1.2*random CC-random CC)|" ; "))
            else ( fn<<(toString(i)|" = "|toString(0.0)|" ; "));
            fn<<endl));
        fn<<endl;
        fn<<(toString(uplus)|" = "|demark("+",u/toString)|" ; ");
        fn<<endl;
        p1 := "function ";
        sf="f";
        p1 = p1|demark(",",apply(#F,i->sf|i))|" ; ";
        print(p1);
        fn<<p1;
        fn<<endl;
        scan(#F,i->(print(sf|i|" = "|toString factor value toString(F_i)|" ; ");
            print degree value (F_i))   );
        scan(#F,i->(
--            g:=toList factor F_i;
--            sg:=g/(i->size(sub(value i,R)))//maxPosition;
            fn<<(sf|i|" = "|toString (F_i)|" ; "); fn<<endl; fn<<endl)   );
        fn <<close;
        fn=openOut(dir|"/inputFile.py");
        D := F/value/degree/(i->new Array from drop(i,1));
        fn<<("degrees = "|toString (new Array from delete([],D)));
        print("#D"=>#D);
        fn<<endl;
        fn<<"logTolerance = -10
maxProcesses = 1
targetDimensions = [[0,0,0]]
algebraicTorusVariableGroups = [0,1,2]";
        close fn;
        return F
        ))

apply(4,z->(
    (n,r)=(4,3);
    F = homogeneousSymLocalKernelFormulation(n,r,z)))

--uSub = {u00 => 0, u01 => 17, u02 => 79, u03 => 5, u04 => 38, u11 => 0, u12 => 8, u13 => 70, u14 => 23, u22 => 0, u23 => 31, u24 => 88, u33 => 19, u34 => 66, u44 => 95}
--uSub = append(uSub,uplus=>uSub/first//sum)
--I=sub(sub(ideal F,uSub),uSub)
