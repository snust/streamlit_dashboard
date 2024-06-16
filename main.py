import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

URL = "https://raw.githubusercontent.com/marcopeix/MachineLearningModelDeploymentwithStreamlit/master/12_dashboard_capstone/data/quarterly_canada_population.csv"

df = pd.read_csv(URL, dtype={'Quarter': str, 
                            'Canada': np.int32,
                            'Newfoundland and Labrador': np.int32,
                            'Prince Edward Island': np.int32,
                            'Nova Scotia': np.int32,
                            'New Brunswick': np.int32,
                            'Quebec': np.int32,
                            'Ontario': np.int32,
                            'Manitoba': np.int32,
                            'Saskatchewan': np.int32,
                            'Alberta': np.int32,
                            'British Columbia': np.int32,
                            'Yukon': np.int32,
                            'Northwest Territories': np.int32,
                            'Nunavut': np.int32})

# Header
st.title("Population of Canada")
st.markdown("Source table can be found [here](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000901)")

# Expander
with st.expander("See full data table"):
    st.dataframe(df)

# Containers
with st.form("population-form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.text("Choose a starting date")
        startQuarter = st.selectbox("Quarter",
                     ("Q1", "Q2", "Q3", "Q4"), key="startSelectBox"
                     )
        startYear = st.slider("Year", min_value=1991, max_value=2023, key="startSlider")

    with col2:
        st.text("Choose an end date")
        endQuarter = st.selectbox("Quarter",
                     ("Q1", "Q2", "Q3", "Q4"), key="endSelectBox"
                     )
        endYear = st.slider("Year", min_value=1991, max_value=2023, key="endSlider")

    with col3:
        st.text("Choose a location")
        location = st.selectbox("Choose a location",
                     options=df.columns[1:], key="locationSelectBox"
                     )
    
    st.form_submit_button("Analyze", type="primary")
        
    startDate = f"{startQuarter} {startYear}"
    endDate = f"{endQuarter} {endYear}"

def format_date_for_comparison(date):
    if date[1] == 2:
        return float(date[2:]) + 0.25
    elif date[1] == 3:
        return float(date[2:]) + 0.50
    elif date[1] == 4:
        return float(date[2:]) + 0.75
    else:
        return float(date[2:])

def end_before_start(start_date, end_date):
    num_start_date = format_date_for_comparison(start_date)
    num_end_date = format_date_for_comparison(end_date)

    if num_start_date > num_end_date:
        return True
    else:
        return False

def display_dashboard(start_date, end_date, target):
    tab1, tab2 = st.tabs(["Population change", "Compare"])

    with tab1:
        st.text(f"Population change from {startDate} to {endDate}")
        
        col1, col2 = st.columns(2)

        with col1:
            original = df.loc[df['Quarter'] == startDate, location].item()
            final = df.loc[df['Quarter'] == endDate, location].item()

            perDiff = round((final - original) / original * 100, 2)
            delta = f"{perDiff}%"
            st.metric(startDate, value=original)
            st.metric(endDate, value=final, delta=delta)

        with col2:
            start_idx = df.loc[df['Quarter'] == startDate].index.item()
            end_idx = df.loc[df['Quarter'] == endDate].index.item()
            filtered_df = df.iloc[start_idx: end_idx+1]

            fig, ax = plt.subplots()
            ax.plot(filtered_df['Quarter'], filtered_df[location])
            ax.set_xlabel('Time')
            ax.set_ylabel('Population')
            ax.set_xticks([filtered_df['Quarter'].iloc[0], filtered_df['Quarter'].iloc[-1]])
            fig.autofmt_xdate()
            st.pyplot(fig)

    with tab2:
        st.text("Compare with other locations")

        allLocations = st.multiselect("Choose other locations",
                    options=filtered_df.columns[1:], default = location)
        
        fig, ax = plt.subplots()
        for each in allLocations:
            ax.plot(filtered_df['Quarter'], filtered_df[each])
        ax.set_xlabel('Time')
        ax.set_ylabel('Population')
        ax.set_xticks([filtered_df['Quarter'].iloc[0], filtered_df['Quarter'].iloc[-1]])
        fig.autofmt_xdate()
        st.pyplot(fig)

if startDate not in df['Quarter'].tolist() or endDate not in df['Quarter'].tolist():
    st.error("No data available. Check your quarter and year selection")
elif end_before_start(startDate, endDate):
    st.error("Dates don't work. Start date must come before end date.")
else:
    display_dashboard(startDate, endDate, location)