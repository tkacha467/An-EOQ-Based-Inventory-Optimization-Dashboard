# 🎬 Master Presentation Guide & Full Group Script
**Project**: Smart Inventory Advisor — EOQ-Based Inventory Optimization Dashboard  
**Course**: MSc Data Science — Modelling in Operations Management (05MD0302)  
**Total Group Duration**: 7.5 to 9 Minutes (2.5 - 3 Minutes per Speaker)  
**Team Members**: 3 Presenters (Speaker 1, Speaker 2, Speaker 3)

---

## 👥 Speaker Roles & Agenda Overview

| Speaker | Section / Agenda | Key Topics Covered | Target Time |
|---|---|---|---|
| **Speaker 1** | **Introduction & Problem Definition** | Why this topic, Project Scope, Core Inventory Cost Trade-off (Ordering vs. Holding Costs) | 2.5 - 3.0 min |
| **Speaker 2** | **Mathematical Model & Architecture** | EOQ Formula ($Q^*$), Reorder Point ($ROP$), Data Pipeline ($data\_pipeline.py$), Tech Stack (NumPy, pandas, Streamlit, Plotly), Unit Testing | 2.5 - 3.0 min |
| **Speaker 3** | **Live Demo, Analytics & Learnings** | Live Calculator Simulation, Cost Curves, Portfolio Insights, 3 Key Team Learnings, Conclusion & Q&A | 2.5 - 3.0 min |

---

# 🎙️ Complete Group Presentation Script

## 👤 Speaker 1: Problem Definition & Business Context (2.5 - 3 min)

> *"Respected Professor and fellow classmates, good morning. Welcome to our MSc Data Science Operations Management presentation. I am [Speaker 1 Name], presenting alongside my team members [Speaker 2 Name] and [Speaker 3 Name].*
>
> *Today, we are excited to showcase our project: **The Smart Inventory Advisor** — an enterprise-grade inventory optimization dashboard powered by real-world supply chain data.*
>
> *Why did we choose this topic? In modern global supply chains, inventory is one of the largest capital commitments on a company’s balance sheet. Holding too much inventory drains cash flow and incurs heavy storage costs, while holding too little leads to stockouts, missed sales, and dissatisfied customers.*
>
> *To understand our project, we must look at the **core operational problem**: the trade-off between two opposing cost forces.*
>
> *First, we have **Ordering Expenses**. Every time a company places a purchase order with a supplier, it incurs fixed shipping fees, freight handling, and administrative costs. To minimize these ordering fees, companies are tempted to place huge purchase orders.*
>
> *However, that triggers the second cost force: **Holding Carrying Costs**. Large orders mean warehouse shelves are overflowing. The company pays for storage space, insurance, capital interest, and risks product depreciation or damage.*
>
> *If you order in large batches, holding costs skyrocket. If you order in tiny batches, ordering costs skyrocket. Traditional purchasing decisions rely on gut feeling or arbitrary rules of thumb, leading to massive financial inefficiency.*
>
> *Our project solves this exact dilemma scientifically.*
>
> *We built a data-driven system that ingests **100 real Stock Keeping Units (SKUs)** from the Kaggle High-Dimensional Supply Chain Dataset across three product categories — Skincare, Haircare, and Cosmetics.*
>
> *Our system calculates the exact **Economic Order Quantity (EOQ)** — the precise order batch size that minimizes total annual inventory costs — as well as the **Reorder Point (ROP)** to prevent lead-time stockouts.*
>
> *Now, I will hand over to my teammate, [Speaker 2 Name], who will explain our mathematical formulation, data pipeline, and technical implementation."*

---

## 👤 Speaker 2: Mathematical Model, Data Pipeline & Tech Stack (2.5 - 3 min)

> *"Thank you, [Speaker 1 Name]. Hello everyone, I am [Speaker 2 Name], and I will walk you through the mathematical engine and technical architecture of our system.*
>
> *At the heart of our backend is the classical **Economic Order Quantity (EOQ)** model. The total annual inventory cost equation is:
> $$TC = \left(\frac{D}{Q} \cdot S\right) + \left(\frac{Q}{2} \cdot H\right)$$
> where $D$ is Annual Demand, $S$ is Shipping/Ordering Cost, $Q$ is Order Quantity, and $H$ is Unit Holding Cost.*
>
> *By taking the derivative with respect to $Q$ and setting it to zero, we derive the optimal lot size formula:
> $$Q^* = \sqrt{\frac{2 \cdot D \cdot S}{H}}$$
> At this exact point $Q^*$, annual ordering cost perfectly equals annual holding cost.*
>
> *Additionally, we compute the **Reorder Point (ROP)** as Daily Demand times Supplier Lead Time Days: $ROP = (D / 365) \cdot L$, which ensures a new order is triggered before stock is exhausted.*
>
> *To feed real data into this mathematical engine, we built an ETL data pipeline in `data_pipeline.py`.*
>
> *We mapped raw fields from the Kaggle dataset:
> - `Product` was mapped to `SKU` + `Product type`.
> - `Annual_Demand` was mapped to `Number of products sold`.
> - `Ordering_Cost` was mapped to `Shipping costs`.
> - `Lead_Time_Days` was mapped to supplier `Lead times`.*
>
> *Crucially, for **Holding Cost ($H$)**, standard inventory theory dictates that carrying cost is a percentage of unit value: $H = i \cdot C$. We derived $H$ using a standard 20% annual carrying rate ($i = 0.20$) applied to unit manufacturing cost ($C$).*
>
> *For our technology stack, we relied on industry-standard Python data science libraries:
> - **NumPy & pandas** for high-performance vectorized dataset transformations and mathematical operations.
> - **Streamlit & Plotly** for interactive web dashboard rendering.
> - **Chart.js, HTML5, & CSS3** for our standalone presentation web app.
> - **Python `unittest` framework** for automated verification.*
>
> *To guarantee mathematical accuracy, we followed **Test-Driven Development (TDD)** and built a 10-test unit suite in `test_eoq_model.py`. It tests column validation, zero/negative input rejection, EOQ precision, cost equity at $Q^*$, and pipeline cleaning. All 10 tests pass cleanly in under 0.05 seconds.*
>
> *Now, I pass the mic to [Speaker 3 Name] to demonstrate our dashboard in action and share our key takeaways."*

---

## 👤 Speaker 3: Live Demo, Visual Analytics & Key Learnings (2.5 - 3 min)

> *"Thank you, [Speaker 2 Name]. Hello everyone, I am [Speaker 3 Name], and I will demonstrate our live system in action and summarize our findings.*
>
> *As you can see on Slide 5, our **Live EOQ & Reorder Point Calculator** allows supply chain managers to select any SKU preset from our 100 real Kaggle SKUs or manually enter custom parameters.*
>
> *For example, taking `SKU0 (Skincare)` with an annual demand of 7,443 units, a shipping cost of $22.28, and a unit holding cost of $1.44:
> Our system instantly computes the optimal batch size of **479.79 units**, an ordering frequency of **15.51 orders per year**, a total annual cost of **$690.62**, and a reorder trigger threshold of **489.40 units**.*
>
> *If a manager adjusts the slider or inputs new parameters, the entire system recalculates in real-time, instantly updating the Plotly cost curves and business recommendations.*
>
> *On Slide 6, our visual analytics highlight key operational insights across the entire portfolio:
> 1. **Cost Curve Behavior**: The line chart confirms that ordering cost drops hyperbolically as batch size increases, while holding cost rises linearly. The total cost curve forms a distinct U-shape, reaching its lowest point precisely at $Q^*$.
> 2. **Portfolio Cost Distribution**: Across all 100 SKUs, total annual inventory expense totals **$44,228.32**. Our bar chart instantly pinpoints high-cost SKUs, allowing managers to prioritize vendor negotiations on top inventory drivers.*
>
> *What did our team learn from building this project?
> 1. **Operations Theory in Action**: We saw how mathematical models like EOQ transform abstract financial trade-offs into clear, actionable business rules.
> 2. **Real-World Data Engineering**: Real datasets are dirty and missing parameters. Learning how to clean data and derive valid carrying costs ($H = i \cdot C$) was crucial.
> 3. **Software Craftsmanship**: Building modular Python code, maintaining 100% unit test coverage, and crafting a responsive dual-mode frontend taught us full-stack software architecture.*
>
> *In conclusion, the Smart Inventory Advisor empowers organizations to minimize inventory expenses, eliminate stockouts, and make data-driven supply chain decisions.*
>
> *Thank you for your time. We are now ready to take any questions!"*
