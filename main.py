import streamlit as st
import pandas as pd

# App Title
st.title("💰 Expense Manager Dashboard")

# Sidebar Section for Accounts and Budget Summary
st.sidebar.header("Accounts Overview")

# Data for Budget and Off Budget accounts
accounts_data = {
    "Account": ["Ally Savings", "Bank of America", "Capital One Checking", "HSBC"],
    "Balance": [3418.71, 6367.06, 356.65, 536.79]
}
accounts_df = pd.DataFrame(accounts_data)

off_budget_data = {
    "Account": ["House Asset", "Mortgage", "Roth IRA", "Vanguard 401k"],
    "Balance": [338400.00, -312001.41, 2269.98, 3389.51]
}
off_budget_df = pd.DataFrame(off_budget_data)

# Total Balance Calculations
total_balance = accounts_df['Balance'].sum() + off_budget_df['Balance'].sum()
budget_balance = accounts_df['Balance'].sum()
off_budget_balance = off_budget_df['Balance'].sum()

# Display Account Overview
st.sidebar.markdown(f"### 💰 Total Account Balance: **${total_balance:,.2f}**")
st.sidebar.markdown(f"#### For Budget: **${budget_balance:,.2f}**")
st.sidebar.markdown(f"#### Off Budget: **${off_budget_balance:,.2f}**")

st.sidebar.subheader("💼 Budget Breakdown")
st.sidebar.write(accounts_df)

# Define Month Pairs
month_pairs = [("Aug", "Sep"), ("Oct", "Nov"), ("Dec", "Jan")]

# Initialize session state for selected month pair if not set
if "selected_pair" not in st.session_state:
    st.session_state.selected_pair = ("Aug", "Sep")  # Default selection

# Styling for Month Pagination with blue selected button
st.markdown("""
<style>
    .month-box {
        display: inline-block;
        padding: 15px;
        text-align: center;
        margin: 10px;
        width: 150px;
        background-color: #f8f9fa;
        font-weight: bold;
        color: #4b4b4b;
        border-radius: 5px;
        cursor: pointer;
    }
    .month-box:hover {
        background-color: #e0e0e0;
    }
    .month-box-selected {
        background-color: #007bff;  /* Blue background for the selected button */
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Function to create clickable divs as month buttons
def month_button(pair, selected_pair):
    if pair == selected_pair:
        button_style = "month-box month-box-selected"
    else:
        button_style = "month-box"
    
    button_html = f"""
    <div class="{button_style}" onclick="window.location.href='/?selected_pair={pair[0]}-{pair[1]}'">
        {pair[0]} - {pair[1]}
    </div>
    """
    st.markdown(button_html, unsafe_allow_html=True)

# Get URL parameters for selected pair
query_params = st.experimental_get_query_params()
if 'selected_pair' in query_params:
    selected_pair_str = query_params['selected_pair'][0]
    selected_pair = tuple(selected_pair_str.split('-'))
    st.session_state.selected_pair = selected_pair
else:
    selected_pair = st.session_state.selected_pair

# Display Month Pair Buttons
columns = st.columns(len(month_pairs))
for i, pair in enumerate(month_pairs):
    with columns[i]:
        month_button(pair, selected_pair)

# Function to get budget summary for a specific month
def get_budget_summary(month):
    if month == "Aug":
        return {
            "Available Funds": 3261.46, "Overspent Last Month": 0.00,
            "Budgeted": 0.00, "Next Month Funds": 0.00,
            "Balance": {
                "Food": 296.32, "Restaurants": 172.09, "Entertainment": 731.38, "Clothing": 53.85,
                "General": 6164.11, "Gift": 0.00, "Medical": 0.00, "Savings": 0.00
            }
        }
    elif month == "Sep":
        return {
            "Available Funds": 3261.46, "Overspent Last Month": 0.00,
            "Budgeted": 0.00, "Next Month Funds": 0.00,
            "Balance": {
                "Food": 400.00, "Restaurants": 250.00, "Entertainment": 500.00, "Clothing": 100.00,
                "General": 5000.00, "Gift": 50.00, "Medical": 200.00, "Savings": 300.00
            }
        }
    elif month == "Oct":
        return {
            "Available Funds": 3500.00, "Overspent Last Month": 200.00,
            "Budgeted": 0.00, "Next Month Funds": 100.00,
            "Balance": {
                "Food": 350.00, "Restaurants": 300.00, "Entertainment": 400.00, "Clothing": 150.00,
                "General": 6000.00, "Gift": 100.00, "Medical": 100.00, "Savings": 500.00
            }
        }
    elif month == "Nov":
        return {
            "Available Funds": 3700.00, "Overspent Last Month": 0.00,
            "Budgeted": 0.00, "Next Month Funds": 200.00,
            "Balance": {
                "Food": 300.00, "Restaurants": 200.00, "Entertainment": 450.00, "Clothing": 120.00,
                "General": 5500.00, "Gift": 80.00, "Medical": 150.00, "Savings": 400.00
            }
        }
    # Add similar summaries for "Dec", "Jan", and other months as needed

# Display Budget Summaries for Selected Month Pair
col1, col2 = st.columns(2)

# Get summaries for the selected pair of months
month1_summary = get_budget_summary(selected_pair[0])
month2_summary = get_budget_summary(selected_pair[1])

with col1:
    st.subheader(f"📊 {selected_pair[0]} Budget Summary")
    st.markdown(f"""
    - Available Funds: **${month1_summary['Available Funds']:,.2f}**
    - Overspent in Last Month: **${month1_summary['Overspent Last Month']:,.2f}**
    - Budgeted: **${month1_summary['Budgeted']:,.2f}**
    - For Next Month: **${month1_summary['Next Month Funds']:,.2f}**
    """)
    st.markdown(f"### To Budget: **${month1_summary['Available Funds']:,.2f}**")

with col2:
    st.subheader(f"📊 {selected_pair[1]} Budget Summary")
    st.markdown(f"""
    - Available Funds: **${month2_summary['Available Funds']:,.2f}**
    - Overspent in Last Month: **${month2_summary['Overspent Last Month']:,.2f}**
    - Budgeted: **${month2_summary['Budgeted']:,.2f}**
    - For Next Month: **${month2_summary['Next Month Funds']:,.2f}**
    """)
    st.markdown(f"### To Budget: **${month2_summary['Available Funds']:,.2f}**")

col1, col2 = st.columns(2)
with col1:
    # Expense Categories Section for the first selected month
    st.subheader(f"💸 Expense Categories for {selected_pair[0]}")
    expense_data1 = {
        "Category": ["Food", "Restaurants", "Entertainment", "Clothing", "General", "Gift", "Medical", "Savings"],
        "Budgeted": [0, 0, 0, 0, 0, 0, 0, 0],
        "Spent": [0, 0, 0, 0, 0, 0, 0, 0],
        "Balance": list(month1_summary["Balance"].values())
    }
    expense_df1 = pd.DataFrame(expense_data1)
    st.dataframe(expense_df1)

with col2:
    # Expense Categories Section for the second selected month
    st.subheader(f"💸 Expense Categories for {selected_pair[1]}")
    expense_data2 = {
        "Category": ["Food", "Restaurants", "Entertainment", "Clothing", "General", "Gift", "Medical", "Savings"],
        "Budgeted": [0, 0, 0, 0, 0, 0, 0, 0],
        "Spent": [0, 0, 0, 0, 0, 0, 0, 0],
        "Balance": list(month2_summary["Balance"].values())
    }
    expense_df2 = pd.DataFrame(expense_data2)
    st.dataframe(expense_df2)

# Footer with Sync/Online Status Simulation
st.markdown('<p style="text-align:right;">🔄 Sync | Server Online</p>', unsafe_allow_html=True)
