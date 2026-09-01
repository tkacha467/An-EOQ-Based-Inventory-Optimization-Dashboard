# 🎙️ Presentation Script — Speaker 3: Live Demo, Key Learnings & Conclusion
**Speaker**: Kaushik Ajani (Student ID: `92500567020`)  
**Faculty Evaluator**: Prof. Rushika Ma'am  
**Course & Event**: MOM Mini-Hackathon (MSc Data Science, Sem 3)  
**Duration**: 2.5 to 3 Minutes (~350 - 400 words)  
**Slides Covered**: Slide 5 (Live Demo), Slide 6 (Metrics & Plots) & Slide 7 (Defense Prep)

---

## 📜 Word-for-Word Speech Script

### 1. Live Interactive Demonstration (0:00 - 1:00)
> *"Thank you, Isha. Respected Prof. Rushika Ma'am and classmates, I am **Kaushik Ajani**, and I will demonstrate our live system in action and summarize our findings.*
>
> *As you can see on Slide 5, our **Live EOQ & Reorder Point Calculator** allows supply chain managers to select any SKU preset from our 100 real Kaggle SKUs or manually enter custom parameters.*
>
> *For example, taking `SKU0 (Skincare)` with an annual demand of 7,443 units, a shipping cost of $22.28, and a unit holding cost of $1.44:
> Our system instantly computes the optimal batch size of **479.79 units**, an ordering frequency of **15.51 orders per year**, a total annual cost of **$690.62**, and a reorder trigger threshold of **489.40 units**.*
>
> *If a manager adjusts the slider or inputs new parameters, the entire system recalculates in real-time, instantly updating the Plotly cost curves and business recommendations."*

---

### 2. Visual Analytics & Portfolio Insights (1:00 - 1:45)
> *"On Slide 6, our visual analytics highlight key operational insights across the entire portfolio:
> 1. **Cost Curve Behavior**: The line chart confirms that ordering cost drops hyperbolically as batch size increases, while holding cost rises linearly. The total cost curve forms a distinct U-shape, reaching its lowest point precisely at $Q^*$.
> 2. **Portfolio Cost Distribution**: Across all 100 SKUs, total annual inventory expense totals **$44,228.32**. Our bar chart instantly pinpoints high-cost SKUs, allowing managers to prioritize vendor negotiations on top inventory drivers."*

---

### 3. Key Learnings & Conclusion (1:45 - 2:30)
> *"What did our team learn from building this project?
> 1. **Operations Theory in Action**: We saw how mathematical models like EOQ transform abstract financial trade-offs into clear, actionable business rules.
> 2. **Real-World Data Engineering**: Real datasets are dirty and missing parameters. Learning how to clean data and derive valid carrying costs ($H = i \cdot C$) was crucial.
> 3. **Software Craftsmanship**: Building modular Python code, maintaining 100% unit test coverage, and crafting a responsive dual-mode frontend taught us full-stack software architecture.*
>
> *In conclusion, the Smart Inventory Advisor empowers organizations to minimize inventory expenses, eliminate stockouts, and make data-driven supply chain decisions.*
>
> *Thank you, Prof. Rushika Ma'am and classmates, for your time. We are now ready to take any questions!"*

---

## 🎯 Quick Delivery Checklist for Speaker 3 (Kaushik)
- [ ] Interact with Slide 5 live controls or demonstrate the calculator on screen.
- [ ] Point out the U-shaped total cost curve on Slide 6.
- [ ] Confidently state the 3 Key Learnings (Operations Theory, Data Engineering, Software Craftsmanship).
- [ ] End with a clear invitation for Q&A to Prof. Rushika Ma'am.
