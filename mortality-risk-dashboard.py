import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# load life tables
@st.cache_data
def load_life_tables():
    male_df = pd.read_csv('life_tables/male_lt.csv', skiprows=1)
    female_df = pd.read_csv('life_tables/female_lt.csv', skiprows=1)

    # Convert all columns to numbers, force bad values to NaN
    male_df = male_df.apply(pd.to_numeric, errors='coerce')
    female_df = female_df.apply(pd.to_numeric, errors='coerce')

    return male_df, female_df


male_table, female_table = load_life_tables()

# Title and description
st.title('Mortality Risk Dashboard')
st.write('Explore survival probabilities, life expectancy, and annuity values based on age and gender.')

# About section
with st.expander("ℹ️ About this app"):
    st.write("""
    This Mortality Risk Dashboard allows users to explore survival probabilities, 
    estimated life expectancy, and annuity values based on gender and age.
    
    **Features:**
    - Choose gender and age
    - Adjust discount rate dynamically
    - View survival curve
    - See estimated life expectancy and annuity value

    **Data source:**  
    Office for National Statistics (ONS) UK Life Tables.
    """)




# Sidebar for user inputs: Gender, Age, discount rate etc.
st.sidebar.header("User Input Features")
gender = st.sidebar.selectbox('Select Gender', options=['Male', 'Female'])
age = st.sidebar.slider('Select Age', min_value=0, max_value=100, value=30)
discount_rate = st.sidebar.slider('Select Discount Rate (%)', min_value=0.5, max_value=5.0, value=2.0, step=0.1) / 100


# Select the correct table based on user input
if gender == 'Male':
    selected_table = male_table.copy()
else:
    selected_table = female_table.copy()

filtered_table = selected_table[selected_table['age'] >= age].copy()

# Calculations:

#    Survival probabilities
filtered_table['Survival_Probability'] = (1 - filtered_table['qx']).cumprod()

#    Life expectancy
current_life_expectancy = filtered_table.iloc[0]['ex']

#    Annuity value
annuity_value = (1 - (1 + discount_rate) ** -current_life_expectancy) / discount_rate

# Display:
#    Survival curve (line plot)
fig, ax = plt.subplots(figsize=(8, 5))  # Bigger figure
ax.plot(filtered_table['age'], filtered_table['Survival_Probability'], linewidth=2)
ax.set_xlabel('Age')
ax.set_ylabel('Probability of Survival')
ax.set_title(f'Survival Curve: {gender} aged {age}', fontsize=14)
ax.grid(True, linestyle='--', alpha=0.7)
st.pyplot(fig)

st.subheader('Results')
col1, col2 = st.columns(2)

#    Estimated life expectancy
with col1:
    st.metric(
        label=f"**Estimated Life Expectancy:**",
        value=f"{current_life_expectancy:.1f} years"
        )

#    Estimated annuity value
with col2:
    st.metric(
        label=f"Annuity Value (at {discount_rate*100:.1f}% discount)",
        value=f"{annuity_value:.2f} x",
        help="Times the annual payment"
    )


st.markdown("""---""")

st.markdown(
    "<h6 style='text-align: center;'>Created by Danny Nufer</h6>",
    unsafe_allow_html=True
)




