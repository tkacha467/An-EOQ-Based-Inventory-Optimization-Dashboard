import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from eoq_model import calculate_eoq, validate_input_dataframe, calculate_cost_tradeoff

st.set_page_config(page_title="Smart Inventory Advisor", page_icon="📦", layout="wide")
st.title("📦 Smart Inventory Advisor")
st.caption("EOQ-Based Inventory Optimization Dashboard")

@st.cache_data
def load_sample():
    return pd.read_csv("data/inventory_data.csv")

uploaded = st.sidebar.file_uploader("Upload inventory CSV", type=["csv"])
try:
    raw = pd.read_csv(uploaded) if uploaded else load_sample()
    results = calculate_eoq(raw)
except Exception as e:
    st.error(f"Invalid dataset: {e}")
    st.stop()

products = results["Product"].astype(str).tolist()
selected = st.sidebar.selectbox("Select Product", products)
row = results[results["Product"].astype(str) == selected].iloc[0]

c1, c2, c3, c4 = st.columns(4)
c1.metric("EOQ", f"{row.EOQ:,.1f} units")
c2.metric("Orders / Year", f"{row.Number_of_Orders_Per_Year:,.2f}")
c3.metric("Total Annual Cost", f"{row.Total_Annual_Inventory_Cost:,.2f}")
c4.metric("Reorder Point", f"{row.Reorder_Point:,.1f} units")

st.subheader("Inventory Optimization Results")
display_cols = ["Product", "Annual_Demand", "Ordering_Cost", "Holding_Cost", "Lead_Time_Days", "EOQ", "Number_of_Orders_Per_Year", "Annual_Ordering_Cost", "Annual_Holding_Cost", "Total_Annual_Inventory_Cost", "Reorder_Point"]
st.dataframe(results[display_cols].round(2), use_container_width=True, hide_index=True)

st.subheader(f"Cost Trade-off — {selected}")
trade = calculate_cost_tradeoff(row)
fig = go.Figure()
for col, name in [("Ordering_Cost", "Ordering Cost"), ("Holding_Cost", "Holding Cost"), ("Total_Cost", "Total Cost")]:
    fig.add_trace(go.Scatter(x=trade.Order_Quantity, y=trade[col], mode="lines", name=name))
fig.add_vline(x=float(row.EOQ), line_dash="dash", annotation_text=f"EOQ = {row.EOQ:.1f}")
fig.update_layout(xaxis_title="Order Quantity", yaxis_title="Annual Cost", hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Total Annual Inventory Cost by Product")
bar = px.bar(results, x="Product", y="Total_Annual_Inventory_Cost", labels={"Total_Annual_Inventory_Cost":"Total Annual Cost"})
st.plotly_chart(bar, use_container_width=True)

st.subheader("💡 Business Insights")
high_cost = results.loc[results["Total_Annual_Inventory_Cost"].idxmax(), "Product"]
st.write(f"• **{high_cost}** has the highest annual inventory cost in the dataset.")
st.write(f"• For **{selected}**, the economical order quantity is approximately **{row.EOQ:.1f} units**.")
st.write(f"• Reorder when inventory reaches approximately **{row.Reorder_Point:.1f} units**, based on annual demand and lead time.")
st.write("• Using EOQ balances ordering and holding costs to reduce avoidable inventory expense.")
