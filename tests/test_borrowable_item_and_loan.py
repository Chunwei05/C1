"""
Comprehensive tests for borrowable_item.py and loan.py to achieve high coverage.
"""

import unittest
from datetime import datetime, timedelta
from src.borrowable_item import BorrowableItem
from src.loan import Loan


class TestBorrowableItem(unittest.TestCase):
    """Test suite for BorrowableItem class"""

    # ===== Tests for initialization =====

    def test_initialization_defaults(self):
        """Test initialization with default parameters"""
        item = BorrowableItem(1, "Test Book", "Fiction Book")

        self.assertEqual(item._id, 1)
        self.assertEqual(item._name, "Test Book")
        self.assertEqual(item._type, "Fiction Book")
        self.assertEqual(item._num_copies, 1)
        self.assertEqual(item._on_loan, 0)
        self.assertEqual(item._location, "Main Library")

    def test_initialization_full_parameters(self):
        """Test initialization with all parameters"""
        item = BorrowableItem(
            item_id=100,
            name="Advanced Book",
            item_type="Non-Fiction Book",
            num_copies=5,
            on_loan=2,
            location="Science Wing"
        )

        self.assertEqual(item._id, 100)
        self.assertEqual(item._name, "Advanced Book")
        self.assertEqual(item._type, "Non-Fiction Book")
        self.assertEqual(item._num_copies, 5)
        self.assertEqual(item._on_loan, 2)
        self.assertEqual(item._location, "Science Wing")

    # ===== Tests for is_available() =====

    def test_is_available_true(self):
        """Test is_available returns True when copies available"""
        item = BorrowableItem(1, "Test Book", "Fiction Book", num_copies=5, on_loan=3)

        self.assertTrue(item.is_available())

    def test_is_available_true_none_on_loan(self):
        """Test is_available with no loans"""
        item = BorrowableItem(1, "Test Book", "Fiction Book", num_copies=3, on_loan=0)

        self.assertTrue(item.is_available())

    def test_is_available_false(self):
        """Test is_available returns False when all copies on loan"""
        item = BorrowableItem(1, "Test Book", "Fiction Book", num_copies=3, on_loan=3)

        self.assertFalse(item.is_available())

    def test_is_available_false_exceeded(self):
        """Test is_available when on_loan exceeds num_copies (edge case)"""
        item = BorrowableItem(1, "Test Book", "Fiction Book", num_copies=2, on_loan=3)

        self.assertFalse(item.is_available())

    def test_is_available_boundary(self):
        """Test is_available at boundary (one copy left)"""
        item = BorrowableItem(1, "Test Book", "Fiction Book", num_copies=5, on_loan=4)

        self.assertTrue(item.is_available())

    # ===== Tests for __str__() =====

    def test_str_representation(self):
        """Test string representation"""
        item = BorrowableItem(1, "Test Book", "Fiction Book", num_copies=5, on_loan=2, location="Main Library")

        result = str(item)

        self.assertIn("Test Book", result)
        self.assertIn("ID: 1", result)
        self.assertIn("Type: Fiction Book", result)
        self.assertIn("Available: 3/5", result)
        self.assertIn("Location: Main Library", result)

    def test_str_all_available(self):
        """Test string when all copies available"""
        item = BorrowableItem(1, "Test Book", "Fiction Book", num_copies=3, on_loan=0)

        result = str(item)

        self.assertIn("Available: 3/3", result)

    def test_str_none_available(self):
        """Test string when no copies available"""
        item = BorrowableItem(1, "Test Book", "Fiction Book", num_copies=2, on_loan=2)

        result = str(item)

        self.assertIn("Available: 0/2", result)


class TestLoan(unittest.TestCase):
    """Test suite for Loan class"""

    # ===== Tests for initialization =====

    def test_initialization(self):
        """Test loan initialization"""
        item = BorrowableItem(1, "Test Book", "Fiction Book")
        due_date = datetime.now().date() + timedelta(days=14)

        loan = Loan(item, due_date)

        self.assertEqual(loan._item, item)
        self.assertEqual(loan._due_date, due_date)

    # ===== Tests for __str__() not overdue =====

    def test_str_not_overdue(self):
        """Test string representation for current loan"""
        item = BorrowableItem(1, "Test Book", "Fiction Book")
        due_date = datetime.now().date() + timedelta(days=7)

        loan = Loan(item, due_date)
        result = str(loan)

        self.assertIn("Test Book", result)
        self.assertIn("Due:", result)
        self.assertNotIn("OVERDUE", result)

    def test_str_due_today(self):
        """Test string representation for loan due today"""
        item = BorrowableItem(1, "Test Book", "Fiction Book")
        due_date = datetime.now().date()

        loan = Loan(item, due_date)
        result = str(loan)

        self.assertIn("Test Book", result)
        self.assertIn("Due:", result)

    # ===== Tests for __str__() overdue =====

    def test_str_overdue_one_day(self):
        """Test string representation for loan overdue by 1 day"""
        item = BorrowableItem(1, "Test Book", "Fiction Book")
        due_date = datetime.now().date() - timedelta(days=1)

        loan = Loan(item, due_date)
        result = str(loan)

        self.assertIn("Test Book", result)
        self.assertIn("OVERDUE", result)
        self.assertIn("1 days", result)

    def test_str_overdue_multiple_days(self):
        """Test string representation for loan overdue by multiple days"""
        item = BorrowableItem(1, "Test Book", "Fiction Book")
        due_date = datetime.now().date() - timedelta(days=5)

        loan = Loan(item, due_date)
        result = str(loan)

        self.assertIn("Test Book", result)
        self.assertIn("OVERDUE", result)
        self.assertIn("5 days", result)

    def test_str_overdue_many_days(self):
        """Test string representation for loan long overdue"""
        item = BorrowableItem(1, "Test Book", "Fiction Book")
        due_date = datetime.now().date() - timedelta(days=30)

        loan = Loan(item, due_date)
        result = str(loan)

        self.assertIn("Test Book", result)
        self.assertIn("OVERDUE", result)
        self.assertIn("30 days", result)


if __name__ == '__main__':
    unittest.main()
