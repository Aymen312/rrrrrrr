import streamlit as st
from ase import Atoms
from ase.visualize import view

st.title("Simple Crystal Visualizer")

a = st.slider("Lattice constant (Å)", 3.0, 5.0, 4.024)

structure = Atoms(
    ['K', 'Mg', 'H', 'H', 'H'],
    positions=[
        [0, 0, 0],
        [a/2, a/2, a/2],
        [0, a/2, a/2],
        [a/2, 0, a/2],
        [a/2, a/2, 0]
    ],
    cell=[a, a, a],
    pbc=True
)

if st.button("Show Structure"):
    st.write("Crystal structure created!")
    st.write(structure)
    # Note: 'view()' won't work in Streamlit Cloud
    # Use st.image() with a saved PNG instead
