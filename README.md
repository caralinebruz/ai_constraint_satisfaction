# AI Constraint Satisfaction

Artificial Intelligence class lab 2

Coloring of an input graph using a (given) minimum number of colors [1-4]

## ABOUT

This code determines color assignment of nodes in a graph based on the rule that no two adjacent edges should share a color.

This code works as a single step to convert the input graph into CNF clauses and then performs DPLL resolution on the constraints. Only a single command performs all steps.

This code does not include the algorithm for computing the minimum number of colors required for the given graph input. It only colors the graph based on adjacent bordering rules.

## EXECUTION

Executed using the following optional verbose flag, the desired number of colors to be used, and the input graph file:

`./colormap.py 3 [-v] data/input/oz.txt`


## OUTPUT

The solution's final graph output coloring goes to STDOUT:


```
NSW = BLUE
NT = BLUE
Q = GREEN
SA = RED
T = RED
V = GREEN
WA = GREEN
```

Corresponding CNF clauses generated from the input graph are persisted to a file in the `output` directory by default in the following format:

EG. if the inputfile is `tiny.txt`, then all CNF output goes to `data/out/cnf_tiny.txt_out`

all outputs will go to the directory `data/out` regardless of inputfilepath (relative as well as absolute input file paths will write to data/out).


## CIMS
This code has been tested on `access.cims.nyu.edu`

## REFERENCES
I have written all of my code. References, when used, are denoted inline with the code in the method I have used them in.
