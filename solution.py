assignments = []

# Import the math library
import math

# These are the potential rows and columns for the sudoku board where rows are
# identified by letter and columns are identified by single digits
rows = 'ABCDEFGHI'
cols = '123456789'

# This gives the length/width of each square unit. Since the board is divided
# into sections based on how many digits are in each row, we can assume that this is the
# square root of the number of digits in each row.
squareSize = int(math.sqrt(len(rows)))

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

'''
Returns the cross product of the input lists A and B
'''
def cross(A, B):
    return [s+t for s in A for t in B]

# List of all boxes on the board
boxes = cross(rows,cols)

# Cross the rows and columns so that we have a container for checking the units
# in each grouping
row_units = [cross(r, cols) for r in rows]
col_units = [cross(rows, c) for c in cols]

# Generate a container for each square of the board
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

# Diagonal Units for the left and right diagonal
left_diag_units = [rows[index] + cols[index] for index in range(9)]
right_diag_units = [rows[index] + cols[::-1][index] for index in range(9)]

# The list of both diagonals to be added to the unit list
diag_units = [left_diag_units, right_diag_units]

# Get the peers for each unit
# First get all the units in a big list
unitlist = row_units + col_units + square_units + diag_units
# create a dictionary of each box where the values are the units in the units related to it
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
# Narrow down the peers by removing duplicates and the box itself
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

'''
In the naked twins problem, we used the same methodology but we added a further constraint.
If a unit U has a subset of boxes B that share an identical set of solutions S, and sets
B and S have the same size then we can reason boxes in U that are not in B will not contain
values in S. Using this reasoning, we can eliminate the values in S from the possible solution
sets of boxes in U that are not in B.

This method takes in the dictionary form of a sudoku board and
uses the naked twins method to eliminate potential values from each box's
solution set.

The resulting board is returned in dictionary form
'''
def naked_twins(values):
    # For each unit, check to see if there are multiple boxes with the same value
    for unit in unitlist:
        naked = {}
        # Check each box in the unit and form lists of boxes for each value
        for box in unit:
            if values[box] in naked.keys():
                naked[values[box]].append(box)
            else:
                naked[values[box]] = [box]
        # Check for any value that has the the same number of boxes as it has values
        for value in naked.keys():
            if len(value) == len(naked[value]) and len(value) > 1:
                # Eliminate the options in the value from the other items in the unit
                for box in [box for box in unit if box not in naked[value]]:
                    for digit in value:
                        values = assign_value(values, box, values[box].replace(digit, ''))

    return values

'''
Takes an input string representing a sudoku board and returns a dictionary representation
'''
def grid_values(grid):
    # Check the grid size so that we are dealing with a certain sized sudoku
    assert len(grid) == len(rows) * len(cols)
    # Initialize the output dictionary with default all 1-9 digits as possible
    output = dict((box, '123456789') for box in boxes)
    # Theoretically the sudoku could be bigger so we can account for this grid
    # size change using these length finders
    for index in range(len(rows) * len(cols)):
        # If the value is already determined in the string, insert the number into the dictionary
        if (grid[index] is not '.'):
            output = assign_value(output, boxes[index], grid[index])
    return output

'''
Provides a display method for outputting a board to the console.
The board is formatted for valid solutions only. An in progress board will
not be properly spaced.

The resulting board is returned in dictionary form
'''
def display(values):
    # Generate the spacer for horizontal use between squares
    spacer = ''
    for r in range(squareSize):
        spacer += '-' * (2 * squareSize)
        if r < squareSize - 1:
            spacer += '+'

    # For each box in a row, find the value in the dictionary and output the grid
    for rowIndex in range(len(row_units)):
        rowOutput = ''
        for colIndex in range(len(col_units)):
            rowOutput += values[row_units[rowIndex][colIndex]] + ' '
            if (colIndex % squareSize) == (squareSize - 1):
                rowOutput += '|'
        if (rowIndex > 0 and rowIndex < len(row_units)):
            if rowIndex % squareSize == 0:
                print(spacer)
        print(rowOutput)
'''
This function takes in the dictionary representation of the board and
checks if the box has one possible value.
If there is a box with only one number in it, eliminate that number from all peers.

The resulting board is returned in dictionary form
'''
def eliminate(values):
    # Get all the boxes that have only one value
    for box in [box for box in values.keys() if len(values[box]) == 1]:
        for peer in peers[box]:
            if (values[box] in values[peer] and peer is not box):
                values = assign_value(values, peer, values[peer].replace(values[box], ''))
    return values

'''
This function takes in the dictionary representation of the sudoku board and
checkes every unit to see if there are boxes that are the only choice for a
value that is not yet taken. If there is, the box is assigned the value.

The resulting board is returned in dictionary form
'''
def only_choice(values):
    # Try every unit
    for unit in unitlist:
        digits = dict.fromkeys(cols)
        # Checking each box in the unit, see which potential values can be claimed
        # by one or more boxes
        for box in unit:
            for val in values[box]:
                if digits[val] is None:
                    digits[val] = [box]
                else:
                    digits[val].append(box)
        # Check each potential value and see if there is only one box associated
        for key in [key for key in digits.keys() if digits[key] is not None and len(digits[key]) == 1]:
            values = assign_value(values, digits[key][0], key)
    return values

'''
This function takes in the dictionary representation of a sudoku board and reduces the puzzle
through repeated elimination of potential values.

If no eliminations can be made, the resulting board is returned.
'''
def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

'''
This function takes in the dictionary representation of the sudoku board and
looks for a solution.

If the solution is found, the dictionary form of the solution board is returned.
If the solution is determined to be un-findable then False is returned
'''
def search(values):
    # "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # This should either find an answer or get us to a stage where we can start searching
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)

    # Check if values is False, which would indicate the solution cannot be found.
    # Return False if this is the case.
    if values is False:
        return False

    # Check if the sudoku board is solved.
    # Return the board if this is the case
    if all(len(values[s]) == 1 for s in boxes):
        return values

    # Choose one of the unfilled squares with the fewest possibilities
    # Get the boxes that are stil not solved to limit search area
    potentialBoxes = [key for key in values.keys() if len(values[key]) > 1]
    # Gets the boxes with lowest number of potential values
    bestBoxes = [box for box in potentialBoxes if len(values[box]) == min([len(values[box]) for box in potentialBoxes])]
    # Pick the first one because it doesn't really matter which one we use
    bestBox = bestBoxes[0]
    # Try each of the digits that are currently options for this key
    # and run the search again to see if an answer appears
    for digit in values[bestBox]:
        attempt = values.copy()
        attempt = assign_value(attempt, bestBox, digit)
        result = search(attempt)
        if result:
            return result
    # Reset the digits so that the next pass will use the correct values

'''
This function takes in the string representation of a sudoku board and
runs the board through the game playing agent.

The resultant board is returned in dictionary form or if no solution can be found,
False will be returned (Carry over from the search function)
'''
def solve(grid):
    return search(grid_values(grid))

if __name__ == '__main__':
    diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
