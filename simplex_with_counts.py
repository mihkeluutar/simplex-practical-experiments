"""
Author: Mihkel Uutar
Last updated: 01.05.2024

University of Tartu
Beyond Worst Case Complexity of the Simplex Algorithm

This file is a copy of simplex.py, but with added variable to count the
number of operations required to arrive at a solution.
"""


# If matrix == dense, then no optimization is done
# If matrix == sparse optimization is done
def simplex_w_counts(A, b, c, func='max', matrix='dense'):
    # a tracker for operations
    counts = {
        'comparisons': 0,  # x > y
        'assignments': 0,  # val = 0
        'arithmetic': 0,   # add, subtract, divide etc.
        'accesses': 0,     # list[0]
        'func_calls': 0    # simplex_w_count(A, b, c)
    }

    num_of_slack_variables = len(b)
    counts['assignments'] += 1  # Assigning to num_of_slack_variables
    counts['func_calls'] += 1   # Calling the len() function

    if func == 'max':
        counts['comparisons'] += 1  # Checking if func is 'max'
        A = [-a for a in A]
        counts['arithmetic'] += len(A)  # Iterating over each element in A
        counts['assignments'] += 1  # Reassigning A

    for i in range(num_of_slack_variables):
        counts['comparisons'] += 1  # Looping
        b[i].extend([1 if i == j else 0 for j in range(num_of_slack_variables)])
        counts['arithmetic'] += num_of_slack_variables  # For each conditional operation inside the list comprehension
        counts['comparisons'] += 1  # i == j
        counts['assignments'] += 1  # Extending b[i]
        counts['accesses'] += num_of_slack_variables + 1  # Accessing b[i] and each 1 or 0 conditionally added

    counts['func_calls'] += 1  # Calling construct_simplex_tableau
    s_tableau, counts = construct_simplex_tableau_w_counts(A, b, c, counts)
    counts['assignments'] += 1  # Assigning to s_tableau

    while min(s_tableau[-1][:-2]) < 0:
        counts['comparisons'] += 1  # For the while loop comparison
        counts['func_calls'] += 1  # For the min function
        counts['accesses'] += len(s_tableau[-1]) - 2  # Accessing elements in s_tableau[-1][:-2]
        pivot_col_index, counts = find_pivot_column_w_counts(s_tableau, counts)
        pivot_row_index, counts = calculate_quotients_and_find_pivot_row_w_counts(s_tableau, pivot_col_index, counts)

        # This part is useful for experimenting with sparse and dense matrixes. Sparse pivoting will try to exploit matrixes with values that are 0
        if matrix == 'dense':
            s_tableau, counts = perform_pivoting_w_counts(s_tableau, pivot_row_index, pivot_col_index, counts)
        elif matrix == 'sparse':
            s_tableau, counts = perform_sparse_pivoting_w_counts(s_tableau, pivot_row_index, pivot_col_index, counts)  
        else:
            print('Matrix type falsely specified. Allowed values are "sparse" and "dense"')
        
    return s_tableau, counts    


def find_pivot_column_w_counts(s_tableau, counts):
    bottom_row = s_tableau[-1][:-2]
    counts['accesses'] += len(s_tableau[-1]) - 2  # Accessing whole row worth of elements
    counts['assignments'] += 1  # For assigning the bottom_row variable

    min_value = min(bottom_row)
    counts['func_calls'] += 1   # Calling the min function
    counts['assignments'] += 1  # Assigning to min_value
    counts['accesses'] += 1     # Accessing bottom_row

    pivot_col_index = bottom_row.index(min_value)
    counts['func_calls'] += 1              # Calling the index function
    # counts['accesses'] += len(bottom_row)  # Accessing bottom_row
    counts['assignments'] += 1             # Assigning to the pivot_col_index

    return pivot_col_index, counts


def calculate_quotients_and_find_pivot_row_w_counts(s_tableau, pivot_col_index, counts):
    quotients = []
    counts['assignments'] += 1  # Assigning the quotients list

    for i, row in enumerate(s_tableau[:-1]):
        counts['comparisons'] += 1  # For the loop condition

        counts['accesses'] += 1  # Accessing row[pivot_col_index]
        if row[pivot_col_index] > 0:
            counts['comparisons'] += 1  # For the if condition
            counts['accesses'] += 2  # Accessing row[-1] and row[pivot_col_index]
            counts['arithmetic'] += 1  # Division
            counts['assignments'] += 1  # Appending to quotients
            
            quotient = (row[-1] / row[pivot_col_index], i)
            quotients.append(quotient)
        else:
            counts['comparisons'] += 1  # Moving to 'else' branch
            counts['assignments'] += 1  # Appending to quotients

            quotients.append((float('inf'), i))

    # The min function involves comparisons within the quotients list
    counts['comparisons'] += len(quotients) - 1
    counts['func_calls'] += 1  # Calling the min function

    _, pivot_row_index = min(quotients)
    counts['assignments'] += 1  # Assigning the pivot_row_index

    return pivot_row_index, counts


def perform_pivoting_w_counts(s_tableau, pivot_row_index, pivot_col_index, counts):
    pivot_element = s_tableau[pivot_row_index][pivot_col_index]
    counts['accesses'] += 2        # Accessing both column and row
    counts['assignments'] += 1     # Assigning pivot_element

    for j in range(len(s_tableau[0])):
      counts['comparisons'] += 1   # Loop condition
      counts['accesses'] += 1      # Accessing s_tableau[0] for loop condition check
      counts['accesses'] += 2      # Accessing s_tableau[pivot_row_index][j] before division
      s_tableau[pivot_row_index][j] /= pivot_element
      counts['arithmetic'] += 1    # Division
      counts['assignments'] += 1   # Assignment of the division result


    for i, row in enumerate(s_tableau):
        counts['comparisons'] += 1  # Loop condition

        if i != pivot_row_index:
            counts['comparisons'] += 1  # If condition check
            counts['accesses'] += 1  # Accessing row[pivot_col_index] to get factor
            factor = row[pivot_col_index]
            counts['assignments'] += 1  # Assigning factor

            for j in range(len(row)):
                counts['func_calls'] += 1  # Calling len() function
                counts['accesses'] += 4  # Accessing row[j], factor, and s_tableau[pivot_row_index][j]
                row[j] -= factor * s_tableau[pivot_row_index][j]
                counts['arithmetic'] += 2  # One for multiplication, one for subtraction
                counts['assignments'] += 1  # Assigning the result of subtraction

    return s_tableau, counts


# Detailed implementation with comments is in simplex.py
def perform_sparse_pivoting_w_counts(s_tableau, pivot_row_index, pivot_col_index, counts):
    pivot_element = s_tableau[pivot_row_index][pivot_col_index]
    counts['accesses'] += 2        # Accessing both column and row
    counts['assignments'] += 1     # Assigning pivot_element

    # Normalizing
    for j in range(len(s_tableau[0])):
        counts['comparisons'] += 1  # Loop condition
        counts['accesses'] += 1  # Accessing s_tableau[0] for loop condition check
        
        if s_tableau[pivot_row_index][j] != 0:  # Only update non-zero elements
            counts['accesses'] += 1  # Accessing s_tableau[pivot_row_index][j] before division
            s_tableau[pivot_row_index][j] /= pivot_element
            counts['arithmetic'] += 1  # Division
            counts['assignments'] += 1  # Assignment of the division result
    
    # Updating other rows as well
    for i in range(len(s_tableau)):
        counts['comparisons'] += 1  # Loop condition
        
        if i != pivot_row_index and s_tableau[i][pivot_col_index] != 0:
            counts['comparisons'] += 1  # If condition check
            counts['accesses'] += 1  # Accessing row[pivot_col_index] to get factor
            factor = s_tableau[i][pivot_col_index]
            counts['assignments'] += 1  # Assigning factor

            for j in range(len(s_tableau[0])):
                if s_tableau[pivot_row_index][j] != 0:  # Only update if not zero
                    counts['accesses'] += 3  # Accessing row[j], factor, and s_tableau[pivot_row_index][j] before arithmetic
                    s_tableau[i][j] -= factor * s_tableau[pivot_row_index][j]
                    counts['arithmetic'] += 2  # One for multiplication, one for subtraction
                    counts['assignments'] += 1  # Assigning the result of subtraction

    return s_tableau, counts           


def construct_simplex_tableau_w_counts(A, b, c, counts):
    num_of_variables = len(A)
    num_of_slack_variables = len(b)
    num_of_columns = num_of_variables + num_of_slack_variables + 2
    num_of_rows = num_of_slack_variables + 1

    counts['assignments'] += 4  # Assigning num_of_variables, num_of_slack_variables, num_of_columns, num_of_rows
    counts['func_calls'] += 2   # Calling len() twice
    counts['arithmetic'] += 3

    # Creating the simplex tableau
    s_tableau = [[0 for _ in range(num_of_columns)] for _ in range(num_of_rows)]
    counts['assignments'] += 1  # Assigning s_tableau
    counts['arithmetic'] += num_of_columns * num_of_rows  # Multiplying to determine the size of s_tableau

    for i in range(num_of_slack_variables):
        counts['comparisons'] += 1  # Loop condition
        s_tableau[i][num_of_variables + i] = 1
        s_tableau[i][-1] = c[i]
        counts['assignments'] += 2  # Assigning to s_tableau twice
        counts['accesses'] += 5
        counts['arithmetic'] += 1

    for i, coef in enumerate(A):
        counts['comparisons'] += 1  # Loop condition
        s_tableau[-1][i] = coef
        counts['assignments'] += 1  # Assigning coef to s_tableau
        counts['accesses'] += 2     # Accessing s_tableau[-1][i]

    s_tableau[-1][-2] = 1
    counts['assignments'] += 1  # Assigning 1 to s_tableau[-1][-2]
    counts['accesses'] += 2  # Accessing s_tableau[-1][-2]

    for i, constraint in enumerate(b):
        counts['comparisons'] += 1  # Loop condition
        for j, coef in enumerate(constraint[:-num_of_slack_variables]):
            counts['comparisons'] += 1  # For the inner loop to start
            s_tableau[i][j] = coef
            counts['assignments'] += 1  # Assigning coef to s_tableau
            counts['accesses'] += 2  # Accessing s_tableau[i][j]

    return s_tableau, counts