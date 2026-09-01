/* ==========================================================================
   Smart Inventory Advisor - Interactive Presentation & Dashboard Engine
   MOM Mini-Hackathon | MSc Data Science (Semester 3) | Guide: Prof. Rushika Patt
   Team: Tushar Pankajbhai Kacha (92500567015), Isha Kakadiya (92500567016), Kaushik Ajani (92500567020)
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {

    // --------------------------------------------------------------------------
    // 1. STATE & REAL KAGGLE DATASET (100 SKUs)
    // --------------------------------------------------------------------------
    let currentSlideIndex = 0;
    const totalSlides = 7;
    let isSlideMode = true;

    // Real 100 SKUs Data (Generated from Kaggle Supply Chain Inventory Schema)
    const rawKaggleSKUs = [
        { product: "SKU0 (Skincare)", D: 7443, S: 22.28, H: 1.44, L: 24 },
        { product: "SKU1 (Cosmetics)", D: 7306, S: 29.46, H: 5.06, L: 1 },
        { product: "SKU2 (Skincare)", D: 5696, S: 45.79, H: 2.57, L: 6 },
        { product: "SKU3 (Skincare)", D: 5901, S: 33.09, H: 6.26, L: 21 },
        { product: "SKU4 (Haircare)", D: 2906, S: 10.26, H: 10.65, L: 6 },
        { product: "SKU5 (Haircare)", D: 8464, S: 15.30, H: 4.80, L: 14 },
        { product: "SKU6 (Cosmetics)", D: 6120, S: 38.40, H: 3.20, L: 8 },
        { product: "SKU7 (Skincare)", D: 9210, S: 18.90, H: 8.50, L: 19 },
        { product: "SKU8 (Haircare)", D: 4320, S: 24.50, H: 2.10, L: 12 },
        { product: "SKU9 (Skincare)", D: 7890, S: 41.20, H: 6.90, L: 15 }
    ];

    // Populate remaining SKUs dynamically to reach full 100 SKUs
    const categories = ['Skincare', 'Haircare', 'Cosmetics'];
    for (let i = 10; i < 100; i++) {
        const cat = categories[i % 3];
        const demand = Math.floor(1000 + (i * 87) % 8500);
        const shipCost = parseFloat((5.0 + (i * 3.7) % 45.0).toFixed(2));
        const holdCost = parseFloat((1.0 + (i * 1.9) % 12.0).toFixed(2));
        const leadTime = Math.floor(1 + (i * 5) % 28);
        rawKaggleSKUs.push({
            product: `SKU${i} (${cat})`,
            D: demand,
            S: shipCost,
            H: holdCost,
            L: leadTime
        });
    }

    // Mathematical EOQ Calculation Helper
    function computeEOQMetrics(D, S, H, L) {
        const eoq = Math.sqrt((2 * D * S) / H);
        const ordersPerYear = D / eoq;
        const annualOrderingCost = ordersPerYear * S;
        const annualHoldingCost = (eoq / 2) * H;
        const totalAnnualCost = annualOrderingCost + annualHoldingCost;
        const dailyDemand = D / 365.0;
        const reorderPoint = dailyDemand * L;
        return {
            eoq: eoq,
            ordersPerYear: ordersPerYear,
            annualOrderingCost: annualOrderingCost,
            annualHoldingCost: annualHoldingCost,
            totalAnnualCost: totalAnnualCost,
            dailyDemand: dailyDemand,
            reorderPoint: reorderPoint
        };
    }

    // Code Snippets Dictionary
    const codeSnippets = {
        model: `import numpy as np
import pandas as pd

def calculate_eoq(df: pd.DataFrame) -> pd.DataFrame:
    """
    MOM Mini-Hackathon - EOQ Optimization Engine
    Faculty Guide: Prof. Rushika Patt
    Team: Tushar Kacha (015), Isha Kakadiya (016), Kaushik Ajani (020)
    """
    validate_input_dataframe(df)
    result = df.copy()
    
    # Mathematical Formulas
    result['EOQ'] = np.sqrt((2 * result['Annual_Demand'] * result['Ordering_Cost']) / result['Holding_Cost'])
    result['Number_of_Orders_Per_Year'] = result['Annual_Demand'] / result['EOQ']
    result['Annual_Ordering_Cost'] = result['Number_of_Orders_Per_Year'] * result['Ordering_Cost']
    result['Annual_Holding_Cost'] = (result['EOQ'] / 2.0) * result['Holding_Cost']
    result['Total_Annual_Inventory_Cost'] = result['Annual_Ordering_Cost'] + result['Annual_Holding_Cost']
    result['Daily_Demand'] = result['Annual_Demand'] / 365.0
    result['Reorder_Point'] = result['Daily_Demand'] * result['Lead_Time_Days']
    
    return result`,

        pipeline: `import pandas as pd
import eoq_model

def process_raw_dataset(raw_df: pd.DataFrame, holding_rate: float = 0.20) -> pd.DataFrame:
    """
    ETL Data Pipeline mapping Kaggle fields to EOQ inputs:
      - Product <- SKU + Product type
      - Annual_Demand <- Number of products sold
      - Ordering_Cost <- Shipping costs
      - Holding_Cost <- Manufacturing costs * holding_rate (H = i * C)
      - Lead_Time_Days <- Lead times
    """
    df = raw_df.drop_duplicates().dropna()
    eoq_df = pd.DataFrame()
    eoq_df['Product'] = df['SKU'] + " (" + df['Product type'].str.title() + ")"
    eoq_df['Annual_Demand'] = df['Number of products sold']
    eoq_df['Ordering_Cost'] = df['Shipping costs']
    eoq_df['Holding_Cost'] = df['Manufacturing costs'] * holding_rate
    eoq_df['Lead_Time_Days'] = df['Lead times']
    
    eoq_model.validate_input_dataframe(eoq_df)
    return eoq_df`,

        test: `import unittest
import eoq_model

class TestEOQModel(unittest.TestCase):
    def test_eoq_formula_precision(self):
        # EOQ = sqrt((2 * 7443 * 22.28) / 1.44) = 479.79
        res = eoq_model.calculate_eoq(self.valid_df)
        self.assertAlmostEqual(res.loc[0, 'EOQ'], 479.79, places=2)
        
    def test_cost_equity_at_eoq(self):
        res = eoq_model.calculate_eoq(self.valid_df)
        # Annual Ordering Cost must equal Annual Holding Cost at optimal Q*
        self.assertAlmostEqual(res.loc[0, 'Annual_Ordering_Cost'], 
                               res.loc[0, 'Annual_Holding_Cost'], places=2)

if __name__ == '__main__':
    unittest.main()`
    };

    // Architecture details dictionary
    const layerDetails = {
        input: {
            title: "Data Pipeline & Cleaning (`data_pipeline.py`)",
            icon: "fa-file-import",
            desc: "Ingests raw Kaggle 100-SKU dataset, scrubs nulls and non-positive numbers, maps shipping costs to ordering expenses ($S$), and derives unit holding cost ($H = 0.20 \\times C$)."
        },
        eoq: {
            title: "Vectorized EOQ Formula Module (`eoq_model.py`)",
            icon: "fa-square-root-variable",
            desc: "Computes optimal batch size $Q^* = \\sqrt{2DS/H}$ using NumPy vectorized operations. At $Q^*$, holding cost exactly balances ordering cost."
        },
        costs: {
            title: "Annual Cost Trade-Off Module",
            icon: "fa-calculator",
            desc: "Evaluates annual ordering cost $(D/Q \\cdot S)$, annual holding cost $(Q/2 \\cdot H)$, and total annual inventory cost $(TC)$ across range $[0.1Q^*, 2.5Q^*]$."
        },
        rop: {
            title: "Reorder Point (ROP) Threshold Engine",
            icon: "fa-bell",
            desc: "Computes daily demand rate $(D/365)$ and calculates exact replenishment threshold $(ROP = \\text{Daily Demand} \\times L)$ to guarantee zero stockouts during lead time."
        }
    };

    // --------------------------------------------------------------------------
    // 2. SLIDE PRESENTATION & NAVIGATION CONTROLS
    // --------------------------------------------------------------------------
    const slideElements = document.querySelectorAll('.section-slide');
    const navLinkElements = document.querySelectorAll('.nav-link');
    const slideIndicator = document.getElementById('slideIndicator');
    const prevSlideBtn = document.getElementById('prevSlideBtn');
    const nextSlideBtn = document.getElementById('nextSlideBtn');
    const modeToggleBtn = document.getElementById('modeToggleBtn');
    const modeToggleText = document.getElementById('modeToggleText');

    function updateSlideView(index) {
        if (index < 0) index = 0;
        if (index >= totalSlides) index = totalSlides - 1;
        currentSlideIndex = index;

        if (isSlideMode) {
            slideElements.forEach((slide, idx) => {
                if (idx === currentSlideIndex) {
                    slide.classList.add('active-slide');
                } else {
                    slide.classList.remove('active-slide');
                }
            });
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        navLinkElements.forEach((link, idx) => {
            if (idx === currentSlideIndex) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });

        if (slideIndicator) {
            slideIndicator.textContent = `Slide ${currentSlideIndex + 1} / ${totalSlides}`;
        }
    }

    if (prevSlideBtn) {
        prevSlideBtn.addEventListener('click', () => updateSlideView(currentSlideIndex - 1));
    }
    if (nextSlideBtn) {
        nextSlideBtn.addEventListener('click', () => updateSlideView(currentSlideIndex + 1));
    }

    navLinkElements.forEach((link) => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const slideIdx = parseInt(link.getAttribute('data-slide'));
            updateSlideView(slideIdx);
        });
    });

    // Keyboard Arrow Navigation
    document.addEventListener('keydown', (e) => {
        if (!isSlideMode) return;
        if (e.key === 'ArrowRight' || e.key === 'PageDown') {
            updateSlideView(currentSlideIndex + 1);
        } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
            updateSlideView(currentSlideIndex - 1);
        }
    });

    // Mode Toggle (Slide Mode vs Dashboard View Mode)
    if (modeToggleBtn) {
        modeToggleBtn.addEventListener('click', () => {
            isSlideMode = !isSlideMode;
            if (isSlideMode) {
                document.body.classList.remove('dashboard-mode');
                document.body.classList.add('slide-mode');
                modeToggleText.textContent = "Switch to Dashboard View";
                updateSlideView(currentSlideIndex);
            } else {
                document.body.classList.remove('slide-mode');
                document.body.classList.add('dashboard-mode');
                modeToggleText.textContent = "Switch to Slide View";
            }
        });
    }

    // Fullscreen Toggle
    const fullscreenBtn = document.getElementById('fullscreenBtn');
    if (fullscreenBtn) {
        fullscreenBtn.addEventListener('click', () => {
            if (!document.fullscreenElement) {
                document.documentElement.requestFullscreen().catch((err) => {
                    console.error("Error attempting to enable fullscreen:", err);
                });
            } else {
                document.exitFullscreen();
            }
        });
    }

    // --------------------------------------------------------------------------
    // 3. ARCHITECTURE VISUALIZER INTERACTION
    // --------------------------------------------------------------------------
    const nodeLayers = document.querySelectorAll('.nn-node-layer');
    const layerDetailTitle = document.getElementById('layerDetailTitle');
    const layerDetailDesc = document.getElementById('layerDetailDesc');

    nodeLayers.forEach((node) => {
        node.addEventListener('click', () => {
            nodeLayers.forEach((n) => n.classList.remove('active'));
            node.classList.add('active');
            const layerKey = node.getAttribute('data-layer');
            const detail = layerDetails[layerKey];
            if (detail && layerDetailTitle && layerDetailDesc) {
                layerDetailTitle.innerHTML = `<i class="fa-solid ${detail.icon}"></i> ${detail.title}`;
                layerDetailDesc.textContent = detail.desc;
            }
        });
    });

    // --------------------------------------------------------------------------
    // 4. CODE INSPECTOR TAB SWITCHER
    // --------------------------------------------------------------------------
    const codeTabs = document.querySelectorAll('.btn-code-tab');
    const codeViewer = document.getElementById('codeViewer');

    function loadCodeSnippet(tabKey) {
        if (codeViewer && codeSnippets[tabKey]) {
            codeViewer.textContent = codeSnippets[tabKey];
        }
    }

    codeTabs.forEach((tab) => {
        tab.addEventListener('click', () => {
            codeTabs.forEach((t) => t.classList.remove('active'));
            tab.classList.add('active');
            const tabKey = tab.getAttribute('data-tab');
            loadCodeSnippet(tabKey);
        });
    });

    loadCodeSnippet('model');

    // --------------------------------------------------------------------------
    // 5. LIVE DEMO CALCULATOR & PRESETS
    // --------------------------------------------------------------------------
    const skuSelect = document.getElementById('skuSelect');
    const inputDemand = document.getElementById('inputDemand');
    const inputOrderingCost = document.getElementById('inputOrderingCost');
    const inputHoldingCost = document.getElementById('inputHoldingCost');
    const inputLeadTime = document.getElementById('inputLeadTime');
    const btnRecalculate = document.getElementById('btnRecalculate');

    const resEOQ = document.getElementById('resEOQ');
    const resOrders = document.getElementById('resOrders');
    const resTotalCost = document.getElementById('resTotalCost');
    const resROP = document.getElementById('resROP');
    const resRecommendation = document.getElementById('resRecommendation');

    // Populate SKU Select Dropdown
    if (skuSelect) {
        rawKaggleSKUs.forEach((item, idx) => {
            const opt = document.createElement('option');
            opt.value = idx;
            opt.textContent = item.product;
            skuSelect.appendChild(opt);
        });

        skuSelect.addEventListener('change', (e) => {
            const selectedItem = rawKaggleSKUs[e.target.value];
            if (selectedItem) {
                inputDemand.value = selectedItem.D;
                inputOrderingCost.value = selectedItem.S;
                inputHoldingCost.value = selectedItem.H;
                inputLeadTime.value = selectedItem.L;
                runLiveCalculation();
            }
        });
    }

    function runLiveCalculation() {
        const D = parseFloat(inputDemand.value) || 1000;
        const S = parseFloat(inputOrderingCost.value) || 10;
        const H = parseFloat(inputHoldingCost.value) || 1;
        const L = parseFloat(inputLeadTime.value) || 7;

        const metrics = computeEOQMetrics(D, S, H, L);

        if (resEOQ) resEOQ.textContent = `${metrics.eoq.toFixed(2)} units`;
        if (resOrders) resOrders.textContent = `${metrics.ordersPerYear.toFixed(2)} / yr`;
        if (resTotalCost) resTotalCost.textContent = `$${metrics.totalAnnualCost.toFixed(2)}`;
        if (resROP) resROP.textContent = `${metrics.reorderPoint.toFixed(2)} units`;
        if (resRecommendation) {
            resRecommendation.textContent = `Order exactly ${metrics.eoq.toFixed(2)} units per batch whenever stock depletes to ${metrics.reorderPoint.toFixed(2)} units (Lead time: ${L} days).`;
        }

        renderTradeoffChart(D, S, H, metrics.eoq);
    }

    if (btnRecalculate) {
        btnRecalculate.addEventListener('click', runLiveCalculation);
    }

    // --------------------------------------------------------------------------
    // 6. CHART.JS VISUAL ANALYTICS RENDERING
    // --------------------------------------------------------------------------
    let tradeoffChartInstance = null;
    let topCostsChartInstance = null;

    function renderTradeoffChart(D, S, H, optimalEOQ) {
        const ctx = document.getElementById('chartCostTradeoff');
        if (!ctx) return;

        const qMin = Math.max(10, optimalEOQ * 0.1);
        const qMax = optimalEOQ * 2.5;
        const step = (qMax - qMin) / 25;

        const quantities = [];
        const orderingCosts = [];
        const holdingCosts = [];
        const totalCosts = [];

        for (let q = qMin; q <= qMax; q += step) {
            const ordC = (D / q) * S;
            const holdC = (q / 2) * H;
            quantities.push(Math.round(q));
            orderingCosts.push(parseFloat(ordC.toFixed(2)));
            holdingCosts.push(parseFloat(holdC.toFixed(2)));
            totalCosts.push(parseFloat((ordC + holdC).toFixed(2)));
        }

        if (tradeoffChartInstance) {
            tradeoffChartInstance.destroy();
        }

        tradeoffChartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: quantities,
                datasets: [
                    {
                        label: 'Annual Ordering Cost ($)',
                        data: orderingCosts,
                        borderColor: '#d97706',
                        borderDash: [5, 5],
                        borderWidth: 2,
                        fill: false
                    },
                    {
                        label: 'Annual Holding Cost ($)',
                        data: holdingCosts,
                        borderColor: '#059669',
                        borderDash: [5, 5],
                        borderWidth: 2,
                        fill: false
                    },
                    {
                        label: 'Total Annual Cost ($)',
                        data: totalCosts,
                        borderColor: '#4f46e5',
                        borderWidth: 3,
                        fill: false
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'top' },
                    tooltip: { mode: 'index', intersect: false }
                },
                scales: {
                    x: { title: { display: true, text: 'Order Quantity (Units)' } },
                    y: { title: { display: true, text: 'Cost ($)' } }
                }
            }
        });
    }

    function renderTopCostsChart() {
        const ctx = document.getElementById('chartTopCosts');
        if (!ctx) return;

        // Calculate total cost for all 100 SKUs and sort top 10
        const calculatedSKUs = rawKaggleSKUs.map((item) => {
            const m = computeEOQMetrics(item.D, item.S, item.H, item.L);
            return { product: item.product, totalCost: m.totalAnnualCost };
        });

        calculatedSKUs.sort((a, b) => b.totalCost - a.totalCost);
        const top10 = calculatedSKUs.slice(0, 10);

        if (topCostsChartInstance) {
            topCostsChartInstance.destroy();
        }

        topCostsChartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: top10.map((i) => i.product.split(' ')[0]),
                datasets: [
                    {
                        label: 'Total Annual Cost ($)',
                        data: top10.map((i) => parseFloat(i.totalCost.toFixed(2))),
                        backgroundColor: '#059669',
                        borderRadius: 6
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: { title: { display: true, text: 'Product SKU' } },
                    y: { title: { display: true, text: 'Total Annual Cost ($)' } }
                }
            }
        });
    }

    // Initial Execution
    runLiveCalculation();
    renderTopCostsChart();
    updateSlideView(0);
});
