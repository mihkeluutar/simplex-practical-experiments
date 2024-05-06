"""
Author: Mihkel Uutar
Last updated: 28.04.2024

University of Tartu
Beyond Worst Case Complexity of the Simplex Algorithm

This file contains different types of input generation functions, as well as some other utilities which
are helpful for generating inputs, such as simple a prime number generator.
"""


import numpy as np
import os
import random


# Defines the base directory so we always know where the primes and pseudoprimes should be stored
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Defines the paths for primes and pseudoprimes text files
PRIMES_DIR = os.path.join(BASE_DIR, 'helper', 'primes')
PSEUDO_PRIMES_DIR = os.path.join(BASE_DIR, 'helper', 'pseudoprimes')


# Helper for generating a list of primes in a given range
# Generating large lists of primes is really expensive and may run upto an hour, thus it makes sense to use something like primesieve instead
# https://github.com/kimwalisch/primesieve
# This function works by trying to read prime numbers form a text file into a list. If the file does not
# exist, function results to generating those instead.
#
# Generating a .txt file with primesieve is explained in the primesieve github page.
def generate_primes_in_range(min_val, max_val):
    primes = []

    file_name = f"primes_upto_{max_val}.txt"  # File to save the primes into
    file_path = os.path.join(PRIMES_DIR, file_name)

    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            primes = [int(line.strip()) for line in file] 
    else:
        print(f'The path {file_path} does not exist, starting to generate primes')
        for i in range(min_val, max_val):
            if i > 1:  # 0 and 1 are not primes
                for j in range(2, int(i / 2) + 1):
                    if i % j == 0:
                        break
                else:
                    primes.append(i)

        # Writing the primes to a file so they can be accessed another time
        with open(file_path, 'w') as file:
            for prime in primes:
                file.write(f"{prime}\n")                 

    return primes                


# Generates prime-like integers in a given range. Pseudoprimes are integers in a given range
# which follow a distribution similar to prime numbers. Prime numbers become less common, the larger
# they become. PSeudoprimes follow the same idea.
# 
# https://en.wikipedia.org/wiki/Prime_number_theorem
def generate_pseudoprimes_in_range(min_val, max_val):
    pseudoprimes = []

    file_name = f"pseudoprimes_upto_{max_val}.txt"  # File to save the pseudoprimes into
    file_path = os.path.join(PSEUDO_PRIMES_DIR, file_name)

    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            pseudoprimes = [int(line.strip()) for line in file] 
    else:
        x = 0
        while True:
            n = x**2 + x + 41
            if n > max_val:
                break
            if n >= min_val:
                pseudoprimes.append(n)
            x += 1

        # Writing the pseudoprimes to a file
        with open(file_path, 'w') as file:
            for pseudoprime in pseudoprimes:
                file.write(f"{pseudoprime}\n")  
    
    return pseudoprimes


# Returns a list limited to max_len items. Samples randomly if reduction is needed.
def limit_list_size(list, max_len):
    return list if len(list) <= max_len else random.sample(list, max_len)


# Function that helps to apply variane within specified bounds
def apply_variance_and_clip(x, min_val, max_val, variation_range):
    variance = np.random.randint(-variation_range, variation_range)
    x += variance
    x = max(x, min_val)  # Ensure that x is larger or equal than min_val
    x = min(x, max_val)  # Ensure that x is not larger than max_val
    return x


# Generates an input in a random fashion. The function uses min_val and max_val to specify the
# range of values for each individual variable
def generate_random_simplex_input(inequalities_n, variables_n, min_val=1, max_val=100):
    # Generates the objective function coefficients
    A = np.random.randint(min_val, max_val, size=variables_n).tolist()
    
    # Generates the coefficients for the inequalities
    b = np.random.randint(min_val, max_val, size=(inequalities_n, variables_n)).tolist()
    
    # Generates the right-hand side values for the inequalities
    c = np.random.randint(min_val, max_val, size=inequalities_n).tolist()
    
    return A, b, c


# Generates a "symmetric" simplex input. Symmetrical input follows a pattern where every
# second inequality reverses the sign of a chosen variable, maintaining the same absolute variable from
# the previous inequality
#
# It could look something like this (7x_2 is the symmetrical variable):
# 2x_1 + 7x_2 + 4_x3 >= 18
# 3x_1 - 7x_2 - 9x_3 >= 2
def generate_symmetric_simplex_input(inequalities_n, variables_n, min_val=0, max_val=9):
    # Generates coefficients for the objective function
    A = np.random.randint(min_val, max_val, size=variables_n).tolist()

    # Generates inequality constraints
    b = []
    for i in range(inequalities_n):
        if i % 2 == 1:
            previous = b[i-1]
            current = previous.copy()

            random_index = np.random.randint(0, len(previous) - 1)
            current[random_index] = -current[random_index]

            b.append(current)
        else:
            b.append(np.random.randint(min_val, max_val, size=variables_n).tolist())

    # Generates values for each inequality
    c = np.random.randint(1, max_val*variables_n, size=inequalities_n).tolist()

    return A, b, c


# Generates an input, where variables for each inequality are defined by a geometric progression
def generate_geometric_simplex_input(inequalities_n, variables_n, min_val=1, max_val=1000):
    # Generating objective function as a geometric progression
    A = [min(min_val * 2**i, max_val) for i in range(variables_n)]
    
    # Generates inequalities as a geometric progression
    b = []
    for i in range(inequalities_n):
        row = [min_val] * variables_n
        for j in range(variables_n):  # Making sure variable value is not larger than max_val
            value = min_val * 2**(i+j)
            row[j] = min(value, max_val)
        b.append(row)
    
    # Generates inequality values as a geometric progression
    c = [min(min_val * 2**(i+1) - 1, max_val) for i in range(variables_n)]
    
    return A, b, c


# Generates an input in a similar way to geometric progression, but adds some variance to all variables
# This method takes the input generated by generate_geometric_simplex_input as base values.
def generate_varied_geometric_simplex_input(inequalities_n, variables_n, min_val=1, max_val=1000, variation_range=20):

    A, b, c = generate_geometric_simplex_input(inequalities_n, variables_n, min_val, max_val)

    # Applying variance
    A = [apply_variance_and_clip(value, min_val, max_val, variation_range) for value in A]
    b = [[apply_variance_and_clip(value, min_val, max_val, variation_range) for value in row] for row in b]
    c = [apply_variance_and_clip(value, min_val, max_val, variation_range) for value in c]

    return A, b, c


# Generates an input where values for each inequaity are defined by linear progression. The function
# has a parameter step_range, which specifies the maximum difference between two adjacent variables.
def generate_linear_simplex_input(inequalities_n, variables_n, min_val=1, max_val=1000, step_range=20):
    
    # Calculates the exact step based on the number of variables
    step = max((step_range // variables_n) if variables_n > 1 else step_range, 1)
    
    # Generates the objective function as a linearly increasing sequence
    A = [min(min_val + step * i, max_val) for i in range(variables_n)]
    
    # Generate b (inequalities) as a matrix where each row starts at an incremented base and increases linearly
    b = []
    for i in range(inequalities_n):
        base = min_val + step * i
        row = [min(max(base + step * j, min_val), max_val) for j in range(variables_n)]
        b.append(row)
    
    # Generates inequality constraint values
    c = np.random.randint(min_val, min_val + step_range, size=variables_n).tolist()
    
    return A, b, c


# Generates a linearly progressing simplex input and adds variance. Uses generate_linear_simplex_input as a base
def generate_varied_linear_simplex_input(inequalities_n, variables_n, min_val, max_val, step_range=-1, variation_range=-1):
    
    # In case step_range and variation_range are not specified we'll set them to something arbitrary.
    if step_range < 0:
        step_range = int(10*(max_val - min_val) / variables_n)

    if variation_range < 0:
        variation_range = int(10*(max_val - min_val) / variables_n)

    A, b, c = generate_linear_simplex_input(inequalities_n, variables_n, min_val, max_val, step_range)

    # Applying variance
    A = [apply_variance_and_clip(value, min_val, max_val, variation_range) for value in A]
    b = [[apply_variance_and_clip(value, min_val, max_val, variation_range) for value in row] for row in b]
    c = [apply_variance_and_clip(value, min_val, max_val, variation_range) for value in c]

    return A, b, c


# This function generates inputs in a way, where every variable, coefficient and inequality value is
# a prime number. A list of prime numbers in the range should be given as an input value, else they
# will be calculated separately.
# 
# NOTE: There are about 9592 prime numbers that are between 1 and 100000 and 168 between 1 and 1000
def generate_input_with_only_primes(inequalities_n, variables_n, min_value, max_value=1000, primes=[]):
    if primes == []:
        primes = generate_primes_in_range(min_value, max_value)    

    A = random.sample(primes, variables_n)
    b = [random.sample(primes, variables_n) for _ in range(inequalities_n)]
    c = random.sample(primes, inequalities_n)

    return A, b, c


# Generates inputs, where every value is a "pseudoprime". Pseudoprimes can be given as a list
# upon input.
#
# More about what is meant by pseudoprimes is written next to the generate_pseudoprimes_in_range function
def generate_pseudoprime_simplex_input(inequalities_n, variables_n, min_value, max_value=1000, pseudoprimes=[]):
    if pseudoprimes == []:
        pseudoprimes = generate_pseudoprimes_in_range(min_value, max_value)    

    A = random.sample(pseudoprimes, variables_n)
    b = [random.sample(pseudoprimes, variables_n) for _ in range(inequalities_n)]
    c = random.sample(pseudoprimes, inequalities_n)

    return A, b, c


# Generates inputs that should somewhat loosely follow a Gaussian Distribution. These are generated
# in a "backwards" manner, where mean and standard deviation are defined first and the actual
# inputs second.
#
# The generation method takes min_value and max_value as parameters to set a range for each individual 
# variable.
#
# More information: https://en.wikipedia.org/wiki/Normal_distribution
def generate_gaussian_simplex_input(inequalities_n, variables_n, min_value, max_value=1000):

    # Define mean and standard deviation for the Gaussian distribution
    mean = (max_value + min_value) / 2
    std_dev = (max_value - min_value) / 6  # Will ensure that each value is within 3 standard deviations from the mean. 99.7% of it atleast :)
    
    # Generates A - objective function coefficients
    A = np.random.normal(mean, std_dev, variables_n)
    
    # Generates b - inequality variable values
    b = np.random.normal(mean, std_dev, (inequalities_n, variables_n))
    
    # Generate c - right-hand side values of inequalities
    c = np.random.normal(mean, std_dev, inequalities_n)
    
    # Clip values if needed and convert them to integers
    # clip - if value is larger than max_value, sets it as max_value; if smaller sets it as min_value
    # rint - rounds elements in an array to the nearest integer
    A = np.clip(np.rint(A), min_value, max_value).astype(int).tolist()
    b = np.clip(np.rint(b), min_value, max_value).astype(int).tolist()
    c = np.clip(np.rint(c), min_value, max_value).astype(int).tolist()

    return A, b, c


# The function sets random variables in each inequality as zero to introduce artificial sparsity.
# sparsity is a modifier which sets the percentage of elements which well be set as zero.
# A sparsity of 0.5 means that 50% of the variables in each inequality will be 0.
def make_sparse_simplex_input(b, c, sparsity=0.5):
    sparse_b = []

    for row in b:
        num_zeros = int(len(row) * sparsity)  # Calculate the number of zeros needed
        non_zero_indices = random.sample(range(len(row)), len(row) - num_zeros)  # Random indexes for elements that are not changed
        sparse_row = [0 if i not in non_zero_indices else row[i] for i in range(len(row))]  # Create sparse row
        sparse_b.append(sparse_row)

    # c remains unchanged, but can be modified if need arises
    sparse_c = c

    return sparse_b, sparse_c


# By default makes all elements ABOVE the top diagonal as zeros
# TODO: Comments ...
def make_diagonal_zeros(b, above_diagonal=True):
    no_constraints = len(b)
    no_variables = len(b[0])
    
    if above_diagonal:
        for i in range(no_constraints):
            for j in range(i + 1, no_variables):
                b[i][j] = 0
    else:
        for i in range(1, no_constraints):
            for j in range(min(i, no_variables)):
                b[i][j] = 0

    return b


# The makes a temporary element for inequalities and their values, shuffles and separates them.
def shuffle_simplex_inputs_rows(b, c):
    temp = list(zip(b, c))
    random.shuffle(temp)
    shuffled_b, shuffled_c = zip(*temp)

    # returns shuffled lists
    return list(shuffled_b), list(shuffled_c)


# The function generates a list of indexes as the new order for current inequalities
# and orders them and the inequality values in that order. 
# It is important to shuffle both in the same order to not mix up variable values.
def shuffle_simplex_inputs_columns(A, b):
    # Generate a new order for the variables
    new_order = list(range(len(A)))
    random.shuffle(new_order)

    # Apply this new order to A
    A_shuffled = [A[i] for i in new_order]

    # We apply the new variable order to each row (constraint) in b.
    b_shuffled = [[constraint[i] for i in new_order] for constraint in b]

    # Returns both the objective function and constraints
    return A_shuffled, b_shuffled