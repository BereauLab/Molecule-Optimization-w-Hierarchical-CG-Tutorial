"""This file contains suggestions for solving the
final three coding tasks in the tutorial notebook."""

import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from rdkit import Chem
from rdkit.Chem import BRICSBuild
from IPython.display import clear_output


def cell_1(encoded: np.ndarray, bo_predictions: list[tuple[np.ndarray, np.ndarray]]):
    """
    For TODO: Visualize the BO prediction over the course of the optimization

    The code below visualizes the predictions of the surrogate model over the
    course of the optimization.
    """
    for i, bo_prediction in enumerate(bo_predictions):
        clear_output(wait=True)
        fig, ax = plt.subplots(figsize=(7, 6))
        # TODO: Visualize the BO prediction using a scatterplot, kernel density estimation, etc.
        # We want to observe the change of the surrogate model predictions over the course of the
        # optimization.

        # Possible solution:
        scatter = ax.scatter(encoded[:, 0], encoded[:, 1], c=bo_prediction[0])
        fig.colorbar(scatter, ax=ax, label=r"$\Delta\Delta G / kcal/mol$")
        ax.set(
            xlabel="Encoding dimension 1",
            ylabel="Encoding dimension 2",
            title=f"Optimization step {i}",
        )

        plt.show()
        time.sleep(0.4)


def cell_2(
    high_res_molecules: list[str],
    simulation_data: dict[int, float],
    bo_predictions: list[tuple[np.ndarray, np.ndarray]],
):
    """
    For TODO: Using the latest predictions and uncertainties from the surrogate model, analyze
    the overall characteristics of promising CG molecular candidates beyond those already
    evaluated. What chemical design rules can be derived from these insights?

    The code below selects the top 10 molecules predicted to have the lowest
    """
    # Select molecules with highest predicted transfer free energy
    top_indices = np.argsort(bo_predictions[-1][0])[-10:]
    # Select molecules with low prediction uncertainty
    uncertainty_cutoff = sorted(bo_predictions[-1][1])[30]
    low_uncertainty_indices = np.nonzero(bo_predictions[-1][1] < uncertainty_cutoff)[0]
    # Calculate intersection of top molecules with low uncertainty
    top_indices = np.intersect1d(top_indices, low_uncertainty_indices)
    top_predicted_molecules = [high_res_molecules[i] for i in top_indices]
    # Print results
    print("Top predicted molecules:", top_predicted_molecules)
    print(
        "Predicted free energies:",
        [f"{v:.3f}" for v in bo_predictions[-1][0][top_indices]],
    )
    print(
        "Predicted uncertainties:",
        [f"{v:.3f}" for v in bo_predictions[-1][1][top_indices]],
    )
    evaluated_indices = [int(i) for i in simulation_data.keys()]
    print(
        "Part of evaluated data: ",
        [f"{str(v in evaluated_indices):>5}" for v in top_indices],
    )


def cell_3():
    """
    For TODO: The files oco-w-coarse-grained.csv and oco-w-fragments.csv contain octanol water
    transfer free energies for the different bead types and various organic fragements.
    Although a simplified approach that ignores some other properties, these values can be used
    to match atomistic fragments and reconstruct atomistic structures from the CG design rules
    derived earlier. Implement the matching of octanol water transfer free energies and use the
    RDKit method BRICSBuild to reconstruct atomistic molecules. The fragments provided in
    oco-w-fragments.csv were derived using the BRICSDecompose method and are ready to use with
    BRICSBuild.

    The code below matches octanol water transfer free energies and reconstructs atomistic
    molecules using RDKit.
    """
    oco_w_cg = pd.read_csv("oco-w-coarse-grained.csv")
    oco_w_atomistic = pd.read_csv("oco-w-fragments.csv")
    # Extract ddG values for the two beads in the CG model
    oco_w_bead1 = oco_w_cg.loc[oco_w_cg["Bead"] == "C1"]["ddG (kJ/mol)"].item()
    oco_w_bead2 = oco_w_cg.loc[oco_w_cg["Bead"] == "P6"]["ddG (kJ/mol)"].item()
    print(
        f"Octanol-water transfer free energies: {oco_w_bead1} kcal/mol and {oco_w_bead2} kcal/mol"
    )
    # Find all fragments that match the bead ddG within 1.0 kJ/mol
    bead1_fragments = oco_w_atomistic.loc[
        np.abs(oco_w_atomistic["ddG (kJ/mol)"] - oco_w_bead1) < 1.0
    ]["Fragment"].tolist()
    bead2_fragments = oco_w_atomistic.loc[
        np.abs(oco_w_atomistic["ddG (kJ/mol)"] - oco_w_bead2) < 1.0
    ]["Fragment"].tolist()
    # Loop over all combinations of fragments and reconstruct molecules using BRICSBuild
    reconstructed_molecules = []
    for frag1 in bead1_fragments:
        frag_mol1 = Chem.MolFromSmiles(frag1)
        for frag2 in bead2_fragments:
            frag_mol2 = Chem.MolFromSmiles(frag2)
            new_mols = list(BRICSBuild([frag_mol1, frag_mol2]))
            if len(new_mols) > 0:
                # Filter molecules that were constructed from two times frag1 or two times frag2
                bad_mols1 = [Chem.MolToSmiles(m) for m in BRICSBuild([frag_mol1])]
                bad_mols2 = [Chem.MolToSmiles(m) for m in BRICSBuild([frag_mol2])]
                new_mols = [
                    m
                    for m in new_mols
                    if Chem.MolToSmiles(m) not in bad_mols1
                    and Chem.MolToSmiles(m) not in bad_mols2
                ]
                reconstructed_molecules.extend(new_mols)
    print(f"Reconstructed {len(reconstructed_molecules)} molecules")
    # Visualize reconstructed molecules
    img = Chem.Draw.MolsToGridImage(
        reconstructed_molecules,
        molsPerRow=5,
        subImgSize=(200, 200),
        maxMols=len(reconstructed_molecules),
        legends=[f"Mol {i+1}" for i in range(len(reconstructed_molecules))],
    )
    return img
