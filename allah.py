import streamlit as st
from ase import Atoms
from gpaw import GPAW, PW
import matplotlib.pyplot as plt

st.title("KMgH₃ DFT Simulation with GPAW")
st.markdown("""
This app runs a Density Functional Theory (DFT) calculation for **KMgH₃** using GPAW.
""")

# Sidebar controls for parameters
with st.sidebar:
    st.header("Simulation Parameters")
    a = st.number_input("Lattice constant (Å)", value=4.024, step=0.01)
    cutoff = st.number_input("Plane-wave cutoff (eV)", value=800, step=50)
    kpts = st.slider("k-point grid", 2, 12, 8)
    width = st.number_input("Fermi smearing width (eV)", value=0.1, step=0.01)

# Define the KMgH₃ structure
kmg_h3 = Atoms(
    symbols=['K', 'Mg', 'H', 'H', 'H'],
    positions=[
        (0, 0, 0),                # K at (0,0,0)
        (0.5*a, 0.5*a, 0.5*a),   # Mg at (0.5,0.5,0.5)
        (0, 0.5*a, 0.5*a),       # H at (0,0.5,0.5)
        (0.5*a, 0, 0.5*a),       # H at (0.5,0,0.5)
        (0.5*a, 0.5*a, 0)        # H at (0.5,0.5,0)
    ],
    cell=[[a, 0, 0], [0, a, 0], [0, 0, a]],
    pbc=True
)

# Run DFT calculation when the user clicks the button
if st.button("Run DFT Calculation"):
    st.write("Running DFT calculation... (This may take a while)")

    # Set up GPAW calculator
    calc = GPAW(
        mode=PW(cutoff),
        xc='PBE',
        kpts=(kpts, kpts, kpts),
        occupations={'name': 'fermi-dirac', 'width': width},
        txt='kmg_h3_dft.txt'
    )

    kmg_h3.set_calculator(calc)
    energy = kmg_h3.get_potential_energy()
    st.success(f"Calculation completed! Total energy: {energy:.3f} eV")

    # Save and reload the calculator
    calc.write('kmg_h3.gpw', mode='all')
    calc = GPAW('kmg_h3.gpw')

    # Compute DOS
    energies, dos = calc.get_dos(npts=2000, width=0.1)

    # Plot DOS
    st.subheader("Density of States (DOS)")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(energies, dos, label="Total DOS", color='black')
    ax.set_xlabel("Energy (eV)")
    ax.set_ylabel("DOS (states/eV)")
    ax.legend()
    st.pyplot(fig)

    # Optional: Show structure
    st.subheader("Crystal Structure")
    st.write(kmg_h3)
