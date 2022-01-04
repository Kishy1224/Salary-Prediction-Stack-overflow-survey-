from pickle import load
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def req_categories(categories,cutoff):
    cat_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            cat_map[categories.index[i]] = categories.index[i]
        else:
            cat_map[categories.index[i]] = 'Other'
    return cat_map
def clean_exp(exp):
    if exp == "More than 50 years":
        return 50
    if exp == "Less than 1 year":
        return 0.5
    return float(exp)

def clean_education(degree):
    if 'Bachelor’s degree' in degree:
        return 'Bachelor’s degree'
    if 'Master’s degree' in degree:
        return 'Master’s degree'
    if 'Professional degree' in degree or 'Other doctoral degree' in degree:
        return 'Post_grad'
    return 'Less than a Bachelors'
@st.cache
def load_data():
    df = pd.read_csv(r"C:\Users\HP\Documents\100\web_app\stack-overflow-developer-survey-2021\survey_results_public.csv")
    df = df[["Country","EdLevel","YearsCodePro","Employment","ConvertedCompYearly"]]
    df = df.rename({"ConvertedCompYearly":"Salary"},axis = 1)
    df = df[df['Salary'].notnull()]
    data = df.copy()
    data = data.dropna()
    data = data.loc[(data.Employment == "Employed full-time") + (data.Employment == "Independent contractor, freelancer, or self-employed")]
    Country_map = req_categories(data.Country.value_counts(),400)
    data["Country"] = data["Country"].map(Country_map)
    data = data[data["Salary"] <= 500000]
    data = data[data["Salary"] >= 10000]
    data = data[data["Country"] != 'Other']
    data['YearsCodePro'] = data["YearsCodePro"].apply(clean_exp)
    data["EdLevel"] = data["EdLevel"].apply(clean_education)
    
    return data

data = load_data()
def show_explore_page():

    st.title("Explore Software Engineer Salaries")

    st.write( """### Stack Overflow Developer Survey 2020""")

    dt = data["Country"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(dt, labels=dt.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.write("""#### Number of Data from different countries""")

    st.pyplot(fig1)
    
    st.write(
        """
    #### Mean Salary Based On Country
    """
    )

    dt = data.groupby("Country")["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(dt)

    st.write(
        """
    #### Mean Salary Based On Experience
    """
    )

    dt = data.groupby("YearsCodePro")["Salary"].mean().sort_values(ascending=True)
    st.line_chart(dt)

       


