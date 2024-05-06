"""
Author: Mihkel Uutar
Last updated: 06.05.2024

University of Tartu
Beyond Worst Case Complexity of the Simplex Algorithm

This file has the Python implementation of a basic Simplex Method.
"""

from Utilities.format_utils import *     # Formatting values for prettier printing
from IGNORED.visualization_utils import *

# ---
# Implementation of the Simplex Algorithm
# ---

# Solves a linear problem by finding the maximum value within the constraints using the Simplex Method developed by George B. Dantzig
# Input is taken as three lists of integer values:
#  A - objective function given as a lsit of coeffiecients
#  b - inequality constraints, given as a matrix with a row for each inequality constraint. Each row has n variables.
#      When a constraint has less than n variables, the value for that variable should be set as 0
#  c - inequality constraint values (right side of the equation)
# The function has additional parameter for printing out values of the table between steps. If print_steps is set to True each step
# of the algorithm (after each pivoting) is printed out to console. If it's False, only the final state of simplex tableau will be printed out.
#
# The logic of the algorithm is divided into sections with clear marking and commenting to make it simple to understand
#
# More about the Simplex Method can be read from the accompanying thesis or
# from wikipedia: https://en.wikipedia.org/wiki/Simplex_algorithm 
# Additional help from:
# 1) https://explain-that.blogspot.com/2011/06/logic-of-how-simplex-method-works.html
# 2) https://math.libretexts.org/Bookshelves/Applied_Mathematics/Applied_Finite_Mathematics_(Sekhon_and_Bloom)/04%3A_Linear_Programming_The_Simplex_Method/4.02%3A_Maximization_By_The_Simplex_Method
def simplex(A, b, c, print_steps=False):
    # **********
    # START OF SETUP
    # **********

    # Prints out the inputs if set to do so
    if print_steps:
        objective_function = format_objective_function(A)
        constraints_str = format_constraints(b, c)

        print(f"Our goal is to maximize the objective function given by:\n{objective_function}")
        print("\nThis is subject to the following constraints:")
        print(constraints_str)

    # First, we must convert inequalities into equations by adding one slack variable for each inequality
    num_of_slack_variables = len(b)

    # The objective function should be rewritten with alternate signs since we are moving the coefficents to the left side
    # of the equation
    # Initial:   Z = 6x_1 - 5x_2
    # Rewritten: -6x_1 + 5x_2 + Z = 0
    A = [-a for a in A]

    # For each variable, we must add a slack variable to each inequality.
    # This is done by adding elements to each constraint in b, where 1 specifies a slack variable
    # This means that when b = [[4, 1, 1, 0], [2, 7, 0, 1]], the constrains will look like
    #  4x_1 + 1x_1 + s_1 >= 0
    #  2x_1 + 7x-2 + s_2 >= 0
    for i in range(num_of_slack_variables):
        b[i].extend([1 if i == j else 0 for j in range(num_of_slack_variables)])

    # Prints the inequality constraints with slack variables
    if print_steps:
        constraint_str_upd = format_constraints(b,c, num_of_slack_variables)
        print('\nState after adding slack variables to inequality constraints')
        print(f'b= {b}')
        print('Our new functions are now...')
        print(constraint_str_upd)

    # **********
    # END OF SETUP
    # **********    

    # Constructing the simplex tableau, where the first n-1 rows have a constraint in them and
    # and the last row holds the objective function
    # In addition to the slack variables, two additional columns for Z and c are added to each row.
    #  Z - will be set as 0 for all rows, except the last one which has the objective function in it
    #  c - constraint value (from input parameter c)
    s_tableau = construct_simplex_tableau(A, b, c)

    # Prints out the constructed simplex tableau
    if print_steps:
        print(f'\nCreated a Simplex tableau -> \n')
        format_simplex_tableau(s_tableau)


    # **********
    # START OF CONVERGENCE
    # **********    

    # Convergence consists of three steps, which are implemented as separate functions
    # 1. Find pivot column by iterating over the bottom row of s_tableau and finding the index of the element with most negative value
    # 2. Find pivot row by calculating quotients
    # 3. Performs "pivoting" by setting other values in the column as 0
    while min(s_tableau[-1][:-2]) < 0:  # Excluding Z and c from the check
        pivot_col_index = find_pivot_column(s_tableau, plot_for_gif)
        pivot_row_index = calculate_quotients_and_find_pivot_row(s_tableau, pivot_col_index=pivot_col_index, plot_for_gif=plot_for_gif)
        perform_pivoting(s_tableau, pivot_row_index=pivot_row_index, pivot_col_index=pivot_col_index)

        # Prints out the simplex tableau
        if print_steps:
            print(f"\ni=[{i}] After pivoting around pivot column {pivot_col_index} and pivot row {pivot_row_index}:")
            format_simplex_tableau(s_tableau)

    # **********
    # END OF CONVERGENCE
    # **********          

    # Prints out the formatted simplex tableau as the solution. The optimum value is in the bottom right corner.
    print(f'Solution found!')
    print(format_simplex_tableau(s_tableau))
    return s_tableau


# Identifies the column we should use for pivoting by finding the minimum
# value in the bottow row of the simplex tableau (s_tableau)
# returns an integer (pivot_col_index) that we'll use in the other methods
def find_pivot_column(s_tableau):
    bottom_row = s_tableau[-1][:-2]  # Exclude Z and c columns
    pivot_col_index = bottom_row.index(min(bottom_row))

    return pivot_col_index


# Calculates the quotients for a given column.
# A quotient is calculated by taking the right-most column (c - constraint values) and
# dividing it by the value the column specified by pivot_col_index
# The method returns an index for the row with smallest quotient.
def calculate_quotients_and_find_pivot_row(s_tableau, pivot_col_index):
    quotients = []  # Saved as a list
    # Iterates over the column and calculates quotients for all elements
    for i, row in enumerate(s_tableau[:-1]):  # Exclude the objective function row

        # Tries to calculate quotient for an element
        if row[pivot_col_index] > 0:  # Avoid division by zero or negative
            quotients.append((row[-1] / row[pivot_col_index], i))
        else:
            quotients.append((float('inf'), i))  # If quotient can't be calculated we should use inf instead

    _, pivot_row_index = min(quotients)  # Finds the index of the row with the samllest quotient.
    
    # Returns the row index
    return pivot_row_index


# The function is used to perform "pivoting" of the simplex tableau, which is given as an input parameter s_tableau
# Additional input parameters pivot_row_index and pivot_col_index are also used for creating a GIF if plot_for_gif is
# marked as True.
def perform_pivoting(s_tableau, pivot_row_index, pivot_col_index):

    # Locating the pivot element
    pivot_element = s_tableau[pivot_row_index][pivot_col_index]

    # Make pivot element 1
    # TODO: COMMENTS
    for j in range(len(s_tableau[0])):
        s_tableau[pivot_row_index][j] /= pivot_element

    # Make other entries in pivot column 0
    # TODO: COMMENTS
    for i, row in enumerate(s_tableau):
        if i != pivot_row_index:
            factor = row[pivot_col_index]
            for j in range(len(row)):
                row[j] -= factor * s_tableau[pivot_row_index][j]

# Constructs the simplex tableau from inputs
# TODO: COMMENTS!
def construct_simplex_tableau(A, b, c):
    num_of_variables = len(A)
    num_of_slack_variables = len(b)
    num_of_columns = num_of_variables + num_of_slack_variables + 2  # For Z and c
    num_of_rows = len(b) + 1  # Constraints + objective function

    # Initialize tableau with zeros
    s_tableau = [[0 for _ in range(num_of_columns)] for _ in range(num_of_rows)]

    # Fill in the slack variables and the constants
    for i in range(num_of_slack_variables):
        s_tableau[i][num_of_variables + i] = 1  # Set slack variable coefficient
        s_tableau[i][-1] = c[i]  # Set the constant

    # Fill in the objective function
    for i, coef in enumerate(A):
        s_tableau[-1][i] = coef  # Set objective function coefficients
    s_tableau[-1][-2] = 1  # Z coefficient for the objective function

    # Fill in the constraints
    for i, constraint in enumerate(b):
        for j, coef in enumerate(constraint[:-num_of_slack_variables]):  # Exclude slack variables
            s_tableau[i][j] = coef

    return s_tableau

