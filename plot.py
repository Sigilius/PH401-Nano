import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go 

class NanoparticleAnalyzer:
    @staticmethod
    def cuboctahedral_total(layer):
        """Calculate total atoms in cuboctahedral nanoparticle."""
        return int((10 * (layer ** 3) + 15 * (layer ** 2) + 11 * layer + 3) / 3)

    @staticmethod
    def cuboctahedral_surface(layer):
        """Calculate surface atoms in cuboctahedral nanoparticle."""
        return int(10 * (layer ** 2) + 2)

    @staticmethod
    def spherical_total(layer):
        """Calculate total atoms in spherical nanoparticle."""
        return int((10 * (layer ** 3) - 15 * (layer ** 2) + 11 * layer - 3) / 3)

    @staticmethod
    def spherical_surface(layer):
        """Calculate surface atoms in spherical nanoparticle."""
        return int(10 * (layer ** 2) - 20 * layer + 12)

    @staticmethod
    def fcc_total(layer):
        """Calculate total atoms in Face-Centered Cubic (FCC) nanoparticle."""
        return int(4 * layer**3)

    @staticmethod
    def fcc_surface(layer):
        """Calculate surface atoms in Face-Centered Cubic (FCC) nanoparticle."""
        return int(4 * (layer**2 + layer + 1))

    @staticmethod
    def sc_total(layer):
        """Calculate total atoms in Simple Cubic (SC) nanoparticle."""
        return int(layer**3)

    @staticmethod
    def sc_surface(layer):
        """Calculate surface atoms in Simple Cubic (SC) nanoparticle."""
        return int(6 * (layer**2))

def main():
    st.set_page_config(page_title="Nanoparticle Analyzer", layout="wide")
    st.title("Nanoparticle Structure and Properties Analyzer")

    # Sidebar for input parameters
    st.sidebar.header("Nanoparticle Configuration")

    # Shape selection
    shape = st.sidebar.radio("Select Nanoparticle Shape:", 
                              ('Cuboctahedral', 'Spherical', 'FCC', 'SC'))

    # Application-based size ranges
    application_ranges = {
        'Optical': (40, 100),
        'Electrical': (10, 20),
        'Magnetic': (1, 10),
        'Strength': (1, 50),
        'Any Value': (1, 100)
    }

    # Application selection
    application = st.sidebar.selectbox(
        "Select Application:", 
        list(application_ranges.keys()), 
        index=4
    )

    # Dynamic size slider based on application
    min_range, max_range = application_ranges[application]
    values = st.sidebar.slider(
        'Specify Size Limits for Nanoparticle (nm)', 
        min_range, max_range, (min_range, 50)
    )

    # Computation and analysis
    sizes = list(range(values[0], values[1] + 1))

    # Select appropriate calculation methods based on shape
    if shape == 'Cuboctahedral':
        total_func = NanoparticleAnalyzer.cuboctahedral_total
        surface_func = NanoparticleAnalyzer.cuboctahedral_surface
    elif shape == 'Spherical':
        total_func = NanoparticleAnalyzer.spherical_total
        surface_func = NanoparticleAnalyzer.spherical_surface
    elif shape == 'FCC':
        total_func = NanoparticleAnalyzer.fcc_total
        surface_func = NanoparticleAnalyzer.fcc_surface
    else:  # Simple Cubic
        total_func = NanoparticleAnalyzer.sc_total
        surface_func = NanoparticleAnalyzer.sc_surface

    # Compute atom data
    atom_data = []
    atoms_surface = []
    atoms_bulk = []

    for size in sizes:
        total_atoms = total_func(size)
        surface_atoms = surface_func(size)
        bulk_atoms = total_atoms - surface_atoms
        
        atom_data.append([
            size, 
            bulk_atoms, 
            surface_atoms, 
            total_atoms, 
            (surface_atoms/total_atoms)*100, 
            (bulk_atoms/total_atoms)*100
        ])
        
        atoms_surface.append((surface_atoms/total_atoms)*100)
        atoms_bulk.append((bulk_atoms/total_atoms)*100)

    # Create DataFrame for display
    atoms_df = pd.DataFrame(
        atom_data, 
        columns=[
            'Particle Size (nm)', 
            'Bulk Atoms', 
            'Surface Atoms', 
            'Total Atoms', 
            '% Surface Atoms', 
            '% Bulk Atoms'
        ]
    )

    # Display results
    st.header(f"{shape} Nanoparticle Analysis")
    
    # Table of first 10 results
    st.subheader("Atom Distribution")
    st.dataframe(atoms_df.head(10), use_container_width=True)

    # Plotting
    st.header("Visualization")

    # Surface vs Bulk Percentage
    fig_percent = go.Figure()  
    fig_percent.add_trace(
        go.Scatter(
            x=sizes, 
            y=atoms_surface, 
            mode='lines+markers', 
            name='Surface Atoms %'
        )
    )
    fig_percent.add_trace(
        go.Scatter(
            x=sizes, 
            y=atoms_bulk, 
            mode='lines+markers', 
            name='Bulk Atoms %'
        )
    )
    fig_percent.update_layout(
        title=f'Percentage of Surface and Bulk Atoms in {shape} Nanoparticles',
        xaxis_title='Particle Size (nm)',
        yaxis_title='Percentage (%)'
    )
    st.plotly_chart(fig_percent, use_container_width=True)

    # Surface to Bulk Ratio
    surface_to_bulk_ratio = [s/b for s, b in zip(atoms_surface, atoms_bulk)]
    fig_ratio = go.Figure() 
    fig_ratio.add_trace(
        go.Scatter(
            x=sizes, 
            y=surface_to_bulk_ratio, 
            mode='lines+markers', 
            name='Surface/Bulk Ratio'
        )
    )
    fig_ratio.update_layout(
        title=f'Surface to Bulk Atom Ratio in {shape} Nanoparticles',
        xaxis_title='Particle Size (nm)',
        yaxis_title='Surface/Bulk Ratio'
    )
    st.plotly_chart(fig_ratio, use_container_width=True)
