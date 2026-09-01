# Smart Inventory Advisor: Technical & Executive Report
**Course**: MSc Data Science — Modelling in Operations Management (05MD0302)  
**Project**: Problem 1 — Smart Inventory Advisor (EOQ Dashboard)  
**Date**: September 2026  

---

## 1. Introduction
Modern supply chain management requires balancing inventory holding costs against order execution expenses. In retail, hardware, and electronics distribution, inefficient inventory policy leads to working capital tie-ups or stockouts. This report details the technical architecture, mathematical model, and empirical results of the **Smart Inventory Advisor**, a Streamlit-based inventory optimization tool developed for MSc Data Science mini-hackathon evaluation.

---

## 2. Business Problem
Organizations face a fundamental trade-off when purchasing inventory:
- **Ordering Costs ($S$)**: Incurred per purchase order placed (freight, administrative overhead, inspection). Ordering in large quantities reduces the number of purchase orders and lowers total ordering costs.
- **Holding Costs ($H$)**: Incurred per unit held in inventory per year (warehousing, insurance, depreciation, opportunity cost of capital). Ordering in large quantities inflates average inventory levels, increasing total holding costs.

Without quantitative decision support, managers rely on ad-hoc order quantities, causing unnecessary inventory costs and stockout risk during supplier lead times.

---

## 3. Objective
The primary objectives of this project are:
1. Develop an automated analytics engine (`eoq_model.py`) to compute optimal Economic Order Quantity (EOQ), annual order frequency, total inventory costs, and Reorder Point (ROP).
2. Enforce strict input data validation against malformed, non-numeric, or non-positive records.
3. Build an intuitive, interactive Streamlit dashboard (`app.py`) for decision-makers.
4. Deliver actionable business recommendations driven dynamically by empirical optimization outputs.

---

## 4. Dataset Description
The model accepts portfolio inventory data with five required columns:
- **`Product`**: Identifier/name of the product.
- **`Annual_Demand` ($D$)**: Total forecast units required per year.
- **`Ordering_Cost` ($S$)**: Fixed cost per purchase order in USD.
- **`Holding_Cost` ($H$)**: Annual holding cost per unit stored in USD.
- **`Lead_Time_Days` ($L$)**: Supplier delivery lead time in days.

The standard demonstration dataset (`data/inventory_data.csv`) contains six representative tech products:
1. **Laptop**: Annual Demand = 1,200 units, Ordering Cost = $150.00, Holding Cost = $40.00, Lead Time = 7 days.
2. **Monitor**: Annual Demand = 2,400 units, Ordering Cost = $100.00, Holding Cost = $20.00, Lead Time = 5 days.
3. **Keyboard**: Annual Demand = 5,000 units, Ordering Cost = $50.00, Holding Cost = $5.00, Lead Time = 3 days.
4. **Mouse**: Annual Demand = 6,000 units, Ordering Cost = $40.00, Holding Cost = $3.00, Lead Time = 3 days.
5. **Printer**: Annual Demand = 800 units, Ordering Cost = $200.00, Holding Cost = $35.00, Lead Time = 10 days.
6. **Headset**: Annual Demand = 3,000 units, Ordering Cost = $60.00, Holding Cost = $8.00, Lead Time = 4 days.

---

## 5. Mathematical Model
The inventory system operates under classic Economic Order Quantity assumptions:
- Constant annual demand ($D$).
- Constant supplier lead time ($L$).
- Instantaneous order replenishment upon arrival.
- No quantity discounts or stockout allowances.

---

## 6. EOQ Formula
The optimal batch size ($EOQ$) minimizes the total annual inventory cost curve by balancing annual ordering cost against annual holding cost:

$$\text{EOQ} = \sqrt{\frac{2 \cdot D \cdot S}{H}}$$

Where:
- $D$ = Annual Demand (units/year)
- $S$ = Ordering Cost ($/order)
- $H$ = Holding Cost ($/unit/year)

At the exact point where $Q = \text{EOQ}$, **Annual Ordering Cost equals Annual Holding Cost**.

---

## 7. Inventory Cost Calculations
From the optimal order quantity $\text{EOQ}$, the secondary metrics are calculated:

1. **Number of Orders per Year**:
   $$\text{Orders/Year} = \frac{D}{\text{EOQ}}$$

2. **Annual Ordering Cost**:
   $$\text{Annual Ordering Cost} = \left(\frac{D}{\text{EOQ}}\right) \times S$$

3. **Annual Holding Cost**:
   $$\text{Annual Holding Cost} = \left(\frac{\text{EOQ}}{2}\right) \times H$$

4. **Total Annual Inventory Cost**:
   $$\text{Total Annual Cost} = \text{Annual Ordering Cost} + \text{Annual Holding Cost}$$

---

## 8. Reorder Point
To prevent stockouts while waiting for supplier deliveries, replenishment purchase orders must be placed when stock reaches the Reorder Point ($\text{ROP}$):

$$\text{Daily Demand} = \frac{D}{365}$$

$$\text{Reorder Point (ROP)} = \text{Daily Demand} \times L$$

---

## 9. System Architecture
The application adheres to a modular, standard Python project architecture:

```text
An-EOQ-Based-Inventory-Optimization-Dashboard/
├── app.py                  # Streamlit visual dashboard & UI
├── eoq_model.py            # Core analytics engine & validation rules
├── test_eoq_model.py       # Automated unit test suite (9 test cases)
├── requirements.txt        # Package dependencies
├── README.md               # Quickstart setup & usage guide
├── data/
│   └── inventory_data.csv  # 6-product sample dataset
└── docs/
    └── report.md           # Technical & executive documentation
```

---

## 10. Implementation
The core computational module (`eoq_model.py`) includes two core functions:
1. `validate_input_dataframe(df)`: Enforces schema completeness, converts data types safely, and verifies strictly positive values ($> 0$).
2. `calculate_eoq(df)`: Executes vectorized NumPy/pandas calculations for all inventory metrics across the portfolio.
3. `calculate_cost_tradeoff(annual_demand, ordering_cost, holding_cost)`: Generates continuous order quantity arrays ranging from 20% to 200% of EOQ for plotting tradeoff curves.

---

## 11. Streamlit Dashboard
The front-end user interface (`app.py`) features:
- **Sidebar Input**: CSV file uploader with automated fallback to `data/inventory_data.csv`, plus dynamic product dropdown selection.
- **Top Metric Cards**: Real-time display of selected product's EOQ, Annual Orders, Total Annual Cost, and Reorder Point.
- **Formated Summary Table**: Full summary table listing all original and computed metrics across all products, rounded to 2 decimal places.
- **Plotly Visualizations**: Interactive cost-curve line plot and cross-product bar chart.
- **Dynamic Business Insights & Recommendations**: Textual guidance calculated on the fly.

---

## 12. Results
Below are the actual calculated results generated by running `eoq_model.py` on `data/inventory_data.csv`:

| Product | Demand ($D$) | Order Cost ($S$) | Hold Cost ($H$) | Lead Time ($L$) | EOQ (Units) | Orders/Yr | Annual Order Cost ($) | Annual Hold Cost ($) | Total Annual Cost ($) | Daily Demand | Reorder Point |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Laptop** | 1,200 | $150.00 | $40.00 | 7 days | **94.87** | 12.65 | $1,897.37 | $1,897.37 | **$3,794.73** | 3.29 | **23.01** |
| **Monitor** | 2,400 | $100.00 | $20.00 | 5 days | **154.92** | 15.49 | $1,549.19 | $1,549.19 | **$3,098.39** | 6.58 | **32.88** |
| **Keyboard** | 5,000 | $50.00 | $5.00 | 3 days | **316.23** | 15.81 | $790.57 | $790.57 | **$1,581.14** | 13.70 | **41.10** |
| **Mouse** | 6,000 | $40.00 | $3.00 | 3 days | **400.00** | 15.00 | $600.00 | $600.00 | **$1,200.00** | 16.44 | **49.32** |
| **Printer** | 800 | $200.00 | $35.00 | 10 days | **95.62** | 8.37 | $1,673.32 | $1,673.32 | **$3,346.64** | 2.19 | **21.92** |
| **Headset** | 3,000 | $60.00 | $8.00 | 4 days | **212.13** | 14.14 | $848.53 | $848.53 | **$1,697.06** | 8.22 | **32.88** |

**Portfolio Totals**:
- Total Portfolio Annual Inventory Cost: **$14,717.95**

---

## 13. Visualization
1. **Cost Trade-Off Chart (Plotly)**: Demonstrates that at $Q < \text{EOQ}$, ordering costs dominate, while at $Q > \text{EOQ}$, holding costs dominate. The red dotted vertical line clearly indicates the optimal batch size where total cost is minimized.
2. **Product Cost Comparison Chart (Plotly Bar)**: Shows the distribution of total annual inventory costs across products, making high-impact items immediately visible to procurement teams.

---

## 14. Business Insights
- **Highest Inventory Cost Driver**: **Laptop** accounts for the highest single annual inventory cost at **$3,794.73**, driven by high holding costs ($40.00/unit/year) and high ordering costs ($150.00/order).
- **Lowest Inventory Cost Driver**: **Mouse** exhibits the lowest annual inventory cost at **$1,200.00**, despite having the highest demand (6,000 units), due to a very low unit holding cost ($3.00/unit/year).
- **Equilibrium Verification**: Across all products, calculated Annual Ordering Cost exactly equals Annual Holding Cost at EOQ, verifying mathematical optimization.

---

## 15. Recommendation
Based on calculated optimization metrics:
1. **Batch Size Strategy for Laptop**: Order in lots of approximately **95 units** (94.87) per cycle, placing approximately **13 orders per year** (12.65).
2. **Replenishment Threshold for Laptop**: Trigger stock reorders when physical inventory drops to **23 units** (23.01) to cover demand during the **7-day lead time**.
3. **Strategic Cost Reduction**: Focus vendor negotiations on **Laptop** and **Printer** to reduce unit holding costs or fixed order costs, as these two products represent over 48% of total portfolio inventory costs.

---

## 16. Limitations
- **Constant Demand Assumption**: Real-world demand fluctuates stochastically.
- **Fixed Lead Times**: Supplier delays are not modeled.
- **No Safety Stock**: The basic EOQ model assumes zero demand variance during lead time.

---

## 17. Conclusion
The **Smart Inventory Advisor** successfully fulfills all hackathon requirements. By automating EOQ and ROP calculations and presenting results through an interactive Streamlit application, it empowers inventory managers to minimize holding and ordering expenses scientifically.

---

## 18. Future Enhancement
1. **Safety Stock Integration**: Incorporate demand variability ($\sigma_D$) and lead-time variance to compute dynamic safety stock ($Z \times \sigma_D \times \sqrt{L}$).
2. **Quantity Discounts**: Extend the algorithm to evaluate volume breaks offered by suppliers.
3. **Multi-Criteria ABC Analysis**: Categorize inventory by dollar-volume usage to streamline stock audits.
