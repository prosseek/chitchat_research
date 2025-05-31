## Overall design

* Revision 0.1: [2015/09/16]

### Process

1. The contexts are described as format in directory "DIRECTORY"
2. The contexts are read and evaluated, the results is in JSON format
    * JSON/JSON compressed
    * Labeled/Labeled compressed
    * Complete
    * FBF from width 1 to 10
    * CBF from width 1 to 10
3. The table is turned into gnuplot script
4. The gnuplot script is executed to generate PNG

### Location

* Source "DIRECTORY": `ContextSharingSimulation/experiment/jsonContextExamples/2015`
* Results in JSON: ``
* GNUSCRIPT in gnu source file: ``
* FINAL PNG file: ``