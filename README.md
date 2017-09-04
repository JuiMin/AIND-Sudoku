# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: In regular sudoku solving, we used constraint propagation to converge each box
on a distinct value by following the rule that no unit (specific collection of boxes) can have boxes with
the same value. As boxes are filled in, the other boxes' potential values are decreased
until one or no solution is found for each box.

In the naked twins problem, we used the same methodology but we added a further constraint.
If a unit U has a subset of boxes B that share an identical set of solutions S, and sets
B and S have the same size then we can reason boxes in U that are not in B will not contain
values in S. Using this reasoning, we can eliminate the values in S from the possible solution
sets of boxes in U that are not in B.

Our use of constraint propagation allows use to add this characteristic as a constraint
when eliminating values from a box's potential solutions. When examining the state of
the board, we can check if a unit has boxes where the naked twins method can apply
and reduce the number of potential solutions further than just using the rule of
requiring values in each unit to be unique. This additional constraint reduces the
number of boards we need to look at by providing an extra method of reducing
potential values. The final result doesn't change but we can get there faster.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: As discussed in question 1, we can use constraint propagation to work towards sudoku
solutions by acknowledging each box as having a set of potential values and using the
constraint that each unit must be a set of boxes with non-repeating values. Using this
non-repeating criteria as our constraint, we can progressively fill in values for
boxes until we converge on one or no solutions.

In the diagonal sudoku problem, we introduced the idea that the board had an extra set of rules
to follow; where the left and right diagonals of the board must also follow the same non-repeating
pattern as the units. This effectively makes them units as well, and we utilized this acknowledgement
in writing the program.

The operation of our constraint propagation relied on the fact that boxes have certain relationships
to other boxes and we must satisfy a specific condition for related boxes in pursuit of
singular solutions for each box. In the diagonal sudoku, some boxes were given
a new relationships for the constraint to work over, reducing the number of potential solutions.

As opposed to the naked twins problem, diagonal sudoku can change the eventual solution.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project.
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.
