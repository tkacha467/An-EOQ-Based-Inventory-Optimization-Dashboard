"""
Unit tests for eoq_model.py and data_pipeline.py modules.
"""

import math
import pandas as pd
import unittest

from eoq_model import (
    calculate_eoq,
    calculate_cost_tradeoff,
    validate_input_dataframe,
    REQUIRED_COLUMNS
)
import data_pipeline


class TestEOQModel(unittest.TestCase):

    def setUp(self):
        self.valid_data = pd.DataFrame({
            'Product': ['SKU0 (Skincare)', 'SKU1 (Cosmetics)'],
            'Annual_Demand': [7443.0, 7306.0],
            'Ordering_Cost': [22.28, 29.46],
            'Holding_Cost': [1.442, 5.060],
            'Lead_Time_Days': [24.0, 1.0]
        })

    def test_1_required_columns_exist(self):
        """Test that validation passes when all required columns exist."""
        try:
            validate_input_dataframe(self.valid_data)
        except Exception as e:
            self.fail(f"validate_input_dataframe raised unexpected exception: {e}")

    def test_2_missing_column(self):
        """Test that missing required columns raise a ValueError."""
        invalid_df = pd.DataFrame({
            'Product': ['SKU0'],
            'Annual_Demand': [1200],
            'Ordering_Cost': [150.0]
        })
        with self.assertRaises(ValueError) as ctx:
            calculate_eoq(invalid_df)
        self.assertIn("missing required column", str(ctx.exception).lower())

    def test_3_non_numeric_values(self):
        """Test that non-numeric strings in numeric columns raise a ValueError."""
        invalid_df = pd.DataFrame({
            'Product': ['SKU0'],
            'Annual_Demand': ['non_numeric_value'],
            'Ordering_Cost': [150.0],
            'Holding_Cost': [40.0],
            'Lead_Time_Days': [7]
        })
        with self.assertRaises(ValueError) as ctx:
            calculate_eoq(invalid_df)
        self.assertIn("non-numeric or missing", str(ctx.exception).lower())

    def test_4_zero_values(self):
        """Test that zero values in numeric fields raise a ValueError."""
        invalid_df = self.valid_data.copy()
        invalid_df.loc[0, 'Annual_Demand'] = 0.0
        with self.assertRaises(ValueError) as ctx:
            calculate_eoq(invalid_df)
        self.assertIn("zero or negative values", str(ctx.exception).lower())

    def test_5_negative_values(self):
        """Test that negative values in numeric fields raise a ValueError."""
        invalid_df = self.valid_data.copy()
        invalid_df.loc[0, 'Ordering_Cost'] = -50.0
        with self.assertRaises(ValueError) as ctx:
            calculate_eoq(invalid_df)
        self.assertIn("zero or negative values", str(ctx.exception).lower())

    def test_6_eoq_calculation(self):
        """Test accuracy of EOQ formula: sqrt((2 * D * S) / H)."""
        res = calculate_eoq(self.valid_data)
        expected_eoq = math.sqrt((2 * 7443.0 * 22.28) / 1.442)
        self.assertAlmostEqual(res.loc[0, 'EOQ'], expected_eoq, places=4)

    def test_7_cost_calculation(self):
        """Test ordering, holding, and total annual inventory cost calculations."""
        res = calculate_eoq(self.valid_data)
        eoq = res.loc[0, 'EOQ']
        expected_ordering_cost = (7443.0 / eoq) * 22.28
        expected_holding_cost = (eoq / 2.0) * 1.442
        expected_total_cost = expected_ordering_cost + expected_holding_cost

        self.assertAlmostEqual(res.loc[0, 'Annual_Ordering_Cost'], expected_ordering_cost, places=4)
        self.assertAlmostEqual(res.loc[0, 'Annual_Holding_Cost'], expected_holding_cost, places=4)
        self.assertAlmostEqual(res.loc[0, 'Total_Annual_Inventory_Cost'], expected_total_cost, places=4)

    def test_8_reorder_point(self):
        """Test daily demand and reorder point calculation."""
        res = calculate_eoq(self.valid_data)
        expected_daily_demand = 7443.0 / 365.0
        expected_rop = expected_daily_demand * 24.0
        self.assertAlmostEqual(res.loc[0, 'Daily_Demand'], expected_daily_demand, places=4)
        self.assertAlmostEqual(res.loc[0, 'Reorder_Point'], expected_rop, places=4)

    def test_9_cost_tradeoff_generation(self):
        """Test cost tradeoff DataFrame generation function."""
        tradeoff = calculate_cost_tradeoff(annual_demand=7443.0, ordering_cost=22.28, holding_cost=1.442, num_points=20)
        self.assertEqual(len(tradeoff), 20)
        self.assertIn('Order_Quantity', tradeoff.columns)
        self.assertIn('Annual_Ordering_Cost', tradeoff.columns)
        self.assertIn('Annual_Holding_Cost', tradeoff.columns)
        self.assertIn('Total_Annual_Inventory_Cost', tradeoff.columns)

    def test_10_data_pipeline_transformation(self):
        """Test data pipeline transformation from Kaggle schema to EOQ format."""
        raw_sample = pd.DataFrame({
            'Product type': ['skincare'],
            'SKU': ['SKU999'],
            'Price': [50.0],
            'Availability': [30],
            'Number of products sold': [5000],
            'Revenue generated': [250000.0],
            'Customer demographics': ['Female'],
            'Stock levels': [20],
            'Lead times': [14],
            'Order quantities': [50],
            'Shipping times': [3],
            'Shipping carriers': ['Carrier A'],
            'Shipping costs': [35.0],
            'Supplier name': ['Supplier 1'],
            'Location': ['Mumbai'],
            'Production volumes': [500],
            'Manufacturing lead time': [10],
            'Manufacturing costs': [25.0],
            'Inspection results': ['Pass'],
            'Defect rates': [0.02],
            'Transportation modes': ['Road'],
            'Routes': ['Route A'],
            'Costs': [300.0]
        })
        processed = data_pipeline.process_raw_dataset(raw_sample, holding_rate=0.20)
        self.assertEqual(len(processed), 1)
        self.assertEqual(processed.loc[0, 'Product'], 'SKU999 (Skincare)')
        self.assertEqual(processed.loc[0, 'Annual_Demand'], 5000.0)
        self.assertEqual(processed.loc[0, 'Ordering_Cost'], 35.0)
        self.assertEqual(processed.loc[0, 'Holding_Cost'], 5.0)  # 25.0 * 0.20
        self.assertEqual(processed.loc[0, 'Lead_Time_Days'], 14.0)


if __name__ == '__main__':
    unittest.main()
