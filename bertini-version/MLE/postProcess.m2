scanLines(ell->value last separate("e",first separate(" ",ell) ),
"/Users/jo/Documents/GoodGit/multiregeneration/bertini-version/Subsection-MLE/fileDirectoryList")

dld = "/Users/jo/Documents/GoodGit/multiregeneration/bertini-version/Subsection-MLE/fileDirectoryList"
sd="/Users/jo/Documents/GoodGit/multiregeneration/bertini-version/Subsection-MLE/n_4_r_3/run/_completed_smooth_solutions/depth_9"
count= 0 ;
Z={0,2,5}
Y={}

  scanLines(fn->(
    countPoint=true;
    print fn;
    P :=  drop(lines get (sd|"/"|fn),1);
    --print P;
    zeroP = apply(Z,i->P_i);
    print zeroP;
    oneP = apply(Y,i->P_i);
    --print oneP;
    scan(zeroP, ell->(
      expo =value last separate("e",first separate(" ",ell));
      print expo;
      if -10<expo
      then countPoint=false
      ));
    print 1;
    print countPoint;
    scan(oneP, ell->
      if -10>value last separate("e",first separate(" ",ell) )
      then countPoint=false
      );
    print countPoint;
    if countPoint then count=count+1),
    dld)
count
