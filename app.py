import streamlit as st


nav = st.navigation({
    "Home": [st.Page("pages/Expert_Home.py",title = "Home",icon="🏠")],
    "Plant": [st.Page("pages/New_plant_iden.py",icon="🌱"),
              st.Page("pages/New_plant_disease.py",icon="🩺")]
})
nav.run()