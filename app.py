import streamlit as st
import pandas as pd
import numpy as np
st.title('Adomly Introduction')

st.header('Overview')
st.text('')

"""
We want some numbers to have break even points, projected profits, market cap etc.
"""
# cost_per_unit = st.number_input("Cost/Unit", value = 50)



accounting_df = pd.read_csv('Accounting.csv')
with st.expander("Cost Matrix"):
    accounting_de = st.data_editor(accounting_df)
    accounting_de.set_index("Item", inplace= True)
    accounting_dict = accounting_de.to_dict()
    cost = accounting_dict["Cost"]
units = st.number_input('Units sold' ,2000)
tab1,tab2 = st.tabs(["Cost", "Profit"])
with st.expander('Breakdown of cost'):
    num_units = st.number_input('Number of Units Sold', value = 100)
    # cost
    fixed_cost = cost["Tooling"] + cost["Prototype"] + cost["Design"]
    unit_cost = cost["Unit Cost"]*num_units
    shopify_fee = cost["Shopify fee"]*num_units
    transaction_fee = cost["Selling Price"]*cost["Online Transaction Fee"]*num_units
    shipping = cost["Shipping"]*num_units
    returns = cost["Returns"]*cost["Selling Price"]*num_units
    variable_cost = unit_cost+shopify_fee+transaction_fee+shipping+returns
    total_cost = fixed_cost+variable_cost
    revenue = cost["Selling Price"]*num_units
    profit = revenue-variable_cost-fixed_cost
    st.text("""Fixed costs from Tooling, Design, Prototype = 
        -${}0""".format(fixed_cost))
    st.text("""Variable Costs Unit Cost + Shopify Fees + Transaction Fees + Shipping Costs + Returns =
        -${}0""".format(variable_cost))
    st.text("""For a grand total of 
        -${}0""".format(total_cost))
    st.text("""Revenue on the other hand will be Number of units * Selling Price = 
        +${}""".format(revenue))
    st.metric("Profit", round(profit))
def profit_graph_data(cost, units, step=100):
    units_array = np.arange(1, units, step)

    fixed_cost = cost["Tooling"] + cost["Prototype"] + cost["Design"]
    unit_cost = cost["Unit Cost"] * units_array
    shopify_fee = cost["Shopify fee"] * units_array
    transaction_fee = cost["Selling Price"] * cost["Online Transaction Fee"] * units_array
    shipping = cost["Shipping"] * units_array
    returns = cost["Returns"] * cost["Selling Price"] * units_array

    variable_cost = unit_cost + shopify_fee + transaction_fee + shipping + returns
    total_cost = fixed_cost + variable_cost
    revenue = cost["Selling Price"] * units_array
    profit = revenue - variable_cost - fixed_cost

    df = pd.DataFrame({
        "Num Units": units_array,
        "Cost": total_cost,
        "Revenue": revenue,
        "Profit": profit
    })

    return df

def find_breakeven(df):
    # Find the index where revenue exceeds cost
    breakeven_index = np.where(df["Revenue"] > df["Cost"])[0]
    
    if breakeven_index.size > 0:
        breakeven_units = df["Num Units"].iloc[breakeven_index[0]]
    else:
        breakeven_units = None
    
    return breakeven_units

with tab1:
    df = profit_graph_data(cost, units)
    st.line_chart(df, x='Num Units',y = ['Cost', 'Revenue'],color=["#FF0000", "#00dd00"], )
    st.caption("Breakeven = {} units".format(find_breakeven(df)))


with tab2:
    st.line_chart(df, x = 'Num Units', y = 'Profit')