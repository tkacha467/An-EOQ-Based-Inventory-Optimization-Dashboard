"""
Smart Inventory Advisor - Streamlit Frontend Application
EOQ-Based Inventory Optimization Dashboard inspired by CNN-ECO Case Study UI Theme.
Presenter: Tushar Pankajbhai Kacha | MSc Data Science
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

# Inject Fonts, FontAwesome Icons, and Reference UI CSS System
st.markdown("""
<!-- Google Fonts & Font Awesome Icons -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<style>
    /* CSS Variables matching reference UI */
    :root {
        --bg-primary: #ffffff;
        --bg-secondary: #f8fafc;
        --bg-card: #ffffff;
        --bg-card-hover: #f1f5f9;
        --border-color: #e2e8f0;
        --border-glow: rgba(16, 185, 129, 0.4);
        
        --accent-emerald: #059669;
        --accent-emerald-light: #ecfdf5;
        --accent-emerald-glow: rgba(5, 150, 105, 0.25);
        --accent-cyan: #0284c7;
        --accent-indigo: #4f46e5;
        --accent-amber: #d97706;
        --accent-rose: #e11d48;
        
        --text-primary: #0f172a;
        --text-secondary: #475569;
        --text-muted: #64748b;
        
        --font-main: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        --font-code: 'JetBrains Mono', monospace;
        
        --transition-smooth: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        --radius-sm: 6px;
        --radius-md: 12px;
        --radius-lg: 20px;
        --shadow-soft: 0 4px 20px rgba(0, 0, 0, 0.06);
        --shadow-glass: 0 10px 30px rgba(0, 0, 0, 0.08);
    }

    /* Global Override */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2.5rem;
        max-width: 96%;
        font-family: var(--font-main);
    }

    /* Top Navigation Banner */
    .top-navbar {
        background: rgba(255, 255, 255, 0.95);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        padding: 1rem 1.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow-soft);
    }

    .nav-brand {
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }

    .logo-badge {
        background: linear-gradient(135deg, #059669, #10b981);
        color: #ffffff;
        font-weight: 900;
        font-size: 0.85rem;
        padding: 0.35rem 0.65rem;
        border-radius: var(--radius-sm);
        box-shadow: 0 2px 8px rgba(5, 150, 105, 0.3);
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
    }

    .brand-title {
        font-size: 1.15rem;
        font-weight: 800;
        letter-spacing: -0.01em;
        color: var(--text-primary);
        line-height: 1.2;
    }

    .brand-sub {
        font-size: 0.78rem;
        color: var(--text-secondary);
        line-height: 1.2;
    }

    /* Meta Pill Container */
    .meta-pill-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
        margin-bottom: 1.2rem;
    }

    .meta-pill {
        background: #f1f5f9;
        border: 1px solid var(--border-color);
        color: var(--text-secondary);
        font-size: 0.78rem;
        font-weight: 600;
        padding: 0.3rem 0.75rem;
        border-radius: 20px;
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
    }

    .meta-pill.highlight {
        background: var(--accent-emerald-light);
        border-color: rgba(5, 150, 105, 0.3);
        color: var(--accent-emerald);
    }

    /* Gradient Typography */
    .hero-title {
        font-size: 2.2rem;
        font-weight: 900;
        line-height: 1.2;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
        color: var(--text-primary);
    }

    .gradient-text-eco {
        background: linear-gradient(135deg, #059669 0%, #10b981 50%, #047857 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        font-size: 0.95rem;
        color: var(--text-secondary);
        margin-bottom: 1.2rem;
        max-width: 900px;
    }

    /* Category Badges */
    .category-badges {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 1.5rem;
        flex-wrap: wrap;
    }

    .cat-badge {
        font-size: 0.75rem;
        font-weight: 700;
        padding: 0.3rem 0.7rem;
        border-radius: 6px;
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
    }

    .cat-haircare { background: #dbeafe; color: #1e40af; }
    .cat-skincare { background: #dcfce7; color: #166534; }
    .cat-cosmetics { background: #fce7f3; color: #9d174d; }

    /* Glassmorphism KPI Card */
    .glass-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        padding: 1.25rem;
        box-shadow: var(--shadow-soft);
        transition: var(--transition-smooth);
        margin-bottom: 1rem;
    }

    .glass-card:hover {
        transform: translateY(-3px);
        border-color: var(--border-glow);
        box-shadow: var(--shadow-glass);
    }

    .glass-card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.5rem;
    }

    .glass-icon {
        font-size: 1.5rem;
    }

    .glass-label {
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        color: var(--text-muted);
        letter-spacing: 0.05em;
    }

    .glass-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: var(--text-primary);
        line-height: 1.1;
    }

    .glass-sub {
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 0.35rem;
    }

    /* Insight & Action Boxes */
    .glass-insight {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-left: 4px solid var(--accent-cyan);
        border-radius: var(--radius-md);
        padding: 1.25rem;
        margin-bottom: 1rem;
    }

    .glass-recommendation {
        background: #ecfdf5;
        border: 1px solid #a7f3d0;
        border-left: 4px solid var(--accent-emerald);
        border-radius: var(--radius-md);
        padding: 1.25rem;
        margin-bottom: 1rem;
    }

    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# SIDEBAR NAVIGATION & DATA PIPELINE
# ------------------------------------------------------------------------------
st.sidebar.markdown("## <i class='fa-solid fa-boxes-packing' style='color:#059669;'></i> CNN-EOQ ADVISOR", unsafe_allow_html=True)
st.sidebar.markdown("*Supply Chain Inventory Optimization*")
st.sidebar.markdown("---")

nav_selection = st.sidebar.radio(
    "Navigation View",
    options=["🏠 Executive Overview", "📈 Inventory Analytics", "🔍 Data Explorer"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("### <i class='fa-solid fa-sliders'></i> Model Settings", unsafe_allow_html=True)

holding_rate = st.sidebar.slider(
    "Annual Carrying Rate (i)",
    min_value=0.10,
    max_value=0.40,
    value=0.20,
    step=0.05,
    help="Derived Holding Cost H = i * Unit Manufacturing Cost (Standard 20% carrying rate)"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### <i class='fa-solid fa-file-csv'></i> Custom Dataset Upload", unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])

# Data Processing
data_source_name = "Kaggle High-Dimensional Supply Chain Dataset"
raw_df = None
eoq_input_df = None

if uploaded_file is not None:
    try:
        raw_df = pd.read_csv(uploaded_file)
        data_source_name = f"Uploaded File: {uploaded_file.name}"
        eoq_input_df = data_pipeline.process_raw_dataset(raw_df, holding_rate=holding_rate)
    except Exception as e:
        st.sidebar.error(f"File Processing Error: {e}")
        st.error(f"Error processing uploaded dataset: {e}")
        st.stop()
else:
    try:
        raw_df, eoq_input_df = data_pipeline.load_and_prepare_data(holding_rate=holding_rate)
    except Exception as e:
        st.error(f"Failed to load dataset: {e}")
        st.stop()

# Compute EOQ Model Results
try:
    calc_df = eoq_model.calculate_eoq(eoq_input_df)
except Exception as err:
    st.error(f"EOQ Model Error: {err}")
    st.stop()

# SKU Dropdown Selector in Sidebar
sku_list = calc_df['Product'].tolist()
selected_sku = st.sidebar.selectbox("Select SKU for Deep-Dive", options=sku_list, index=0)
product_data = calc_df[calc_df['Product'] == selected_sku].iloc[0]

# ------------------------------------------------------------------------------
# TOP NAVBAR
# ------------------------------------------------------------------------------
st.markdown(f"""
<div class="top-navbar">
    <div class="nav-brand">
        <span class="logo-badge"><i class="fa-solid fa-truck-ramp-box"></i> EOQ-SMART</span>
        <div>
            <div class="brand-title">Smart Inventory Advisor & Decision Support</div>
            <div class="brand-sub">Presenter: Tushar Pankajbhai Kacha (ID: 92500567015) | MSc Data Science</div>
        </div>
    </div>
    <div style="display:flex; align-items:center; gap: 0.8rem;">
        <span class="meta-pill highlight"><i class="fa-solid fa-circle-check"></i> System Operational</span>
        <span class="meta-pill"><i class="fa-solid fa-database"></i> {len(calc_df)} Real SKUs Loaded</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Hero Header & Meta Pills
st.markdown(f"""
<div class="meta-pill-container">
    <span class="meta-pill highlight"><i class="fa-solid fa-user-graduate"></i> Presenter: Tushar Pankajbhai Kacha</span>
    <span class="meta-pill"><i class="fa-solid fa-id-card"></i> Student ID: 92500567015</span>
    <span class="meta-pill"><i class="fa-solid fa-brain"></i> Model: Economic Order Quantity (EOQ) + ROP</span>
    <span class="meta-pill"><i class="fa-solid fa-bullseye"></i> Target: Cost Minimization & Replenishment</span>
</div>

<h1 class="hero-title">
    Automated <span class="gradient-text-eco">Inventory Optimization</span><br>
    Powered by EOQ Engine
</h1>
<p class="hero-subtitle">
    An intelligent operations management decision framework balancing purchase ordering costs against inventory holding carrying expenses. Leveraging real-world Kaggle supply chain data to optimize lot sizes and prevent lead-time stockouts.
</p>

<div class="category-badges">
    <span class="cat-badge cat-haircare"><i class="fa-solid fa-pump-soap"></i> Haircare Portfolio</span>
    <span class="cat-badge cat-skincare"><i class="fa-solid fa-hand-holding-droplet"></i> Skincare Portfolio</span>
    <span class="cat-badge cat-cosmetics"><i class="fa-solid fa-wand-magic-sparkles"></i> Cosmetics Portfolio</span>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# VIEW 1: EXECUTIVE OVERVIEW
# ==============================================================================
if nav_selection == "🏠 Executive Overview":
    st.markdown("### <i class='fa-solid fa-chart-line' style='color:#059669;'></i> Executive Portfolio Summary", unsafe_allow_html=True)
    
    # Dataset Details Card
    with st.expander("ℹ️ Kaggle Real Dataset Specification & Derivations", expanded=False):
        st.markdown(f"""
        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:12px 16px; font-size:0.88rem;">
            <strong>Data Source:</strong> <a href="https://www.kaggle.com/datasets/ziya07/high-dimensional-supply-chain-inventory-dataset" target="_blank">Kaggle — High-Dimensional Supply Chain Inventory Dataset</a><br>
            <strong>Raw Dataset Dimensions:</strong> {len(raw_df)} records | {len(calc_df)} Unique SKUs | 3 Product Categories<br>
            <strong>Mathematical Mapping & Field Derivations:</strong>
            <ul style="margin-top:0.3rem; margin-bottom:0;">
                <li><code>Product</code> &larr; <code>SKU</code> + Category</li>
                <li><code>Annual_Demand</code> ($D$) &larr; <code>Number of products sold</code></li>
                <li><code>Ordering_Cost</code> ($S$) &larr; <code>Shipping costs</code></li>
                <li><code>Holding_Cost</code> ($H$) &larr; <em>DERIVED:</em> <code>Manufacturing costs</code> &times; {holding_rate*100:.0f}% annual carrying cost rate (<em>H = i &times; C</em>)</li>
                <li><code>Lead_Time_Days</code> ($L$) &larr; <code>Lead times</code></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Portfolio Top KPI Cards Grid
    total_skus = len(calc_df)
    avg_eoq = calc_df['EOQ'].mean()
    total_portfolio_cost = calc_df['Total_Annual_Inventory_Cost'].sum()
    avg_product_cost = calc_df['Total_Annual_Inventory_Cost'].mean()
    high_cost_count = len(calc_df[calc_df['Total_Annual_Inventory_Cost'] > avg_product_cost])
    
    k1, k2, k3, k4 = st.columns(4)
    
    with k1:
        st.markdown(f"""
        <div class="glass-card" style="border-top: 4px solid var(--accent-cyan);">
            <div class="glass-card-header">
                <span class="glass-label">Total Portfolio SKUs</span>
                <span class="glass-icon" style="color:var(--accent-cyan);"><i class="fa-solid fa-cubes"></i></span>
            </div>
            <div class="glass-value">{total_skus}</div>
            <div class="glass-sub" style="color:var(--accent-cyan);">Active SKU Count</div>
        </div>
        """, unsafe_allow_html=True)
        
    with k2:
        st.markdown(f"""
        <div class="glass-card" style="border-top: 4px solid var(--accent-emerald);">
            <div class="glass-card-header">
                <span class="glass-label">Average Portfolio EOQ</span>
                <span class="glass-icon" style="color:var(--accent-emerald);"><i class="fa-solid fa-boxes-stacked"></i></span>
            </div>
            <div class="glass-value">{avg_eoq:,.1f} <span style="font-size:1rem;">units</span></div>
            <div class="glass-sub" style="color:var(--accent-emerald);">Optimal Mean Lot Size</div>
        </div>
        """, unsafe_allow_html=True)
        
    with k3:
        st.markdown(f"""
        <div class="glass-card" style="border-top: 4px solid var(--accent-indigo);">
            <div class="glass-card-header">
                <span class="glass-label">Total Annual Cost</span>
                <span class="glass-icon" style="color:var(--accent-indigo);"><i class="fa-solid fa-sack-dollar"></i></span>
            </div>
            <div class="glass-value">${total_portfolio_cost:,.2f}</div>
            <div class="glass-sub" style="color:var(--accent-indigo);">Combined Inventory Expense</div>
        </div>
        """, unsafe_allow_html=True)
        
    with k4:
        st.markdown(f"""
        <div class="glass-card" style="border-top: 4px solid var(--accent-rose);">
            <div class="glass-card-header">
                <span class="glass-label">High-Cost Focus SKUs</span>
                <span class="glass-icon" style="color:var(--accent-rose);"><i class="fa-solid fa-triangle-exclamation"></i></span>
            </div>
            <div class="glass-value" style="color:var(--accent-rose);">{high_cost_count} <span style="font-size:1rem;">SKUs</span></div>
            <div class="glass-sub" style="color:var(--accent-rose);">Above Mean (${avg_product_cost:,.0f})</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Visual Analytics Grid
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown(f"#### <i class='fa-solid fa-chart-line' style='color:#059669;'></i> EOQ Cost Trade-Off Curve ({selected_sku})", unsafe_allow_html=True)
        tradeoff_df = eoq_model.calculate_cost_tradeoff(product_row=product_data)
        
        fig_tradeoff = go.Figure()
        fig_tradeoff.add_trace(go.Scatter(
            x=tradeoff_df['Order_Quantity'], y=tradeoff_df['Annual_Ordering_Cost'],
            mode='lines', name='Annual Ordering Cost', line=dict(color='#d97706', width=2, dash='dash')
        ))
        fig_tradeoff.add_trace(go.Scatter(
            x=tradeoff_df['Order_Quantity'], y=tradeoff_df['Annual_Holding_Cost'],
            mode='lines', name='Annual Holding Cost', line=dict(color='#059669', width=2, dash='dash')
        ))
        fig_tradeoff.add_trace(go.Scatter(
            x=tradeoff_df['Order_Quantity'], y=tradeoff_df['Total_Annual_Inventory_Cost'],
            mode='lines', name='Total Annual Cost', line=dict(color='#4f46e5', width=3)
        ))
        
        selected_eoq = float(product_data['EOQ'])
        fig_tradeoff.add_vline(
            x=selected_eoq, line_width=2, line_dash="dot", line_color="#e11d48",
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
        st.markdown("#### <i class='fa-solid fa-chart-bar' style='color:#0284c7;'></i> Total Inventory Cost by SKU (Top 15)", unsafe_allow_html=True)
        top15_df = calc_df.sort_values(by='Total_Annual_Inventory_Cost', ascending=False).head(15)
        colors = ['#059669' if p == selected_sku else '#94a3b8' for p in top15_df['Product']]
        
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


# ==============================================================================
# VIEW 2: INVENTORY ANALYTICS
# ==============================================================================
elif nav_selection == "📈 Inventory Analytics":
    st.markdown(f"### <i class='fa-solid fa-magnifying-glass-chart' style='color:#0284c7;'></i> Deep-Dive Analytics: **{selected_sku}**", unsafe_allow_html=True)
    
    # Selected SKU Metric Cards Grid
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="glass-card" style="border-top: 4px solid var(--accent-emerald);">
            <div class="glass-card-header">
                <span class="glass-label">EOQ Batch Size</span>
                <span class="glass-icon" style="color:var(--accent-emerald);"><i class="fa-solid fa-box-archive"></i></span>
            </div>
            <div class="glass-value">{product_data['EOQ']:,.2f}</div>
            <div class="glass-sub" style="color:var(--accent-emerald);">Optimal Order Units</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="glass-card" style="border-top: 4px solid var(--accent-cyan);">
            <div class="glass-card-header">
                <span class="glass-label">Order Frequency</span>
                <span class="glass-icon" style="color:var(--accent-cyan);"><i class="fa-solid fa-rotate"></i></span>
            </div>
            <div class="glass-value">{product_data['Number_of_Orders_Per_Year']:,.2f}</div>
            <div class="glass-sub" style="color:var(--accent-cyan);">Orders / Year</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="glass-card" style="border-top: 4px solid var(--accent-indigo);">
            <div class="glass-card-header">
                <span class="glass-label">Total Annual Cost</span>
                <span class="glass-icon" style="color:var(--accent-indigo);"><i class="fa-solid fa-calculator"></i></span>
            </div>
            <div class="glass-value">${product_data['Total_Annual_Inventory_Cost']:,.2f}</div>
            <div class="glass-sub" style="color:var(--accent-indigo);">Holding + Ordering</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="glass-card" style="border-top: 4px solid var(--accent-amber);">
            <div class="glass-card-header">
                <span class="glass-label">Reorder Point (ROP)</span>
                <span class="glass-icon" style="color:var(--accent-amber);"><i class="fa-solid fa-bell"></i></span>
            </div>
            <div class="glass-value">{product_data['Reorder_Point']:,.2f}</div>
            <div class="glass-sub" style="color:var(--accent-amber);">Replenishment Threshold</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    chart_c1, chart_c2 = st.columns(2)
    
    with chart_c1:
        st.markdown("#### <i class='fa-solid fa-scale-balanced' style='color:#059669;'></i> Cost Trade-Off Curve", unsafe_allow_html=True)
        tradeoff_df = eoq_model.calculate_cost_tradeoff(product_row=product_data)
        
        fig_tradeoff = go.Figure()
        fig_tradeoff.add_trace(go.Scatter(
            x=tradeoff_df['Order_Quantity'], y=tradeoff_df['Annual_Ordering_Cost'],
            mode='lines', name='Annual Ordering Cost', line=dict(color='#d97706', width=2, dash='dash')
        ))
        fig_tradeoff.add_trace(go.Scatter(
            x=tradeoff_df['Order_Quantity'], y=tradeoff_df['Annual_Holding_Cost'],
            mode='lines', name='Annual Holding Cost', line=dict(color='#059669', width=2, dash='dash')
        ))
        fig_tradeoff.add_trace(go.Scatter(
            x=tradeoff_df['Order_Quantity'], y=tradeoff_df['Total_Annual_Inventory_Cost'],
            mode='lines', name='Total Annual Cost', line=dict(color='#4f46e5', width=3)
        ))
        
        selected_eoq = float(product_data['EOQ'])
        fig_tradeoff.add_vline(
            x=selected_eoq, line_width=2, line_dash="dot", line_color="#e11d48",
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
        st.markdown("#### <i class='fa-solid fa-chart-pie' style='color:#4f46e5;'></i> Portfolio Cost Distribution", unsafe_allow_html=True)
        fig_hist = px.histogram(
            calc_df, x='Total_Annual_Inventory_Cost', nbins=20,
            labels={'Total_Annual_Inventory_Cost': 'Total Annual Cost ($)'},
            color_discrete_sequence=['#059669'], template='plotly_white'
        )
        fig_hist.update_layout(height=400, yaxis_title="SKU Count", showlegend=False)
        st.plotly_chart(fig_hist, use_container_width=True)
        
    st.markdown("---")
    
    # Insights & Recommendations Cards
    highest_row = calc_df.loc[calc_df['Total_Annual_Inventory_Cost'].idxmax()]
    lowest_row = calc_df.loc[calc_df['Total_Annual_Inventory_Cost'].idxmin()]
    
    ins1, ins2 = st.columns(2)
    with ins1:
        st.markdown("""
        <div class="glass-insight">
            <h4 style="margin-top:0; color:var(--accent-cyan);"><i class="fa-solid fa-lightbulb"></i> Dynamic Business Insights</h4>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        - **Highest Cost SKU**: **{highest_row['Product']}** incurring **${highest_row['Total_Annual_Inventory_Cost']:,.2f}** annually.
        - **Lowest Cost SKU**: **{lowest_row['Product']}** incurring **${lowest_row['Total_Annual_Inventory_Cost']:,.2f}** annually.
        - **Selected Item ({selected_sku}) Analysis**:
          - Recommended batch size (EOQ): **{product_data['EOQ']:,.2f} units**.
          - Ordering frequency: **{product_data['Number_of_Orders_Per_Year']:,.2f} orders/year** (every **{365/product_data['Number_of_Orders_Per_Year']:,.1f} days**).
          - Supplier lead-time threshold: **{product_data['Reorder_Point']:,.2f} units**.
        """)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with ins2:
        st.markdown("""
        <div class="glass-recommendation">
            <h4 style="margin-top:0; color:var(--accent-emerald);"><i class="fa-solid fa-bullseye"></i> Actionable Recommendation</h4>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        1. **Order Batch Size**: For **{selected_sku}**, place purchase orders of exactly **{product_data['EOQ']:,.2f} units** per cycle.
        2. **Replenishment Trigger**: Trigger replenishment when stock reaches **{product_data['Reorder_Point']:,.2f} units** to cover the **{product_data['Lead_Time_Days']} day** lead time window.
        3. **Inventory Prioritization**: Focus cost reduction and vendor contract negotiations on **{highest_row['Product']}**.
        """)
        st.markdown("</div>", unsafe_allow_html=True)


# ==============================================================================
# VIEW 3: DATA EXPLORER
# ==============================================================================
elif nav_selection == "🔍 Data Explorer":
    st.markdown("### <i class='fa-solid fa-table-list' style='color:#059669;'></i> Complete Inventory Data Explorer", unsafe_allow_html=True)
    
    col_search, col_filter = st.columns([2, 1])
    with col_search:
        search_query = st.text_input("🔍 Search SKU or Category Name...", "")
    with col_filter:
        sort_col = st.selectbox("Sort By Metric", options=['Total_Annual_Inventory_Cost', 'EOQ', 'Annual_Demand', 'Reorder_Point'], index=0)
        
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
    st.markdown("#### <i class='fa-solid fa-square-root-variable'></i> Mathematical Model & Derivation Reference", unsafe_allow_html=True)
    f1, f2 = st.columns(2)
    with f1:
        st.latex(r"\text{EOQ} = \sqrt{\frac{2 \cdot D \cdot S}{H}}")
        st.latex(r"\text{Total Cost} = \left(\frac{D}{\text{EOQ}} \cdot S\right) + \left(\frac{\text{EOQ}}{2} \cdot H\right)")
    with f2:
        st.latex(r"H = i \times \text{Manufacturing Cost } (i=0.20)")
        st.latex(r"\text{Reorder Point (ROP)} = \left(\frac{D}{365}\right) \times \text{Lead Time Days}")
