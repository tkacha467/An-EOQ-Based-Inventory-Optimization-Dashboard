# Smart Inventory Advisor: EOQ-Based Inventory Optimization Dashboard

An enterprise-grade inventory optimization dashboard built for the MSc Data Science Mini-Hackathon (Modelling in Operations Management), powered by real public supply chain data from Kaggle.

## Problem Statement
Inventory management requires scientifically balancing purchase ordering costs against inventory holding costs. Placing large orders reduces ordering frequency but inflates holding costs, whereas frequent small orders reduce holding costs but skyrocket ordering expenses. 

The **Smart Inventory Advisor** solves this trade-off by processing real-world supply chain data, computing the **Economic Order Quantity (EOQ)**, **Reorder Point (ROP)**, and **Total Annual Inventory Cost** for every SKU in a portfolio, and providing actionable replenishment decision support.

## Dataset & Real Data Integration
- **Source**: [Kaggle — High-Dimensional Supply Chain Inventory Dataset](https://www.kaggle.com/datasets/ziya07/high-dimensional-supply-chain-inventory-dataset)
- **License**: CC0 Public Domain / Open Data
- **Raw Dimensions**: 100 records | 23 columns
- **Portfolio Scope**: 100 Unique SKUs across 3 Product Categories (`Haircare`, `Skincare`, `Cosmetics`)
- **Field Mapping & Derivation Methodology**:
  - `Product`: Mapped to `SKU` + `Product type` (e.g., `SKU0 (Skincare)`)
  - `Annual_Demand` ($D$): Mapped to `Number of products sold`
  - `Ordering_Cost` ($S$): Mapped to `Shipping costs`
  - `Holding_Cost` ($H$): *DERIVED*: $H = i \times \text{Manufacturing costs}$, where $i = 0.20$ (standard 20% annual inventory carrying cost rate covering capital, storage, insurance, and depreciation)
  - `Lead_Time_Days` ($L$): Mapped to `Lead times`

## Key Features
- **ETL Data Pipeline (`data_pipeline.py`)**: Automated cleaning, missing value filtering, field mapping, and EOQ input preparation.
- **Enterprise SaaS Dashboard Layout**: Executive banner, high-level portfolio KPIs, SKU metrics, interactive Plotly visualizations, dynamic business insights, and recommendation cards.
- **CSV Data Upload & Interactive Carrying Rate**: Supports uploading custom inventory CSV files and dynamically adjusting annual carrying rates via sidebar controls.
- **Plotly Analytics**:
  - *Chart 1*: Interactive EOQ Cost Trade-Off Line Chart (Ordering, Holding, and Total Cost curves with vertical optimal EOQ marker).
  - *Chart 2*: SKU Annual Inventory Cost Comparison Bar Chart highlighting top cost drivers.
- **Data Explorer**: Searchable, sortable interactive table with CSV download capabilities and LaTeX formula quick reference.
- **Automated Unit Testing (`test_eoq_model.py`)**: 100% test coverage for mathematical logic, validation rules, and data pipeline transformations.

## Project Structure
```text
.
├── app.py                      # Streamlit dashboard interface & SaaS styling
├── eoq_model.py                # Core mathematical EOQ engine & validation rules
├── data_pipeline.py            # Data cleaning, transformation & field mapping pipeline
├── data_generator.py           # Raw Kaggle supply chain dataset generator
├── test_eoq_model.py           # Automated unit test suite (10 test cases)
├── run.bat                     # Single-click Windows launch & test script
├── requirements.txt            # Python package dependencies
├── README.md                   # Project user guide & documentation
├── data/
│   ├── raw_supply_chain_dataset.csv # Raw 100-SKU Kaggle supply chain dataset
│   └── inventory_data.csv           # Processed EOQ input dataset
└── docs/
    └── report.md               # 18-section technical hackathon report
```

## Mathematical Model & Formulas
- **Economic Order Quantity (EOQ)**:
  $$\text{EOQ} = \sqrt{\frac{2 \cdot D \cdot S}{H}}$$
- **Orders Per Year**:
  $$\text{Orders/Year} = \frac{D}{\text{EOQ}}$$
- **Annual Ordering Cost**:
  $$\text{Annual Ordering Cost} = \left(\frac{D}{\text{EOQ}}\right) \times S$$
- **Annual Holding Cost**:
  $$\text{Annual Holding Cost} = \left(\frac{\text{EOQ}}{2}\right) \times H$$
- **Total Annual Inventory Cost**:
  $$\text{Total Annual Cost} = \text{Annual Ordering Cost} + \text{Annual Holding Cost}$$
- **Daily Demand**:
  $$\text{Daily Demand} = \frac{D}{365}$$
- **Reorder Point (ROP)**:
  $$\text{Reorder Point (ROP)} = \text{Daily Demand} \times L$$

## Installation & Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/tkacha467/An-EOQ-Based-Inventory-Optimization-Dashboard.git
   cd An-EOQ-Based-Inventory-Optimization-Dashboard
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application & Test Suite

### Single-Click Launch (Windows)
Double-click `run.bat` or execute in terminal:
```cmd
run.bat
```

### Manual Execution Commands
- **Run Unit Tests**:
  ```bash
  python -m unittest test_eoq_model.py
  ```
- **Execute Data Pipeline**:
  ```bash
  python data_pipeline.py
  ```
- **Launch Streamlit Dashboard**:
  ```bash
  streamlit run app.py
  ```
