# Smart Inventory Advisor: Technical & Executive Report
**Course**: MSc Data Science — Modelling in Operations Management (05MD0302), Semester 3  
**Event**: MOM Mini-Hackathon  
**Faculty Guide**: Prof. Rushika Ma'am  
**Team Members**:
1. **Tushar Pankajbhai Kacha** (Student ID: `92500567015`)
2. **Isha Kakadiya** (Student ID: `92500567016`)
3. **Kaushik Ajani** (Student ID: `92500567020`)  
**Date**: September 2026  

---

## 1. Introduction & Problem Statement
Inventory management requires balancing ordering execution costs against inventory carrying costs. In modern supply chain operations, purchasing in excessively large batches inflates holding expenses and ties up working capital, while purchasing in tiny batches skyrockets shipping and administrative costs.

The **Smart Inventory Advisor** is an enterprise analytics dashboard designed for the MOM Mini-Hackathon under the guidance of Prof. Rushika Ma'am. It processes real supply chain data, calculates the **Economic Order Quantity (EOQ)**, **Reorder Point (ROP)**, and **Total Annual Inventory Cost**, providing quantitative replenishment guidance for supply chain decision-makers.

---

## 2. Business Objective
1. Develop a mathematical backend (`eoq_model.py`) and data transformation pipeline (`data_pipeline.py`) to process real-world inventory data.
2. Calculate optimal batch size (EOQ), order frequency, total annual cost, daily demand, and reorder threshold (ROP) for every SKU.
3. Distinguish clearly between raw dataset inputs and derived cost assumptions.
4. Render a SaaS-grade Streamlit visual interface (`app.py`) and an interactive presentation frontend (`index.html`) featuring high-level KPI cards, interactive Plotly/Chart.js cost-tradeoff curves, portfolio cost distributions, and dynamic business recommendations.

---

## 3. Dataset Source & Metadata
- **Source**: [Kaggle — High-Dimensional Supply Chain Inventory Dataset](https://www.kaggle.com/datasets/ziya07/high-dimensional-supply-chain-inventory-dataset)
- **URL**: `https://www.kaggle.com/datasets/ziya07/high-dimensional-supply-chain-inventory-dataset`
- **License**: CC0: Public Domain / Open Data
- **Raw Row Count**: 100 records
- **Unique SKU Count**: 100 SKUs across 3 categories (`Haircare`, `Skincare`, `Cosmetics`)
- **Temporal Scope**: Annual operations

---

## 4. Dataset Description & Schema
The raw Kaggle dataset contains 23 operational columns across supply chain dimensions:
- `Product type`: Category (`Haircare`, `Skincare`, `Cosmetics`)
- `SKU`: Unique Stock Keeping Unit Identifier (`SKU0` through `SKU99`)
- `Price`: Unit selling price ($)
- `Availability`: Current stock level
- `Number of products sold`: Annual demand volume ($D$)
- `Revenue generated`: Annual revenue ($)
- `Stock levels`: On-hand inventory
- `Lead times`: Supplier replenishment lead time in days ($L$)
- `Order quantities`: Simulated order batch size
- `Shipping times`: Transit lead time
- `Shipping carriers`: Freight provider
- `Shipping costs`: Fixed shipping cost per purchase order ($S$)
- `Supplier name`: Supplier identifier
- `Location`: Warehouse hub location
- `Manufacturing costs`: Unit manufacturing/production cost ($C$)
- `Inspection results`: Audit status (`Pass`, `Fail`, `Pending`)
- `Defect rates`: Percentage defect rate

---

## 5. Data Cleaning & Validation
The ETL pipeline (`data_pipeline.py`) executes:
1. **Duplicate Filtering**: Drops exact duplicate rows.
2. **Type Enforcement**: Converts demand, shipping cost, manufacturing cost, and lead times to numeric `float` types.
3. **Data Scrubbing**: Removes nulls, zero values, or negative numbers across essential fields.
4. **Validation Check**: Invokes `eoq_model.validate_input_dataframe()` to verify schema integrity.

---

## 6. Data Transformation & Field Mapping
To connect raw Kaggle operational data with the EOQ model:

| EOQ Input Field | Mapped Kaggle Dataset Field | Derivation Status | Mathematical & Business Rationale |
|---|---|---|---|
| **`Product`** | `SKU` + `Product type` | **RAW MAPPED** | Combines SKU ID with category (e.g. `SKU0 (Skincare)`) for clear identification. |
| **`Annual_Demand` ($D$)** | `Number of products sold` | **RAW MAPPED** | Total annual units sold per SKU. |
| **`Ordering_Cost` ($S$)** | `Shipping costs` | **RAW MAPPED** | Fixed shipping and freight expense incurred per purchase order placed. |
| **`Holding_Cost` ($H$)** | `Manufacturing costs` $\times 0.20$ | **DERIVED** | **Assumption**: $H = i \times C$, where $i=20\%$ is the standard annual carrying cost rate (capital, storage, insurance, obsolescence) applied to unit manufacturing cost $C$. |
| **`Lead_Time_Days` ($L$)** | `Lead times` | **RAW MAPPED** | Supplier delivery lead time in calendar days. |

---

## 7. EOQ Mathematical Model
The optimal order quantity ($\text{EOQ}$) minimizes the sum of annual ordering and holding costs:

$$\text{EOQ} = \sqrt{\frac{2 \cdot D \cdot S}{H}}$$

At $Q = \text{EOQ}$, **Annual Ordering Cost equals Annual Holding Cost**.

---

## 8. Mathematical Inventory Formulas
- **Number of Orders per Year**:
  $$\text{Orders/Year} = \frac{D}{\text{EOQ}}$$

- **Annual Ordering Cost**:
  $$\text{Annual Ordering Cost} = \left(\frac{D}{\text{EOQ}}\right) \times S$$

- **Annual Holding Cost**:
  $$\text{Annual Holding Cost} = \left(\frac{\text{EOQ}}{2}\right) \times H$$

- **Total Annual Inventory Cost**:
  $$\text{Total Annual Cost} = \text{Annual Ordering Cost} + \text{Annual Holding Cost}$$

---

## 9. Reorder Point (ROP) Model
To guarantee stock availability during supplier lead time $L$:

$$\text{Daily Demand} = \frac{D}{365}$$

$$\text{Reorder Point (ROP)} = \text{Daily Demand} \times L$$

---

## 10. System Architecture
```text
RAW KAGGLE CSV (100 SKUs)
         ↓
data_pipeline.py (ETL Cleaning & Derivations)
         ↓
eoq_model.py (Vectorized NumPy/pandas Calculation)
         ↓
Dual Interface: app.py (Streamlit) & index.html (Light Presentation Frontend)
```

---

## 11. Implementation & Test Suite
- `eoq_model.py`: Implements `validate_input_dataframe()`, `calculate_eoq()`, and `calculate_cost_tradeoff()`.
- `test_eoq_model.py`: Automated test suite containing **10 unit tests** covering validation errors, calculation precision, and pipeline transformations. All 10 tests pass in 0.040s.

---

## 12. Dashboard Architecture
The interface follows a SaaS layout:
- **Header**: Team member badges (`Tushar`, `Isha`, `Kaushik`), Faculty guide (`Prof. Rushika Ma'am`), and event tag (`MOM Mini-Hackathon`).
- **Top KPI Cards**: Total Active SKUs (100), Average EOQ (456.9 units), Total Portfolio Cost ($44,228.32), High-Cost Focus SKUs count.
- **Interactive Visualizations**: High on the page (EOQ Cost Tradeoff curve and Top 15 SKU Cost bar chart).
- **Business Insights & Recommendations**: Dynamic bullet points highlighting specific SKUs.
- **Data Explorer**: Searchable, sortable table located at the bottom of the dashboard.

---

## 13. Results (Sample Processed SKUs)

| Product | Demand ($D$) | Shipping Cost ($S$) | Hold Cost ($H$) | Lead Time ($L$) | EOQ (Units) | Orders/Yr | Total Annual Cost ($) | Reorder Point |
|---|---|---|---|---|---|---|---|---|
| **SKU0 (Skincare)** | 7,443 | $22.28 | $1.442 | 24 days | **479.79** | 15.51 | **$690.62** | **489.40** |
| **SKU1 (Cosmetics)** | 7,306 | $29.46 | $5.060 | 1 day | **291.68** | 25.05 | **$1,475.76** | **20.02** |
| **SKU2 (Skincare)** | 5,696 | $45.79 | $2.574 | 6 days | **450.31** | 12.65 | **$1,159.20** | **93.63** |
| **SKU3 (Skincare)** | 5,901 | $33.09 | $6.262 | 21 days | **249.77** | 23.63 | **$1,563.85** | **339.51** |
| **SKU4 (Haircare)** | 2,906 | $10.26 | $10.650 | 6 days | **74.92** | 38.79 | **$797.87** | **47.77** |

---

## 14. Conclusion
The **Smart Inventory Advisor** successfully integrates real-world Kaggle supply chain data into a validated mathematical EOQ model delivered through a responsive frontend designed for the MSc Data Science MOM Mini-Hackathon under the guidance of Prof. Rushika Ma'am.
