"""
Smart Inventory Advisor - Streamlit Frontend Application
EOQ-Based Inventory Optimization Dashboard powered by Real Kaggle Supply Chain Data.
"""

import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

import eoq_model
import data_pipeline

# Page Configuration
st.set_page_config(
    page_title="Smart Inventory Advisor | EOQ Analytics Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Custom CSS Injection (Enterprise SaaS Visual Theme)
st.markdown("""
<style>
    /* Global Layout & Padding */
    .main .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2.5rem;
        max-width: 96%;
    }

    /* Executive Header Banner */
    .header-banner {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        border-radius: 12px;
        padding: 24px 30px;
        color: #FFFFFF;
        margin-bottom: 22px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.12);
    }
    
    .header-title {
        font-size: 2.15rem;
        font-weight: 800;
        margin: 0;
        color: #F8FAFC;
        letter-spacing: -0.02em;
    }
    
    .header-subtitle {
        font-size: 1.05rem;
        color: #94A3B8;
        margin-top: 5px;
        margin-bottom: 12px;
    }
    
    .status-badge {
        display: inline-flex;
        align-items: center;
        background: rgba(16, 185, 129, 0.15);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 3px 12px;
        border-radius: 16px;
        font-size: 0.82rem;
        font-weight: 600;
    }

    /* Data Source Info Card */
    .data-source-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #3B82F6;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 20px;
        font-size: 0.9rem;
        color: #334155;
    }

    /* Modern KPI Cards */
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 18px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.08);
    }
    
    .kpi-label {
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        color: #64748B;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    
    .kpi-value {
        font-size: 1.65rem;
        font-weight: 700;
        color: #0F172A;
        line-height: 1.2;
    }

    .kpi-sub {
        font-size: 0.8rem;
        color: #2563EB;
        font-weight: 500;
        margin-top: 4px;
    }

    /* Insights & Recommendation Containers */
    .insight-card {
        background: #F8FAFC;
        border-left: 4px solid #3B82F6;
        border-radius: 8px;
        padding: 18px;
        margin-bottom: 15px;
    }

    .recommendation-card {
        background: #F0FDF4;
        border-left: 4px solid #10B981;
        border-radius: 8px;
        padding: 18px;
        margin-bottom: 15px;
    }

    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------------------------
st.sidebar.markdown("## 📦 Smart Inventory Advisor")
st.sidebar.markdown("*EOQ-Based Inventory Optimization*")
st.sidebar.markdown("---")

nav_selection = st.sidebar.radio(
    "Navigation View",
    options=["📊 Dashboard Overview", "📈 Inventory Analysis", "🔍 Data Explorer"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📁 Data Source & CSV Upload")
uploaded_file = st.sidebar.file_uploader("Upload Inventory CSV (Kaggle or EOQ Format)", type=["csv"])

# Adjustable Carrying Rate Slider for Derived Holding Cost Calculation (H = i * C)
holding_rate = st.sidebar.slider(
    "Annual Carrying Rate (i)",
    min_value=0.10,
    max_value=0.40,
    value=0.20,
    step=0.05,
    help="Derived Holding Cost H = i * Unit Manufacturing Cost (Standard 20% carrying rate)"
)

# ------------------------------------------------------------------------------
# DATA LOADING & PIPELINE PROCESSING
# ------------------------------------------------------------------------------
data_source_description = "Kaggle — High-Dimensional Supply Chain Inventory Dataset"
raw_df = None
eoq_input_df = None

if uploaded_file is not None:
    try:
        raw_df = pd.read_csv(uploaded_file)
        data_source_description = f"Uploaded CSV Dataset: {uploaded_file.name}"
        eoq_input_df = data_pipeline.process_raw_dataset(raw_df, holding_rate=holding_rate)
    except Exception as e:
        st.sidebar.error(f"Upload Processing Error: {e}")
        st.error(f"Could not process uploaded file: {e}")
        st.stop()
else:
    try:
        raw_df, eoq_input_df = data_pipeline.load_and_prepare_data(holding_rate=holding_rate)
    except Exception as e:
        st.error(f"Error loading default dataset: {e}")
        st.stop()

# Compute EOQ Model Results
try:
    calc_df = eoq_model.calculate_eoq(eoq_input_df)
except ValueError as val_err:
    st.error(f"Validation Error: {val_err}")
    st.stop()
except Exception as err:
    st.error(f"EOQ Calculation Failure: {err}")
    st.stop()

# Product / SKU Dropdown Selector
sku_list = calc_df['Product'].tolist()
selected_sku = st.sidebar.selectbox("Select SKU / Product to Analyze", options=sku_list, index=0)
product_data = calc_df[calc_df['Product'] == selected_sku].iloc[0]

# Render Header Banner
st.markdown(f"""
<div class="header-banner">
    <div class="header-title">Smart Inventory Advisor</div>
    <div class="header-subtitle">EOQ-Based Inventory Optimization & Decision Support Dashboard</div>
    <div>
        <span class="status-badge">● Operational ({len(calc_df)} SKUs Processed)</span>
        <span style="margin-left: 15px; color: #94A3B8; font-size: 0.85rem;">Data Source: {data_source_description}</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# PAGE 1: DASHBOARD OVERVIEW
# ------------------------------------------------------------------------------
if nav_selection == "📊 Dashboard Overview":
    st.markdown("### 📊 Portfolio High-Level Summary")
    
    # Real Data Source Information Panel
    with st.expander("ℹ️ Data Source Details & Mapping Methodology", expanded=False):
        st.markdown(f"""
        <div class="data-source-card">
            <strong>Data Source:</strong> Kaggle — High-Dimensional Supply Chain Inventory Dataset<br>
            <strong>Raw Dataset Statistics:</strong> {len(raw_df)} records | {len(calc_df)} Unique SKUs | Multi-Category Operations (Haircare, Skincare, Cosmetics)<br>
            <strong>Field Mapping & Derivations:</strong>
            <ul>
                <li><code>Product</code> &larr; <code>SKU</code> + Category</li>
                <li><code>Annual_Demand</code> &larr; <code>Number of products sold</code></li>
                <li><code>Ordering_Cost</code> &larr; <code>Shipping costs</code></li>
                <li><code>Holding_Cost</code> &larr; <em>DERIVED:</em> <code>Manufacturing costs</code> &times; {holding_rate*100:.0f}% annual carrying cost rate (<em>H = i &times; C</em>)</li>
                <li><code>Lead_Time_Days</code> &larr; <code>Lead times</code></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Calculate Top Portfolio KPIs
    total_skus = len(calc_df)
    avg_eoq = calc_df['EOQ'].mean()
    total_portfolio_cost = calc_df['Total_Annual_Inventory_Cost'].sum()
    avg_product_cost = calc_df['Total_Annual_Inventory_Cost'].mean()
    high_cost_skus = calc_df[calc_df['Total_Annual_Inventory_Cost'] > avg_product_cost]
    
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Active SKUs</div>
            <div class="kpi-value">{total_skus}</div>
            <div class="kpi-sub">Portfolio Items</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Average EOQ</div>
            <div class="kpi-value">{avg_eoq:,.1f} <span style="font-size:1rem;">units</span></div>
            <div class="kpi-sub">Optimal Mean Lot Size</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Annual Cost</div>
            <div class="kpi-value">${total_portfolio_cost:,.2f}</div>
            <div class="kpi-sub">Combined Inventory Expense</div>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">High-Cost Focus Items</div>
            <div class="kpi-value" style="color:#EF4444;">{len(high_cost_skus)} <span style="font-size:1rem;">SKUs</span></div>
            <div class="kpi-sub">Cost Above Mean (${avg_product_cost:,.0f})</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Main Visual Analytics High On The Page
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown(f"#### 1️⃣ EOQ Cost Trade-Off Curve ({selected_sku})")
        tradeoff_df = eoq_model.calculate_cost_tradeoff(product_row=product_data)
        
        fig_tradeoff = go.Figure()
        fig_tradeoff.add_trace(go.Scatter(
            x=tradeoff_df['Order_Quantity'], y=tradeoff_df['Annual_Ordering_Cost'],
            mode='lines', name='Annual Ordering Cost', line=dict(color='#F59E0B', width=2, dash='dash')
        ))
        fig_tradeoff.add_trace(go.Scatter(
            x=tradeoff_df['Order_Quantity'], y=tradeoff_df['Annual_Holding_Cost'],
            mode='lines', name='Annual Holding Cost', line=dict(color='#10B981', width=2, dash='dash')
        ))
        fig_tradeoff.add_trace(go.Scatter(
            x=tradeoff_df['Order_Quantity'], y=tradeoff_df['Total_Annual_Inventory_Cost'],
            mode='lines', name='Total Annual Cost', line=dict(color='#2563EB', width=3)
        ))
        
        selected_eoq = float(product_data['EOQ'])
        fig_tradeoff.add_vline(
            x=selected_eoq, line_width=2, line_dash="dot", line_color="#EF4444",
            annotation_text=f"Optimal EOQ ({selected_eoq:,.1f})", annotation_position="top right"
        )
        fig_tradeoff.update_layout(
            template='plotly_white', height=380,
            xaxis_title="Order Quantity (Units)", yaxis_title="Cost ($)",
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_tradeoff, use_container_width=True)
        
    with col_chart2:
        st.markdown("#### 2️⃣ Total Annual Inventory Cost by SKU (Top 15)")
        top15_df = calc_df.sort_values(by='Total_Annual_Inventory_Cost', ascending=False).head(15)
        colors = ['#2563EB' if p == selected_sku else '#94A3B8' for p in top15_df['Product']]
        
        fig_bar = go.Figure(data=[
            go.Bar(
                x=top15_df['Product'], y=top15_df['Total_Annual_Inventory_Cost'],
                marker_color=colors,
                text=[f"${v:,.0f}" for v in top15_df['Total_Annual_Inventory_Cost']],
                textposition='auto'
            )
        ])
        fig_bar.update_layout(
            template='plotly_white', height=380,
            xaxis_title="Product SKU", yaxis_title="Total Annual Cost ($)",
            showlegend=False
        )
        st.plotly_chart(fig_bar, use_container_width=True)


# ------------------------------------------------------------------------------
# PAGE 2: INVENTORY ANALYSIS
# ------------------------------------------------------------------------------
elif nav_selection == "📈 Inventory Analysis":
    st.markdown(f"### 📈 Deep-Dive Inventory Analytics: **{selected_sku}**")
    
    # Selected SKU Metric Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Economic Order Quantity (EOQ)", f"{product_data['EOQ']:,.2f} units")
    with c2:
        st.metric("Order Frequency", f"{product_data['Number_of_Orders_Per_Year']:,.2f} / year")
    with c3:
        st.metric("Total Annual Inventory Cost", f"${product_data['Total_Annual_Inventory_Cost']:,.2f}")
    with c4:
        st.metric("Reorder Point (ROP)", f"{product_data['Reorder_Point']:,.2f} units")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    chart_c1, chart_c2 = st.columns(2)
    
    with chart_c1:
        st.markdown("#### 📐 Cost Trade-Off Curve Analysis")
        tradeoff_df = eoq_model.calculate_cost_tradeoff(product_row=product_data)
        
        fig_tradeoff = go.Figure()
        fig_tradeoff.add_trace(go.Scatter(
            x=tradeoff_df['Order_Quantity'], y=tradeoff_df['Annual_Ordering_Cost'],
            mode='lines', name='Annual Ordering Cost', line=dict(color='#F59E0B', width=2, dash='dash')
        ))
        fig_tradeoff.add_trace(go.Scatter(
            x=tradeoff_df['Order_Quantity'], y=tradeoff_df['Annual_Holding_Cost'],
            mode='lines', name='Annual Holding Cost', line=dict(color='#10B981', width=2, dash='dash')
        ))
        fig_tradeoff.add_trace(go.Scatter(
            x=tradeoff_df['Order_Quantity'], y=tradeoff_df['Total_Annual_Inventory_Cost'],
            mode='lines', name='Total Annual Cost', line=dict(color='#2563EB', width=3)
        ))
        
        selected_eoq = float(product_data['EOQ'])
        fig_tradeoff.add_vline(
            x=selected_eoq, line_width=2, line_dash="dot", line_color="#EF4444",
            annotation_text=f"EOQ = {selected_eoq:,.1f}", annotation_position="top right"
        )
        fig_tradeoff.update_layout(
            template='plotly_white', height=400,
            xaxis_title="Order Quantity (Units)", yaxis_title="Cost ($)",
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_tradeoff, use_container_width=True)
        
    with chart_c2:
        st.markdown("#### 📊 Portfolio SKU Cost Distribution")
        fig_hist = px.histogram(
            calc_df, x='Total_Annual_Inventory_Cost', nbins=20,
            labels={'Total_Annual_Inventory_Cost': 'Total Annual Cost ($)'},
            color_discrete_sequence=['#3B82F6'], template='plotly_white'
        )
        fig_hist.update_layout(height=400, yaxis_title="SKU Count", showlegend=False)
        st.plotly_chart(fig_hist, use_container_width=True)
        
    st.markdown("---")
    
    # Insights & Recommendations
    highest_row = calc_df.loc[calc_df['Total_Annual_Inventory_Cost'].idxmax()]
    lowest_row = calc_df.loc[calc_df['Total_Annual_Inventory_Cost'].idxmin()]
    
    ins1, ins2 = st.columns(2)
    with ins1:
        st.markdown("""
        <div class="insight-card">
            <h4 style="margin-top:0; color:#1E3A8A;">💡 Dynamic Business Insights</h4>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        - **Highest Cost SKU**: **{highest_row['Product']}** incurring **${highest_row['Total_Annual_Inventory_Cost']:,.2f}** per year.
        - **Lowest Cost SKU**: **{lowest_row['Product']}** incurring **${lowest_row['Total_Annual_Inventory_Cost']:,.2f}** per year.
        - **Selected Item ({selected_sku}) Breakdown**:
          - Recommended purchase order quantity: **{product_data['EOQ']:,.2f} units**.
          - Annual ordering frequency: **{product_data['Number_of_Orders_Per_Year']:,.2f} times/year** (every **{365/product_data['Number_of_Orders_Per_Year']:,.1f} days**).
          - Replenishment trigger threshold: **{product_data['Reorder_Point']:,.2f} units**.
        """)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with ins2:
        st.markdown("""
        <div class="recommendation-card">
            <h4 style="margin-top:0; color:#065F46;">🎯 Actionable Business Recommendation</h4>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        1. **Order Batch Size**: For **{selected_sku}**, order exactly **{product_data['EOQ']:,.2f} units** per replenishment cycle to minimize total cost.
        2. **Replenishment Timing**: Issue purchase orders when stock reaches **{product_data['Reorder_Point']:,.2f} units** to prevent stockouts during supplier lead time (**{product_data['Lead_Time_Days']} days**).
        3. **Inventory Prioritization**: Focus cost reduction efforts on **{highest_row['Product']}**, as it carries the largest inventory holding burden.
        """)
        st.markdown("</div>", unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# PAGE 3: DATA EXPLORER
# ------------------------------------------------------------------------------
elif nav_selection == "🔍 Data Explorer":
    st.markdown("### 🔍 Complete Inventory Calculations Explorer")
    
    col_search, col_filter = st.columns([2, 1])
    with col_search:
        search_query = st.text_input("🔍 Search SKU or Product Name...", "")
    with col_filter:
        sort_col = st.selectbox("Sort By Column", options=['Total_Annual_Inventory_Cost', 'EOQ', 'Annual_Demand', 'Reorder_Point'], index=0)
        
    filtered_df = calc_df.copy()
    if search_query:
        filtered_df = filtered_df[filtered_df['Product'].str.contains(search_query, case=False, na=False)]
        
    filtered_df = filtered_df.sort_values(by=sort_col, ascending=False)
    
    st.markdown(f"Displaying **{len(filtered_df)}** of **{len(calc_df)}** SKU records.")
    
    display_cols = [
        'Product', 'Annual_Demand', 'Ordering_Cost', 'Holding_Cost', 'Lead_Time_Days',
        'EOQ', 'Number_of_Orders_Per_Year', 'Annual_Ordering_Cost',
        'Annual_Holding_Cost', 'Total_Annual_Inventory_Cost', 'Daily_Demand', 'Reorder_Point'
    ]
    
    format_mapping = {
        'Annual_Demand': '{:,.0f}',
        'Ordering_Cost': '${:,.2f}',
        'Holding_Cost': '${:,.2f}',
        'Lead_Time_Days': '{:.0f}',
        'EOQ': '{:,.2f}',
        'Number_of_Orders_Per_Year': '{:,.2f}',
        'Annual_Ordering_Cost': '${:,.2f}',
        'Annual_Holding_Cost': '${:,.2f}',
        'Total_Annual_Inventory_Cost': '${:,.2f}',
        'Daily_Demand': '{:,.2f}',
        'Reorder_Point': '{:,.2f}'
    }
    
    st.dataframe(filtered_df[display_cols].style.format(format_mapping), use_container_width=True, height=450)
    
    # Download Button
    csv_bytes = calc_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Calculated Inventory Metrics (CSV)",
        data=csv_bytes,
        file_name="real_kaggle_eoq_inventory_metrics.csv",
        mime="text/csv"
    )
    
    st.markdown("---")
    st.markdown("#### 📐 Mathematical Model & Derivation Reference")
    f1, f2 = st.columns(2)
    with f1:
        st.latex(r"\text{EOQ} = \sqrt{\frac{2 \cdot D \cdot S}{H}}")
        st.latex(r"\text{Total Cost} = \left(\frac{D}{\text{EOQ}} \cdot S\right) + \left(\frac{\text{EOQ}}{2} \cdot H\right)")
    with f2:
        st.latex(r"H = i \times \text{Manufacturing Cost } (i=0.20)")
        st.latex(r"\text{Reorder Point (ROP)} = \left(\frac{D}{365}\right) \times \text{Lead Time Days}")
