import streamlit as st
import pandas as pd

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
def profit_graph_data(cost, units):
        costs = []
        revenues = []
        profits = []
        for num_units in range(1,units):
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

            costs.append(total_cost)
            revenues.append(revenue)
            profits.append(profit)
        df = pd.DataFrame()
        df["Num Units"] = [i for i in range(1,units)]
        df["Cost"] = costs
        df["Revenue"] = revenues
        df['Profit'] = profits
        return df

with tab1:
    df = profit_graph_data(cost, units)
    st.line_chart(df, x='Num Units',y = ['Cost', 'Revenue'],color=["#FF0000", "#00dd00"], )
    st.caption("Breakeven = {} units".format([z for x,y,z in zip(df.Revenue, df.Cost, df["Num Units"]) if x>y ][0]))


with tab2:
    st.line_chart(df, x = 'Num Units', y = 'Profit')