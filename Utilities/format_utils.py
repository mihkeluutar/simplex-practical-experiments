"""
Author: Mihkel Uutar
Last updated: 28.04.2024

University of Tartu
Beyond Worst Case Complexity of the Simplex Algorithm

This file contains functions that are mainly used for formatting inequalities, objective functions, simplex tableaus
or anything else for printing. They are used mainly for validating the correctness or more detailed study of
the Simplex Methods behavior ona  specific input.

These functions don't serve a real purpose in making this implemenetation of the Simplex Algorithm work.
"""


import json
import os


# Defines the base directory so we always know where the primes and pseudoprimes should be stored
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_RESULT_DIR = os.path.join(BASE_DIR, 'helper/results')


# Prints out a nicely formatted example of a generated input. An input should be generated before calling this function
# and passed in as parameters.
def print_example(A, b, c, input_type):
    print(f'Example for {input_type} input:')
    print(f'A={A}, b={b}, c={c}\n')
    objective_function = format_objective_function(A)
    constraints_str = format_constraints(b, c, False)
    print(f"Our goal is to maximize the objective function given by:\n{objective_function}")
    print("Which is subject to the following constraints/inequalities:")
    print(constraints_str)
    print('---\n')


# Formats inequalities into a printable format to use in logging out each step or to see each inequality
# in a way it would be shown in a real-life problem
# positivity_constraint adds another constraint for every single element to be larger than zero.
# This is purely for printing purposes and does not affect the input or Simplex Method's behavior
def format_constraints(b, c, positivity_constraint=True):
    constraints_str = []
    num_vars = len(b[0])

    for i, (constraint, bound) in enumerate(zip(b, c)):
        constraint_variables = []
        for j, coef in enumerate(constraint):
            # Formats the coefficient and variable, taking into account the sign so it won't print out + -7x_2
            if coef > 0:
                element = f'{coef}x_{j+1}' if j == 0 else f' + {coef}x_{j+1}'
            else:
                element = f' - {-coef}x_{j+1}' if coef < 0 else f' + 0x_{j+1}'
            constraint_variables.append(element)
        
        # Join all elements in an inequality into a single string.
        constraint_eq = ''.join(constraint_variables)

        # IC - Inequality Constraint; shortened for better printing.
        constraints_str.append(f'IC {i+1}: {constraint_eq} <= {bound}')

    if positivity_constraint:
        # Positivity constraint for all varaibles
        positivity_constraints = ', '.join(f'x_{i+1} >= 0' for i in range(num_vars))
        constraints_str.append(f'Positivity: {positivity_constraints}')

    return '\n'.join(constraints_str)


# Formats objective function into a nice, readable string.
# This takes into account either the Simplex is built for maximizing, or minimizing the objective function.
def format_objective_function(A, func='max'):
    # If maximizing, reverse the sign of each coefficient.
    if func == 'max':
        A_neg = [-coef for coef in A]
    else:
        A_neg = A.copy()
    objective_function = ' + '.join(f'{coef}x_{i+1}' for i, coef in enumerate(A_neg))

    # Adds Z to represent the objective function
    objective_function += ' + Z = 0'
    return objective_function    


# Formats the simplex tableau, which holds the objective function, inequalities and their values
# as a table and prints it out.
# Takes s_tableau (Simplex Tableau) as an input which can be constructed from inputs via construct_simplex_tableau
def format_simplex_tableau(s_tableau):
    # Determining the number of variables and inequalities based on the table size
    num_of_variables = len(s_tableau[0]) - 2  # Excludes Z and c columns
    num_of_slack_variables = len(s_tableau) - 1  # Excludes objective function row (always in the bottom)

    # Prepares column headers
    headers = ['x_{}'.format(i) for i in range(num_of_variables - num_of_slack_variables)] + \
              ['y_{}'.format(i) for i in range(num_of_slack_variables)] + \
              ['Z', 'c']

    # Calculates column widths based on headers
    column_widths = [max(len(header), max((len(f"{cell:.2f}") for cell in column), default=0)) + 2
                     for header, column in zip(headers, zip(*s_tableau))]

    # Prints out headers with correct alignment
    header_row = ''.join(header.center(width) for header, width in zip(headers, column_widths))
    print(header_row)

    # Divider for separating the objective function row
    divider = '-' * len(header_row)

    # Print each row of the tableau with proper alignment
    for i, row in enumerate(s_tableau):
        if i == len(s_tableau) - 1:  # Add divider before the last row (objective function)
            print(divider)
        formatted_row = ''.join(f"{cell: {width}.2f}" for cell, width in zip(row, column_widths))
        print(formatted_row)


# The function takes experiment parameters as input, as well as the
# experiment results directory and writes it into a file as JSON for further
# analysis.
def save_results(constraints_n, variables_n, max_iterations, number_of_runs_for_iteration, min_value, max_value, data_dict, file_prefix='', file_suffix=''):
    # Constructs the filename according to experiment parameters.
    filename = f'{file_prefix}_{constraints_n}_{max_iterations}_v{variables_n}_{max_iterations}_i{max_iterations}_r{number_of_runs_for_iteration}_min{min_value}_max{max_value}_{file_suffix}.txt'
    
    # Open the file in write mode and write the dictionary as JSON
    file_path = os.path.join(DEFAULT_RESULT_DIR, filename)
    with open(file_path, 'w') as file:
        json.dump(data_dict, file, indent=4)
    
    print(f'Data saved to {file_path}')