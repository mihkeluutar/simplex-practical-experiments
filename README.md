# Beyond Worst-Case Complexity of the Simplex Method

This codebase supplements my thesis by the same name. It has the necessary functions for running three practical experiments on the performance of the Simplex Method based on input distributions.

## Running the Code

The experiments were tested to work with ```Python 3.10.13``` and have not been verified to run on other versions. However they should still run as the necessary packages are quite basic (Matplotlib, Numpy).

## Structure of the Codebase

### Cool Bits

This directory is for archiving some findings or tools that were not necessary for the thesis itself, but could be useful for further work. The directory contains examples of Pseudoprime plotting in ``pseudoprimes.ipynb`` and has some helpful functions for generating LaTeX formatted tables and Plot the results in the ```utilities.ipynb``` file.

Please note, that the ``utilities.ipynb`` contents were used in the later stages of the thesis to format the final document and should be used with caution, as they might not work for different formats of inputs.

### Final Results

This directory hosts the results received from the final iterations of the experiments and are saved into three subfolders - one for each experiment. The folders containt both raw ```.txt``` files with ``json`` formatted data, graphs and LaTeX tables.

### helper

This directory has some text files with pseudoprimes and prime numbers to save time calculating them before experiments.

### Utilities

The directory has functions for formatting some stages in the Simplex Methods operations (like printing out the Simplex Tableu or the Inequalities) hosted in the ``format_utils.py`` file.

The directory also has a file for the functins needed to generate inputs - ``input_gen_utils.py`` which has a separate function for each type of input. The file also has helper functions to generate prime numbers and pseudoprimes.

### `distributions.ipynb`

This is a Jupyter Notebook file to experiment with visualizations of the different data distributions

### ```simplex.py```

The file has an implementation for the Simplex Method which uses Dantzigs pivot rule as a base. More about the implementation can be read from the comments and thesis itself.

### ```simplex_with_counts.py```

This file is in essence a copy of the ``simplex.py`` file, but with added variable to count the number of operations done at each iteration of the Simplex Method.

### ```thesis_experiments.ipynb```

The most important file for the thesis - it hosts all experiments explained in the paper and has parameters to set specifics. The experiments run quite quickly for a smaller number of iterations and small inputs, but may take several hours on a local computer for larger inputs. Every experiment is explained before corresponding code.

---