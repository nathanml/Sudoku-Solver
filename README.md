# Sudoku Solver
## Instructions to run and test
From the root directory, run the following command in the 
command line:

```
python sudoku_solver.py
```
The user can then choose to solve either the easy puzzle (1), the
hard puzzle (2), or a custom puzzle (3). If the user chooses the
custom puzzle, they must build the initial state.

```
1. Easy Board
2. Hard Board
3. Custom Board
Enter the number of the board you would like to complete:3
What value would you like for position {0,0}. Please enter 0 if you would like to leave that position blank:
```

## Constraint Problem Definitions
### States
States will hold the board with a current set of assignments.
Board is represented by a 2D array of elements that are set 
to 0 if the unassigned, and 1-9 otherwise.

### Initial State
The initial state is a sudoku board at the start of execution. The
user can select either the easy board or hard board provided, or they
can opt to build a custom board themselves.

### Possible Actions
At any given state, the algorithm can select any unassigned cell (x,y)
and assign it to a variable within the domain. With no constraints, the 
domain is [1-9]; however, there are enhancements to this algorithm to
prune the domain as it becomes more constrained.

### Successor Function
select_unassigned_variable(board, domains): This function selects the next 
cell to assign. It takes as input the current board and domains available 
for each cell and returns the selected cell.

### Goal Test
check_completion_status(board): This function iterates through the board and returns
true if there are no more unassigned cells (goal state is reached).

## Design
This program uses a chronological backtracking search with several enhancements
to solve sudoku boards. This search iterates through the board, selecting an
assignment from the domain of each unassigned cell, then recursively selecting
subsequent values for the board, returning failure if there are no available values,
such that the algorithm can go back and change a previous selection.

### Improvement 1: Forward Checking
prune_domain(board, domain, x, y): This prunes the domains of the assignments
for cell (x, y) that are no longer valid so that the algorithm can
pre-emptively backtrack (as opposed to waiting for that value to be selected).

### Improvement 2: Smart selection with Minimum Remaining Value
The cell with the fewest legal values in its domain is always selected first, reducing
the overall search space.

### Improvement 3: Value Ordering with Least Constraining Value
When a cell is being assigned to a value, the domain is ordered 
by least constraining value, such that the value that rules out the fewest
number of other values is always selected, reducing the search space.

### External Libraries
heapq for ordering the domain values based on least constraining value.

### Citations
print_board function: This function beautifies the 3x3 sudoku board that
is printed for the user. I found this function at
https://stackoverflow.com/questions/61433589/variable-scope-is-incorrectly-global


