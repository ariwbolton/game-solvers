## Sudoku

This solver uses the following algorithm. First, initialize the board to have each empty square be considered to possibly contain every single number. Such "possibilities" are called "options" from here on out.


1. For each cell that's filled in 
    1. Apply the "row", "column", and "subsquare" rules, to eliminate options in other cells.
1. For each incomplete row, column, and subsquare
    1. If this group is 
1. Further refine options

If at any point, a cell has only one option, fill that cell in with that option, and apply the "row", "column", and "subsquare'

### Notes

1. Call "rows", "columns" and "regions"
1. Each cell has a list of numbers that "can" be in that square, and a list of numbers that "can't"

1. Every "deduction" results from one of the following rules:
    1. A number **can** be in region A, so that number **can't** be in region ~A
    1. A number **can't** be in region A, so that number **can** be in region ~A
    
1. "Must" preconditions
    1. A number is already filled in, in a square
    1. A number
    
1. The puzzle is done when every cell has only one number that "can" be in it

### More notes

1. Row, Column, Region "already exists" rules
1. Row, Column, Region "must exist" rules

### Another

1. Maintain a bipartite (directed?) graph of "numbers" and "cells", for the entire board
    1. A "number" has an edge to a "cell" if that number "can be in that cell"
    1. A "cell" has an edge to a "number" if that cell "can contain that number"
1. For each "constraint" (row, column, region), do the following:
    1. For each "number", maintain the list of cells that it can be in, under that constraint
    1. For each "cell" in that constraint, maintain the list of "numbers" that can be in it
    1. Define "rules" for that constraint as follows:
        1. If N cells can each only contain the same N numbers, then those numbers cannot be in any other cells
        1. If N numbers can each only be in the same N cells, then those cells cannot contain any other numbers
    1. So, need to maintain "inverse" mappings:
        1. From "cell groups" to a list of numbers
        1. From "number group" to a list of cells
    1. If any cell group has a number list of length equal to the number of cells in that cell group, apply rule #1
    1. If any "number group" has a cell list of length equal to the number of numbers in that number group, apply rule #2
    1. When applying rules, "notify" the constraints that "contain" any cell that is affected, to update its internal mappings for those cells and corresponding numbers
    1. First notify to update **all** internal mappings, then tell those constraints to check for new rules applications
        1. Call each unit of work a "task"
            1. "update mapping" tasks - mark a number as not an option for a cell
                1. Must **remove** cell from "number options"
                1. Must update the cell group mapping - remove number from cell group mapping list
                1. Must **remove** number from "cell options"
                1. Must update the number group mapping - remove cell from number group mapping list
            1. "apply rules" tasks
        1. All tasks are parametrized by a "cell group" or a "number group"
            1. Should check if that cell group or number group has a small enough number of corresponding values
            
            
number_map          = [number   : [cell]]
cell_map            = [cell     : [number]]
cell_group_map      = [[cell]   : [number]]     # Used by rules
number_group_map    = [[number] : [cell]]       # Used by rules
        