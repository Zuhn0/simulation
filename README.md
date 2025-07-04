Input : python3 simulation.py -n 100 -L 1000 -S 200 -g G1 25 G2 25 G3 25 G4 25 -D 1000 -T 200 -o simulated_output.bed
output : //FILE GETS CREATED with NAME  "simulated_output.bed"
              simulated_output.bed: 
                chr1    0       1142    1142    G2
                chr2    2209    3197    988     G3
                chr3    4373    5303    930     G4
                chr4    6053    7176    1123    G2
                chr5    8302    9198    896     G3
                chr6    10242   11151   909     G3
                chr7    12388   13451   1063    G1
                chr8    14651   15392   741     G3
                chr9    16229   16923   694     G1
                chr10   17809   18565   756     G4
                chr11   19351   21133   1782    G4
                chr12   22071   22997   926     G4
                chr13   24301   25334   1033    G3
                chr14   26530   27741   1211    G2
                chr15   28864   29709   845     G1
                chr16   30513   31823   1310    G1
                chr17   33143   34325   1182    G4
                chr18   35177   36549   1372    G2
                chr19   37412   38311   899     G2
                chr20   39218   40213   995     G2
                chr21   41100   42043   943     G3
                chr22   43383   44274   891     G4
                chr23   45464   46487   1023    G1
                chr24   47530   48995   1465    G2
                chr25   49796   50719   923     G4
                chr26   52061   53071   1010    G2
                chr27   54244   55272   1028    G3
                chr28   56081   57314   1233    G1
                chr29   58654   59173   519     G2
                chr30   59929   60645   716     G4
                chr31   61900   63090   1190    G3
                chr32   64189   65370   1181    G4
                chr33   66358   67771   1413    G3
                chr34   68824   69765   941     G3
                chr35   70683   71678   995     G2
                chr36   72812   73980   1168    G1
                chr37   75225   76307   1082    G1
                chr38   77293   78035   742     G4
                chr39   79211   80318   1107    G1
                chr40   81350   82238   888     G1
                chr41   82939   83762   823     G1
                chr42   84404   85587   1183    G1
                chr43   86569   87569   1000    G3
                chr44   88567   89596   1029    G3
                chr45   90708   91776   1068    G1
                chr46   92771   93431   660     G2
                chr47   94584   95765   1181    G4
                chr48   96660   98070   1410    G3
                chr49   99133   99808   675     G3
                chr50   100947  102377  1430    G2
                chr51   103436  104405  969     G2
                chr52   105434  106450  1016    G2
                chr53   107475  108498  1023    G3
                chr54   109286  110448  1162    G1
                chr55   111476  112057  581     G3
                chr56   113017  114027  1010    G4
                chr57   115465  116765  1300    G3
                chr58   117784  118668  884     G4
                chr59   119759  120559  800     G1
                chr60   120940  121791  851     G4
                chr61   123164  124253  1089    G1
                chr62   125424  126419  995     G1
                chr63   126936  128043  1107    G4
                chr64   129018  130178  1160    G4
                chr65   130753  131754  1001    G3
                chr66   132698  133685  987     G3
                chr67   134174  135553  1379    G4
                chr68   136115  136853  738     G2
                chr69   138082  139084  1002    G1
                chr70   139536  140930  1394    G3
                chr71   141742  142730  988     G3
                chr72   143529  144747  1218    G2
                chr73   145673  146526  853     G2
                chr74   147538  148544  1006    G2
                chr75   149673  150763  1090    G4
                chr76   151799  152779  980     G4
                chr77   154075  154739  664     G4
                chr78   155576  156644  1068    G3
                chr79   157166  158034  868     G3
                chr80   158709  159594  885     G3
                chr81   160873  162153  1280    G1
                chr82   162962  164216  1254    G2
                chr83   165213  166315  1102    G1
                chr84   167342  168682  1340    G4
                chr85   169865  170880  1015    G4
                chr86   171972  173135  1163    G1
                chr87   174100  175532  1432    G4
                chr88   176515  177789  1274    G2
                chr89   178807  179906  1099    G2
                chr90   180765  181826  1061    G3
                chr91   182998  183987  989     G4
                chr92   184579  185567  988     G3
                chr93   186417  187237  820     G4
                chr94   188097  189275  1178    G4
                chr95   190383  191190  807     G1
                chr96   192033  192906  873     G3
                chr97   194210  194969  759     G4
                chr98   195925  197044  1119    G2
                chr99   198057  199559  1502    G3
                chr100  200787  201771  984     G3

Extracting the individual part of file using "extract_rows_from_bed.py" file using input "extract_rows_from_bed.py simulated_output.bed short.bed 20 41"  inputfile:simulated_output.bed  Outputfile:short.bed from line:20 to 41 


  short.bed:
            chr20   39218   40213   995     G2
            chr21   41100   42043   943     G3
            chr22   43383   44274   891     G4
            chr23   45464   46487   1023    G1
            chr24   47530   48995   1465    G2
            chr25   49796   50719   923     G4
            chr26   52061   53071   1010    G2
            chr27   54244   55272   1028    G3
            chr28   56081   57314   1233    G1
            chr29   58654   59173   519     G2
            chr30   59929   60645   716     G4
            chr31   61900   63090   1190    G3
            chr32   64189   65370   1181    G4
            chr33   66358   67771   1413    G3
            chr34   68824   69765   941     G3
            chr35   70683   71678   995     G2
            chr36   72812   73980   1168    G1
            chr37   75225   76307   1082    G1
            chr38   77293   78035   742     G4
            chr39   79211   80318   1107    G1
            chr40   81350   82238   888     G1
            chr41   82939   83762   823     G1

Now performing mutation on short.bed file using command :
For Deletion :   "python3 mutationsimulation.py short.bed mutated_output.bed --d G1@56081" //G1 at start of 56081 gets deleted 
For Inversion :  "python3 mutationsimulation.py short.bed mutated_output.bed --invert G1" //All  G1 genes gets inverted
For Insertion :  "python3 mutationsimulation.py short.bed mutated_output.bed --insert chr20:40214:20:G50" // chr20:Start:size:name  , rest all positions gets shifted further
For Duplication: " python3 mutationsimulation.py short.bed mutated_output.bed  --dup chr20:39218-40213@chr21:40214" // chrtoduplicate:start-end@chratwhichtocopy:start   ,rest all positions gets adjusted


We Can combine all those above commands to one ex : "python3 mutationsimulation.py short.bed mutated_output.bed --d G1@56081 --invert G1 --insert chr20:40214:20:G50 --dup chr20:39218-40213@chr21:40214"

mutated_output.bed file gets created containing the mutated file. 

HOW TO RUN AND CHECK THIS SCRIPT FURTHER : 

Lets check for inversion of genes :  "python3 mutationsimulation.py short.bed mutated_output.bed --invert G1"

  mutated_output.bed 

            chr20   39218   40213   995     G2
            chr21   41100   42043   943     G3
            chr22   43383   44274   891     G4
            chr23   46487   45464   -1023   G1
            chr24   47530   48995   1465    G2
            chr25   49796   50719   923     G4
            chr26   52061   53071   1010    G2
            chr27   54244   55272   1028    G3
            chr28   57314   56081   -1233   G1
            chr29   58654   59173   519     G2
            chr30   59929   60645   716     G4
            chr31   61900   63090   1190    G3
            chr32   64189   65370   1181    G4
            chr33   66358   67771   1413    G3
            chr34   68824   69765   941     G3
            chr35   70683   71678   995     G2
            chr36   73980   72812   -1168   G1
            chr37   76307   75225   -1082   G1
            chr38   77293   78035   742     G4
            chr39   80318   79211   -1107   G1
            chr40   82238   81350   -888    G1
            chr41   83762   82939   -823    G1
   

     
  
                
           
                

