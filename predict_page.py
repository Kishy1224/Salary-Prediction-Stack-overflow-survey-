import pickle

import numpy as np
import streamlit as st


def load_model():
    with open('saved_steps.pkl','rb') as file:
        data = pickle.load(file)
    return data

final_data = load_model()

regressor = final_data["model"]
le_country = final_data["le_country"]
le_education = final_data["le_education"]

def show_predict_page():
    st.title("Salary prediction")

    st.write("""### we need some info to predict salary""")

    countries = (
        "India",
        "Germany",
        "United Kingdom of Great Britain and Northern Ireland",
        "Canada",
        "Brazil",
        "France",
        "Spain",
        "Australia",
        "Netherlands",
        "Poland",
        "Italy",
        "Russian Federation",
        "Sweden",
    )

    education = (
        "Less than a Bachelors",
        "Bachelor’s degree",
        "Master’s degree",
        "Post_grad",
    )

    country = st.selectbox("Country", countries)
    education = st.selectbox("Education Level", education)

    expericence = st.slider("Years of Experience", 0, 50, 3)

    ok = st.button("Calculate Salary")
    if ok:

        p_array = np.array([[country,education,expericence]])
        p_array[:,0] = le_country.fit_transform(p_array[:,0])
        p_array[:,1] = le_education.fit_transform(p_array[:,1])
        p_array = p_array.astype(float)

        salary = regressor.predict(p_array)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")
