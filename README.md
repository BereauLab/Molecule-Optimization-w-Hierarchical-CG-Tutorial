# Tutorial on Coarse-Grained Molecular Optimization

This repository contains a tutorial on how to use hierarchical coarse-grained models and mutli-level Bayesian optimization for molecular discovery. Although the example system is quite simple, the methods are general and can be applied to more complex systems and larger molecules.

The tutorial is based on the paper [Navigating Chemical Space: Multi-Level Bayesian Optimization with Hierarchical Coarse-Graining](https://doi.org/10.1039/D5SC03855C).

## Setup
To run the tutorial, clone this repository:

```bash
git clone https://github.com/BereauLab/Molecule-Optimization-w-Hierarchical-Coarse-Graining.git
cd Molecule-Optimization-w-Hierarchical-Coarse-Graining
```

Next, a few dependencies are required:
- [GROMACS](https://www.gromacs.org/): This program is used to run molecular dynamics simulations. See [this page](https://manual.gromacs.org/current/install-guide/index.html) for installation instructions.

- Python packages: The provided `requirements.txt` file lists the necessary python packages. You can install them using pip:

    ```bash
    pip install -r requirements.txt
    ```
    It is recommended to use Python 3.11 and to create a virtual environment, e.g. using [`venv`](https://docs.python.org/3/library/venv.html) or [`uv`](https://docs.astral.sh/uv/).

## Running the Tutorial
To run the tutorial, launch the Jupyter notebook [Tutorial_on_Coarse_Grained_Molecular_Optimization.ipynb](Tutorial_on_Coarse_Grained_Molecular_Optimization.ipynb) in a Jupyter environment, e.g. using the command:

```bash
jupyter lab Tutorial_on_Coarse_Grained_Molecular_Optimization.ipynb
```
