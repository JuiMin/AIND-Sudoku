assignments = []

import math

# Config Data
rows = 'ABCDEFGHI'
cols = '123456789'

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

def cross(A, B):
    return [s+t for s in A for t in B]

# List of boxes
boxes = cross(rows,cols)

# Cross the rows and columns so that we have a container for checking the units
# in each grouping
row_units = [cross(r, cols) for r in rows]
col_units = [cross(rows, c) for c in cols]

# Generate a container for each square of the board
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

# Diagonal Units
left_diag_units = [rows[index] + cols[index] for index in range(9)]
right_diag_units = [rows[index] + cols[::-1][index] for index in range(9)]

diag_units = [left_diag_units, right_diag_units]

# Get the peers for each unit
# First get all the units in a big list
unitlist = row_units + col_units + square_units + diag_units
# create a dictionary of each box where the values are the units in the units related to it
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
# Narrow down the peers by removing duplicates and the box itself
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def naked_twins(values):
    # For each unit, check to see if there are multiple boxes with the same value
    for unit in unitlist:
        naked = {}
        # Check each box and record values
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
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

# Takes an input string representing a sudoku board and returns a dictionary representation
def grid_values(grid):
    # Check the grid size so that we are dealing with a certain sized sudoku
    assert len(grid) == 81
    # Initialize the output dictionary
    output = dict((box, '123456789') for box in boxes)
    # Theoretically the sudoku could be bigger so we can account for this grid
    # size change using these length finders
    for index in range(len(rows) * len(cols)):
        if (grid[index] is not '.'):
            output = assign_value(output, boxes[index], grid[index])
    return output

def display(values):
    # Generate the Spacer between squares
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

# This function should go through all the values in the dictionary and eliminate
# values that can't be the answer
# If there is a box with only one number in it, eliminate that number from all peers
def eliminate(values):
    # Get all the boxes that have only one value
    for box in [box for box in values.keys() if len(values[box]) == 1]:
        for peer in peers[box]:
            if (values[box] in values[peer] and peer is not box):
                values = assign_value(values, peer, values[peer].replace(values[box], ''))
    return values

# If the boxes examined have have a value that is the only choice in a specific set,
# You should eliminate the other values and confirm that number
def only_choice(values):
    # Try every unit
    for unit in unitlist:
        # Check if there are any boxes in the unit that have only one possibility
        digits = dict.fromkeys(cols)
        for box in unit:
            for val in values[box]:
                if digits[val] is None:
                    digits[val] = [box]
                else:
                    digits[val].append(box)
        for key in [key for key in digits.keys() if digits[key] is not None and len(digits[key]) == 1]:
            values = assign_value(values, digits[key][0], key)
    return values

# Reduces the puzzle so that we can find a solution
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

# Search
def search(values):
    # "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # This should either find an answer or get us to a stage where we can start searching
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)

    # Check if either the values are false (error) or if the puzzle is complete
    if values is False:
        return False

    # Solved
    if all(len(values[s]) == 1 for s in boxes):
        return values

    # Choose one of the unfilled squares with the fewest possibilities
    # Get the keys that are possible
    keys = [key for key in values.keys() if len(values[key]) > 1]
    # Gets the keys with the best possible results
    bestKeys = [key for key in keys if len(values[key]) == min([len(values[key]) for key in keys])]
    if len(bestKeys) > 0:
        # Loop through the best keys to do a depth first search
        key = bestKeys[0]
        # Check each of the digits that are currently options for this key
        digitlist = values[key]
        for digit in digitlist:
            attempt = values.copy()
            attempt = assign_value(attempt, key, digit)
            result = search(attempt)
            if result:
                return result
    # Reset the digits so that the next pass will use the correct values

def solve(grid):
    return search(grid_values(grid))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
