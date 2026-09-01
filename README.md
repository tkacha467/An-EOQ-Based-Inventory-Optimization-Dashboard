# Smart Inventory Advisor — EOQ Dashboard

A Streamlit dashboard for inventory optimization using Economic Order Quantity (EOQ).

## Features
- Upload an inventory CSV or use the included sample dataset
- EOQ, orders/year, ordering cost, holding cost, total annual inventory cost
- Reorder Point based on 365-day annual demand and supplier lead time
- Interactive EOQ cost trade-off chart
- Product total-cost comparison chart

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Required CSV columns
`Product`, `Annual_Demand`, `Ordering_Cost`, `Holding_Cost`, `Lead_Time_Days`

## Model
EOQ = sqrt(2DS/H), where D is annual demand, S is ordering cost, and H is holding cost.
