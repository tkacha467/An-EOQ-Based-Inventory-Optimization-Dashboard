"""
Unit tests for eoq_model.py module covering required validation and mathematical rules.
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


class TestEOQModel(unittest.TestCase):

    def setUp(self):
        self.valid_data = pd.DataFrame({
            'Product': ['Laptop', 'Monitor'],
            'Annual_Demand': [1200, 2400],
            'Ordering_Cost': [150.0, 100.0],
            'Holding_Cost': [40.0, 20.0],
            'Lead_Time_Days': [7, 5]
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
            'Product': ['Laptop'],
            'Annual_Demand': [1200],
            'Ordering_Cost': [150.0]
        })
        with self.assertRaises(ValueError) as ctx:
            calculate_eoq(invalid_df)
        self.assertIn("missing required column", str(ctx.exception))

    def test_3_non_numeric_values(self):
        """Test that non-numeric strings in numeric columns raise a ValueError."""
        invalid_df = pd.DataFrame({
            'Product': ['Laptop'],
            'Annual_Demand': ['non_numeric_value'],
            'Ordering_Cost': [150.0],
            'Holding_Cost': [40.0],
            'Lead_Time_Days': [7]
        })
        with self.assertRaises(ValueError) as ctx:
            calculate_eoq(invalid_df)
        self.assertIn("contains non-numeric or missing", str(ctx.exception))

    def test_4_zero_values(self):
        """Test that zero values in numeric fields raise a ValueError."""
        invalid_df = self.valid_data.copy()
        invalid_df.loc[0, 'Annual_Demand'] = 0.0
        with self.assertRaises(ValueError) as ctx:
            calculate_eoq(invalid_df)
        self.assertIn("contains zero or negative values", str(ctx.exception))

    def test_5_negative_values(self):
        """Test that negative values in numeric fields raise a ValueError."""
        invalid_df = self.valid_data.copy()
        invalid_df.loc[0, 'Ordering_Cost'] = -50.0
        with self.assertRaises(ValueError) as ctx:
            calculate_eoq(invalid_df)
        self.assertIn("contains zero or negative values", str(ctx.exception))

    def test_6_eoq_calculation(self):
        """Test accuracy of EOQ formula: sqrt((2 * D * S) / H)."""
        res = calculate_eoq(self.valid_data)
        # Laptop: sqrt((2 * 1200 * 150) / 40) = sqrt(9000) ≈ 94.8683298
        expected_eoq = math.sqrt((2 * 1200 * 150.0) / 40.0)
        self.assertAlmostEqual(res.loc[0, 'EOQ'], expected_eoq, places=5)

    def test_7_cost_calculation(self):
        """Test ordering, holding, and total annual inventory cost calculations."""
        res = calculate_eoq(self.valid_data)
        eoq = res.loc[0, 'EOQ']
        expected_ordering_cost = (1200 / eoq) * 150.0
        expected_holding_cost = (eoq / 2.0) * 40.0
        expected_total_cost = expected_ordering_cost + expected_holding_cost

        self.assertAlmostEqual(res.loc[0, 'Annual_Ordering_Cost'], expected_ordering_cost, places=5)
        self.assertAlmostEqual(res.loc[0, 'Annual_Holding_Cost'], expected_holding_cost, places=5)
        self.assertAlmostEqual(res.loc[0, 'Total_Annual_Inventory_Cost'], expected_total_cost, places=5)

    def test_8_reorder_point(self):
        """Test daily demand and reorder point calculation."""
        res = calculate_eoq(self.valid_data)
        expected_daily_demand = 1200 / 365.0
        expected_rop = expected_daily_demand * 7
        self.assertAlmostEqual(res.loc[0, 'Daily_Demand'], expected_daily_demand, places=5)
        self.assertAlmostEqual(res.loc[0, 'Reorder_Point'], expected_rop, places=5)

    def test_9_cost_tradeoff_generation(self):
        """Test cost tradeoff DataFrame generation function."""
        tradeoff = calculate_cost_tradeoff(annual_demand=1200, ordering_cost=150.0, holding_cost=40.0, num_points=20)
        self.assertEqual(len(tradeoff), 20)
        self.assertIn('Order_Quantity', tradeoff.columns)
        self.assertIn('Annual_Ordering_Cost', tradeoff.columns)
        self.assertIn('Annual_Holding_Cost', tradeoff.columns)
        self.assertIn('Total_Annual_Inventory_Cost', tradeoff.columns)


if __name__ == '__main__':
    unittest.main()
