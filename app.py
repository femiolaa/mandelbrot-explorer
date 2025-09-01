# app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import time

def mandelbrot(c, max_iter):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z*z + c
        n += 1
    if n == max_iter:
        return max_iter
    return n + 1 - np.log(np.log2(abs(z)))

def generate_mandelbrot(width, height, x_min, x_max, y_min, y_max, max_iter):
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    C = np.tile(x, (height, 1)).T + 1j * np.tile(y, (width, 1))
    mandelbrot_set = np.fromfunction(lambda i, j: mandelbrot(C[i, j], max_iter), (width, height))
    return mandelbrot_set

st.title("Interactive Mandelbrot Set Explorer")
st.sidebar.header("Parameters")

width = st.sidebar.slider("Image Width", 200, 1000, 600)
height = st.sidebar.slider("Image Height", 200, 1000, 600)
max_iter = st.sidebar.slider("Max Iterations", 50, 500, 100)

zoom = st.sidebar.slider("Zoom Level", 0.1, 10.0, 1.0)
center_x = st.sidebar.slider("Center X", -2.5, 1.0, -0.5)
center_y = st.sidebar.slider("Center Y", -1.5, 1.5, 0.0)

half_width = 1.5 / zoom
half_height = 1.5 / zoom
x_min = center_x - half_width
x_max = center_x + half_width
y_min = center_y - half_height
y_max = center_y + half_height

if st.sidebar.button("Generate Mandelbrot Set"):
    with st.spinner("Computing... This may take a moment for high resolutions."):
        start_time = time.time()
        mandelbrot_set = generate_mandelbrot(width, height, x_min, x_max, y_min, y_max, max_iter)
        end_time = time.time()
        
        fig, ax = plt.subplots(figsize=(10, 10))
        cmap = ListedColormap(['#000000'] + plt.cm.viridis(np.linspace(0, 1, max_iter)).tolist())
        ax.imshow(mandelbrot_set.T, origin='lower', cmap=cmap, extent=[x_min, x_max, y_min, y_max])
        ax.axis('off')
        
        st.pyplot(fig)
        st.write(f"Computation time: {end_time - start_time:.2f} seconds")
    
st.markdown("""
### About this App
This Streamlit app generates and visualizes the Mandelbrot set, a famous fractal in complex mathematics. 
The Mandelbrot set is defined as the set of complex numbers c for which the function f(z) = z² + c does not diverge when iterated from z=0.
Adjust the parameters in the sidebar to explore different regions and iteration depths.
""")
