import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import image
import os

st.title("DineScore")
st.subheader("The primary objective is to gain insights into popular restaurants and determine their ratings.")
st.write("Restaurant ratings are widely used to evaluate eateries by individuals. \
         The rating of a restaurant is influenced by factors such as reviews, location, average cost for two, \
         votes, cuisines, and restaurant type.")


 # Used to get the directory path of the current Python script file that is being executed.
file_dir=os.path.dirname(os.path.abspath(__file__))

# combines the folder path from the previous step with the folder name "resources" to create a new path.
dir_of_interest = os.path.join(file_dir, "resources")

# combines the path from the previous step with the image file name "image.jpg" to create a new path. 
image_path= os.path.join(dir_of_interest, "image.jpg")

# reads the image file located at the path obtained in the previous step and stores it in the variable img.
img = image.imread(image_path)

# displays the image stored in the img variable.
st.image(img)
