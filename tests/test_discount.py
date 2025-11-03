"""
Test suite for discount calculation functionality.

This module tests the calculate_discount function using:
1. Equivalence Partitioning (EP) technique
2. Boundary Value Analysis (BVA) technique

Author: Test Suite for FIT2107 Assignment
"""

import unittest
import sys
import os

# Add src directory to path to import discount module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from discount import calculate_discount


class TestDiscount(unittest.TestCase):
    """
    Test class for discount calculation using EP and BVA techniques.
    """

    # ========== Equivalence Partitioning Tests ==========

    def test_EP_valid_discount_10_percent(self):
        """
        Test EP: Valid discount percentage (10%)
        Equivalence class: Valid discount range (0 <= discount <= 100)
        """
        result = calculate_discount(100.0, 10.0)
        self.assertEqual(result, 90.0)

    def test_EP_valid_discount_50_percent(self):
        """
        Test EP: Valid discount percentage (50%)
        Equivalence class: Valid discount range (0 <= discount <= 100)
        """
        result = calculate_discount(200.0, 50.0)
        self.assertEqual(result, 100.0)

    def test_EP_invalid_negative_discount(self):
        """
        Test EP: Invalid negative discount percentage
        Equivalence class: Negative discount (discount < 0)
        """
        with self.assertRaises(ValueError) as context:
            calculate_discount(100.0, -10.0)
        self.assertIn("cannot be negative", str(context.exception))

    def test_EP_invalid_exceeds_100_percent(self):
        """
        Test EP: Invalid discount exceeding 100%
        Equivalence class: Discount greater than 100 (discount > 100)
        """
        with self.assertRaises(ValueError) as context:
            calculate_discount(100.0, 150.0)
        self.assertIn("cannot exceed 100", str(context.exception))

    def test_EP_zero_discount(self):
        """
        Test EP: Zero discount (edge of valid range)
        Equivalence class: Valid discount range (discount = 0)
        """
        result = calculate_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_EP_maximum_valid_discount(self):
        """
        Test EP: Maximum valid discount (100%)
        Equivalence class: Valid discount range (discount = 100)
        """
        result = calculate_discount(100.0, 100.0)
        self.assertEqual(result, 0.0)

    def test_EP_invalid_negative_price(self):
        """
        Test EP: Invalid negative price
        Equivalence class: Negative price (price < 0)
        """
        with self.assertRaises(ValueError) as context:
            calculate_discount(-50.0, 10.0)
        self.assertIn("Price cannot be negative", str(context.exception))

    # ========== Boundary Value Analysis Tests ==========

    def test_BVA_discount_0_percent(self):
        """
        Test BVA: Discount at minimum boundary (0%)
        Boundary: Lower bound of valid range
        """
        result = calculate_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_BVA_discount_1_percent(self):
        """
        Test BVA: Discount just above minimum boundary (1%)
        Boundary: Just inside lower bound
        """
        result = calculate_discount(100.0, 1.0)
        self.assertEqual(result, 99.0)

    def test_BVA_discount_negative_1_percent(self):
        """
        Test BVA: Discount just below minimum boundary (-1%)
        Boundary: Just outside lower bound (invalid)
        """
        with self.assertRaises(ValueError) as context:
            calculate_discount(100.0, -1.0)
        self.assertIn("cannot be negative", str(context.exception))

    def test_BVA_discount_99_percent(self):
        """
        Test BVA: Discount just below maximum boundary (99%)
        Boundary: Just inside upper bound
        """
        result = calculate_discount(100.0, 99.0)
        self.assertEqual(result, 1.0)

    def test_BVA_discount_100_percent(self):
        """
        Test BVA: Discount at maximum boundary (100%)
        Boundary: Upper bound of valid range
        """
        result = calculate_discount(100.0, 100.0)
        self.assertEqual(result, 0.0)

    def test_BVA_discount_101_percent(self):
        """
        Test BVA: Discount just above maximum boundary (101%)
        Boundary: Just outside upper bound (invalid)
        """
        with self.assertRaises(ValueError) as context:
            calculate_discount(100.0, 101.0)
        self.assertIn("cannot exceed 100", str(context.exception))

    def test_BVA_price_boundary_zero(self):
        """
        Test BVA: Price at zero boundary
        Boundary: Minimum valid price value
        """
        result = calculate_discount(0.0, 10.0)
        self.assertEqual(result, 0.0)

    def test_BVA_price_boundary_small_positive(self):
        """
        Test BVA: Small positive price (0.01)
        Boundary: Just above minimum price
        """
        result = calculate_discount(0.01, 10.0)
        self.assertAlmostEqual(result, 0.009, places=3)

    def test_BVA_large_price_value(self):
        """
        Test BVA: Large price value
        Boundary: Testing with large values to ensure calculation accuracy
        """
        result = calculate_discount(10000.0, 25.0)
        self.assertEqual(result, 7500.0)


if __name__ == '__main__':
    unittest.main()
