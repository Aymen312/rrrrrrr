import streamlit as st
from ase import Atoms

st.title("Crystal Structure Viewer")
a = st.slider("Lattice constant", 3.0, 5.0, 4.024)

structure = Atoms(
    ['K', 'Mg', 'H', 'H', 'H'],
    positions=[...],
    cell=[[a, 0, 0], [0, a, 0], [0, 0, a]],
    pbc=True
)

st.write("Structure created successfully!")
st.write(structure)
