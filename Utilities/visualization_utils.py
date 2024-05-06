"""
Author: Mihkel Uutar
Last updated: 28.04.2024

University of Tartu
Beyond Worst Case Complexity of the Simplex Algorithm

The file has helpful functions for visualizing how the Simplex Method works. There is a 
function to create a GIF file of the solution process and some more functions to support it.
"""


import numpy as np
import matplotlib.pyplot as plt
import os
import imageio


# Clears the directory of all .png and .gif files. It's necessary for create_gif to work as expected.
def clear_directory(directory_path):
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.png') or file_name.endswith('.gif'):
            os.remove(os.path.join(directory_path, file_name))


# Plots the simplex_tableau and saves it as an image to later be stitched together into a GIF animation.
# 
# The function takes in Simplex Tableau (s_tableau) and currently active pivot_row_index and pivot_col_index
# To highlight them for better visaulization.            
def plot_simplex_tableau(s_tableau, pivot_row_index=None, pivot_col_index=None, save_path='helper/simplex_iterations'):
    
    # Creates a new directory if it does not exist yet
    os.makedirs(save_path, exist_ok=True)
    
    # Finds out what the image name shoule be (they all have to be in order)
    existing_files = [f for f in os.listdir(save_path) if f.endswith('.png')]
    next_image_num = max([int(f.split('_')[-1].split('.')[0]) for f in existing_files] + [0]) + 1
    
    # Setting up the plot
    _, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')
    
    # Turns the table into a NumPy array for easier manipulation later
    s_tableau_np = np.array(s_tableau)
    
    # Generate headers based on the structure of s_tableau_np
    num_of_variables = s_tableau_np.shape[1] - 2  # Last two columns are c and Z
    headers = ['x_{}'.format(i) for i in range(num_of_variables - len(s_tableau) + 1)] + \
              ['y_{}'.format(i) for i in range(1, len(s_tableau))] + \
              ['Z', 'c']
    
    # Prepend headers to the tableau for display
    headers_text = [headers] + np.round(s_tableau_np, 2).astype(str).tolist()
    
    simplex_table = ax.table(cellText=headers_text, loc='center', cellLoc='center')
    
    n_rows, n_cols = len(headers_text), len(headers_text[0])
    
    # Apply color customization to highlight active row and column
    for i in range(1, n_rows):  # Starting from row 1, since the first one is for headers
        for j in range(n_cols):
            cell = simplex_table[(i, j)]
            if i-1 == pivot_row_index or j == pivot_col_index: 
                cell.set_facecolor('yellow')  # Highlighing rows and columns
            if i-1 == pivot_row_index and j == pivot_col_index:
                cell.set_facecolor('orange')  # Pivot element is highlighted in a different color
    
    # Differentiating the header row
    for j in range(n_cols):
        cell = simplex_table[(0, j)]
        cell.set_facecolor('#dddddd')  # Light grey
        cell.set_text_props(weight='bold')

    # Saving file to a specified location
    plt.savefig(f"{save_path}/tableau_{next_image_num}.png", bbox_inches='tight')
    plt.close()


# Creates a GIF from all images saved into a folder. 
# The fucntion takes all of the images and order them by name (expected file names are 1.png, 2.png ...)
# fps is an additional parameter to set the frame rate of the GIF.
def create_gif(fps, image_folder='helper/simplex_iterations', gif_name='helper/simplex_iterations/simplex_process.gif'):
    images = []
    for file_name in sorted(os.listdir(image_folder), key=lambda x: int(x.split('_')[-1].split('.')[0])):
        if file_name.endswith('.png'):
            file_path = os.path.join(image_folder, file_name)
            images.append(imageio.imread(file_path))
    imageio.mimsave(gif_name, images, fps=fps)
                    
