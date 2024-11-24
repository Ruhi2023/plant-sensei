import streamlit as st 
import time
import numpy as np
import pandas as pd


background_image = "https://images7.alphacoders.com/522/thumbbig-522733.webp"  # Replace with the actual path to your image

# Add the background image to the page
st.markdown(
    f"""
    <style>
        .stApp {{
            background-image: url('{background_image}');
            background-size: cover;
            background-position: top center;
            height: 100vh;
            background-color: #f2f1f1;
        }}
    </style>
    """,
    unsafe_allow_html=True
)



st.session_state["i ran"] = False

intro_para = """
***Discover the Green World: A World of Wonder***
Plants are more than just pretty faces. 
They are the foundation of life on Earth, providing us with oxygen, food, and medicine. 
Learning about plants can be a fascinating journey that opens up a world of wonder and discovery. 
From the towering trees of the rainforest to the tiny wildflowers that bloom in our gardens, plants offer endless opportunities for exploration and appreciation. 
So, let's embark on a botanical adventure together and uncover the secrets of the plant kingdom!
"""


def stream_data():
    for word in intro_para.split(" "):
        yield word + " "
        time.sleep(0.02)
st.title("Plant Expert")
c2,c3,c4 =st.columns([1,3,1])
goto_inf =c2.button(":green[:material/description: Get Plant Info]")

goto_dis = c4.button(":blue[:material/medication_liquid: Get Plant Disease]")

if goto_inf:
    st.switch_page("pages/New_plant_iden.py")
if goto_dis:
    st.switch_page("pages/New_plant_disease.py")
if st.session_state["i ran"] == False:
    c3.write_stream(stream_data)
    st.session_state["i ran"] = True