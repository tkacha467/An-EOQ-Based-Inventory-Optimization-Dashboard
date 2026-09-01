# 🎙️ Presentation Script — Speaker 2: Mathematical Model, Data Pipeline & Tech Stack
**Speaker**: Isha Kakadiya (Student ID: `92500567016`)  
**Faculty Evaluator**: Prof. Rushika Patt  
**Course & Event**: MOM Mini-Hackathon (MSc Data Science, Sem 3)  
**Duration**: 2.5 to 3 Minutes (~350 - 400 words)  
**Slides Covered**: Slide 3 (Architecture & Formulas) & Slide 4 (Code Inspector)

---

## 📜 Word-for-Word Speech Script

### 1. Mathematical Formulation & EOQ Model (0:00 - 1:00)
> *"Thank you, Tushar. Respected Prof. Rushika Patt and classmates, I am **Isha Kakadiya**, and I will walk you through the mathematical engine and technical architecture of our system.*
>
> *At the heart of our backend is the classical **Economic Order Quantity (EOQ)** model. The total annual inventory cost equation is:
> $$TC = \left(\frac{D}{Q} \cdot S\right) + \left(\frac{Q}{2} \cdot H\right)$$
> where $D$ is Annual Demand, $S$ is Shipping/Ordering Cost, $Q$ is Order Quantity, and $H$ is Unit Holding Cost.*
>
> *By taking the derivative with respect to $Q$ and setting it to zero, we derive the optimal lot size formula:
> $$Q^* = \sqrt{\frac{2 \cdot D \cdot S}{H}}$$
> At this exact point $Q^*$, annual ordering cost perfectly equals annual holding cost.*
>
> *Additionally, we compute the **Reorder Point (ROP)** as Daily Demand times Supplier Lead Time Days: $ROP = (D / 365) \cdot L$, which ensures a new order is triggered before stock is exhausted."*

---

### 2. Data Pipeline & Field Mapping (1:00 - 1:45)
> *"To feed real data into this mathematical engine, we built an ETL data pipeline in `data_pipeline.py`.*
>
> *We mapped raw fields from the Kaggle dataset:
> - `Product` was mapped to `SKU` + `Product type`.
> - `Annual_Demand` was mapped to `Number of products sold`.
> - `Ordering_Cost` was mapped to `Shipping costs`.
> - `Lead_Time_Days` was mapped to supplier `Lead times`.*
>
> *Crucially, for **Holding Cost ($H$)**, standard inventory theory dictates that carrying cost is a percentage of unit value: $H = i \cdot C$. We derived $H$ using a standard 20% annual carrying rate ($i = 0.20$) applied to unit manufacturing cost ($C$)."*

---

### 3. Tech Stack, Libraries & Test-Driven Development (1:45 - 2:30)
> *"For our technology stack, we relied on industry-standard Python data science libraries:
> - **NumPy & pandas** for high-performance vectorized dataset transformations and mathematical operations.
> - **Streamlit & Plotly** for interactive web dashboard rendering.
> - **Chart.js, HTML5, & CSS3** for our standalone presentation web app.
> - **Python `unittest` framework** for automated verification.*
>
> *To guarantee mathematical accuracy, we followed **Test-Driven Development (TDD)** and built a 10-test unit suite in `test_eoq_model.py`. It tests column validation, zero/negative input rejection, EOQ precision, cost equity at $Q^*$, and pipeline cleaning. All 10 tests pass cleanly in under 0.05 seconds.*
>
> *Now, I pass the mic to **Kaushik Ajani** to demonstrate our dashboard in action and share our key takeaways."*

---

## 🎯 Quick Delivery Checklist for Speaker 2 (Isha)
- [ ] Refer to Slide 3 (Architecture & Formulas) when explaining $Q^* = \sqrt{2DS/H}$.
- [ ] Clearly explain the derived holding cost formula ($H = i \times C$).
- [ ] Mention key Python libraries (**NumPy, pandas, Streamlit, Plotly, unittest**).
