"""
Comprehensive tests for patron.py to achieve high coverage.
Tests the Patron class and all its methods.
"""

import unittest
from datetime import datetime, timedelta
from src.patron import Patron
from src.borrowable_item import BorrowableItem
from src.loan import Loan


class TestPatron(unittest.TestCase):
    """Test suite for Patron class"""

    # ===== Tests for get_type() =====

    def test_get_type_minor(self):
        """Test patron type for minor (age < 18)"""
        patron = Patron(1, "Minor User", 0)
        self.assertEqual(patron.get_type(), "Minor")

        patron = Patron(2, "Minor User", 10)
        self.assertEqual(patron.get_type(), "Minor")

        patron = Patron(3, "Minor User", 17)
        self.assertEqual(patron.get_type(), "Minor")

    def test_get_type_regular(self):
        """Test patron type for regular (18 <= age < 65)"""
        patron = Patron(1, "Regular User", 18)
        self.assertEqual(patron.get_type(), "Regular")

        patron = Patron(2, "Regular User", 25)
        self.assertEqual(patron.get_type(), "Regular")

        patron = Patron(3, "Regular User", 64)
        self.assertEqual(patron.get_type(), "Regular")

    def test_get_type_elderly(self):
        """Test patron type for elderly (age >= 65)"""
        patron = Patron(1, "Elderly User", 65)
        self.assertEqual(patron.get_type(), "Elderly")

        patron = Patron(2, "Elderly User", 70)
        self.assertEqual(patron.get_type(), "Elderly")

        patron = Patron(3, "Elderly User", 100)
        self.assertEqual(patron.get_type(), "Elderly")

    # ===== Tests for add_loan() =====

    def test_add_loan_default_period(self):
        """Test adding loan with default period"""
        patron = Patron(1, "Test User", 25)
        item = BorrowableItem(1, "Test Book", "Fiction Book")

        initial_loan_count = len(patron._loans)
        initial_on_loan = item._on_loan

        patron.add_loan(item)

        self.assertEqual(len(patron._loans), initial_loan_count + 1)
        self.assertEqual(item._on_loan, initial_on_loan + 1)
        self.assertEqual(patron._loans[0]._item, item)

        # Check due date is 14 days from now (default)
        expected_due = datetime.now().date() + timedelta(days=14)
        self.assertEqual(patron._loans[0]._due_date, expected_due)

    def test_add_loan_custom_period(self):
        """Test adding loan with custom period"""
        patron = Patron(1, "Test User", 25)
        item = BorrowableItem(1, "Test Book", "Fiction Book")

        patron.add_loan(item, due_days=21)

        # Check due date is 21 days from now
        expected_due = datetime.now().date() + timedelta(days=21)
        self.assertEqual(patron._loans[0]._due_date, expected_due)

    def test_add_loan_multiple_items(self):
        """Test adding multiple loans"""
        patron = Patron(1, "Test User", 25)
        item1 = BorrowableItem(1, "Book 1", "Fiction Book")
        item2 = BorrowableItem(2, "Book 2", "Non-Fiction Book")

        patron.add_loan(item1)
        patron.add_loan(item2)

        self.assertEqual(len(patron._loans), 2)
        self.assertEqual(item1._on_loan, 1)
        self.assertEqual(item2._on_loan, 1)

    # ===== Tests for return_item() =====

    def test_return_item_success(self):
        """Test successful item return"""
        patron = Patron(1, "Test User", 25)
        item = BorrowableItem(1, "Test Book", "Fiction Book")

        patron.add_loan(item)
        self.assertEqual(len(patron._loans), 1)

        result = patron.return_item(1)

        self.assertTrue(result)
        self.assertEqual(len(patron._loans), 0)
        self.assertEqual(item._on_loan, 0)

    def test_return_item_not_found(self):
        """Test returning item not on loan"""
        patron = Patron(1, "Test User", 25)
        item = BorrowableItem(1, "Test Book", "Fiction Book")

        patron.add_loan(item)

        result = patron.return_item(999)  # Non-existent item

        self.assertFalse(result)
        self.assertEqual(len(patron._loans), 1)  # Loan still exists

    def test_return_item_multiple_loans(self):
        """Test returning specific item from multiple loans"""
        patron = Patron(1, "Test User", 25)
        item1 = BorrowableItem(1, "Book 1", "Fiction Book")
        item2 = BorrowableItem(2, "Book 2", "Non-Fiction Book")
        item3 = BorrowableItem(3, "Book 3", "Magazine")

        patron.add_loan(item1)
        patron.add_loan(item2)
        patron.add_loan(item3)

        result = patron.return_item(2)  # Return item2

        self.assertTrue(result)
        self.assertEqual(len(patron._loans), 2)
        self.assertEqual(item2._on_loan, 0)
        self.assertEqual(item1._on_loan, 1)
        self.assertEqual(item3._on_loan, 1)

    # ===== Tests for has_item() =====

    def test_has_item_true(self):
        """Test has_item returns True when item is on loan"""
        patron = Patron(1, "Test User", 25)
        item = BorrowableItem(1, "Test Book", "Fiction Book")

        patron.add_loan(item)

        self.assertTrue(patron.has_item(1))

    def test_has_item_false(self):
        """Test has_item returns False when item is not on loan"""
        patron = Patron(1, "Test User", 25)
        item = BorrowableItem(1, "Test Book", "Fiction Book")

        patron.add_loan(item)

        self.assertFalse(patron.has_item(999))

    def test_has_item_empty_loans(self):
        """Test has_item with no loans"""
        patron = Patron(1, "Test User", 25)

        self.assertFalse(patron.has_item(1))

    # ===== Tests for calculate_overdue_fees() =====

    def test_calculate_overdue_fees_no_loans(self):
        """Test calculating fees with no loans"""
        patron = Patron(1, "Test User", 25)

        fees = patron.calculate_overdue_fees()
        self.assertEqual(fees, 0.0)

    def test_calculate_overdue_fees_not_overdue(self):
        """Test calculating fees when not overdue"""
        patron = Patron(1, "Test User", 25)
        item = BorrowableItem(1, "Test Book", "Fiction Book")

        patron.add_loan(item, due_days=14)  # Due in future

        fees = patron.calculate_overdue_fees()
        self.assertEqual(fees, 0.0)

    def test_calculate_overdue_fees_one_day(self):
        """Test calculating fees for 1 day overdue"""
        patron = Patron(1, "Test User", 25)
        item = BorrowableItem(1, "Test Book", "Fiction Book")

        # Create overdue loan
        due_date = datetime.now().date() - timedelta(days=1)
        loan = Loan(item, due_date)
        patron._loans.append(loan)

        fees = patron.calculate_overdue_fees()
        self.assertEqual(fees, 1.0)

    def test_calculate_overdue_fees_multiple_days(self):
        """Test calculating fees for multiple days overdue"""
        patron = Patron(1, "Test User", 25)
        item = BorrowableItem(1, "Test Book", "Fiction Book")

        # Create overdue loan (5 days)
        due_date = datetime.now().date() - timedelta(days=5)
        loan = Loan(item, due_date)
        patron._loans.append(loan)

        fees = patron.calculate_overdue_fees()
        self.assertEqual(fees, 5.0)

    def test_calculate_overdue_fees_multiple_loans(self):
        """Test calculating fees for multiple overdue loans"""
        patron = Patron(1, "Test User", 25)
        item1 = BorrowableItem(1, "Book 1", "Fiction Book")
        item2 = BorrowableItem(2, "Book 2", "Non-Fiction Book")

        # First loan: 3 days overdue
        due_date1 = datetime.now().date() - timedelta(days=3)
        loan1 = Loan(item1, due_date1)
        patron._loans.append(loan1)

        # Second loan: 2 days overdue
        due_date2 = datetime.now().date() - timedelta(days=2)
        loan2 = Loan(item2, due_date2)
        patron._loans.append(loan2)

        fees = patron.calculate_overdue_fees()
        self.assertEqual(fees, 5.0)  # 3 + 2 = 5

    def test_calculate_overdue_fees_mixed_loans(self):
        """Test calculating fees with mix of overdue and current loans"""
        patron = Patron(1, "Test User", 25)
        item1 = BorrowableItem(1, "Book 1", "Fiction Book")
        item2 = BorrowableItem(2, "Book 2", "Non-Fiction Book")

        # Overdue loan: 4 days
        due_date1 = datetime.now().date() - timedelta(days=4)
        loan1 = Loan(item1, due_date1)
        patron._loans.append(loan1)

        # Current loan: not due yet
        due_date2 = datetime.now().date() + timedelta(days=7)
        loan2 = Loan(item2, due_date2)
        patron._loans.append(loan2)

        fees = patron.calculate_overdue_fees()
        self.assertEqual(fees, 4.0)  # Only the overdue one

    # ===== Tests for add_fee() =====

    def test_add_fee(self):
        """Test adding fee to outstanding fees"""
        patron = Patron(1, "Test User", 25, outstanding_fees=10.0)

        patron.add_fee(5.0)
        self.assertEqual(patron._outstanding_fees, 15.0)

    def test_add_fee_zero_initial(self):
        """Test adding fee when no initial fees"""
        patron = Patron(1, "Test User", 25)

        patron.add_fee(10.0)
        self.assertEqual(patron._outstanding_fees, 10.0)

    # ===== Tests for pay_fee() =====

    def test_pay_fee_partial(self):
        """Test partial fee payment"""
        patron = Patron(1, "Test User", 25, outstanding_fees=10.0)

        remaining = patron.pay_fee(3.0)

        self.assertEqual(remaining, 7.0)
        self.assertEqual(patron._outstanding_fees, 7.0)

    def test_pay_fee_full(self):
        """Test full fee payment"""
        patron = Patron(1, "Test User", 25, outstanding_fees=10.0)

        remaining = patron.pay_fee(10.0)

        self.assertEqual(remaining, 0.0)
        self.assertEqual(patron._outstanding_fees, 0.0)

    def test_pay_fee_overpayment(self):
        """Test overpayment (should not go negative)"""
        patron = Patron(1, "Test User", 25, outstanding_fees=10.0)

        remaining = patron.pay_fee(15.0)

        self.assertEqual(remaining, 0.0)
        self.assertEqual(patron._outstanding_fees, 0.0)

    # ===== Tests for __str__() =====

    def test_str_representation(self):
        """Test string representation of patron"""
        patron = Patron(1, "John Doe", 25, outstanding_fees=5.50)

        result = str(patron)

        self.assertIn("John Doe", result)
        self.assertIn("ID: 1", result)
        self.assertIn("Age: 25", result)
        self.assertIn("Loans: 0", result)
        self.assertIn("Fees: $5.50", result)

    def test_str_with_loans(self):
        """Test string representation with loans"""
        patron = Patron(1, "Jane Doe", 30, outstanding_fees=0.0)
        item = BorrowableItem(1, "Test Book", "Fiction Book")
        patron.add_loan(item)

        result = str(patron)

        self.assertIn("Loans: 1", result)

    # ===== Tests for to_full_string() =====

    def test_to_full_string_no_loans(self):
        """Test full string representation with no loans"""
        patron = Patron(1, "John Doe", 25)

        result = patron.to_full_string()

        self.assertIn("John Doe", result)
        self.assertIn("No current loans", result)

    def test_to_full_string_with_loans(self):
        """Test full string representation with loans"""
        patron = Patron(1, "Jane Doe", 30)
        item1 = BorrowableItem(1, "Book 1", "Fiction Book")
        item2 = BorrowableItem(2, "Book 2", "Non-Fiction Book")

        patron.add_loan(item1)
        patron.add_loan(item2)

        result = patron.to_full_string()

        self.assertIn("Jane Doe", result)
        self.assertIn("Current loans:", result)
        # Should contain loan information

    # ===== Tests for initialization with all parameters =====

    def test_patron_initialization_full(self):
        """Test patron initialization with all parameters"""
        patron = Patron(
            patron_id=100,
            name="Test User",
            age=35,
            outstanding_fees=25.50,
            gardening_tool_training=True,
            carpentry_tool_training=True,
            makerspace_training=True
        )

        self.assertEqual(patron._id, 100)
        self.assertEqual(patron._name, "Test User")
        self.assertEqual(patron._age, 35)
        self.assertEqual(patron._outstanding_fees, 25.50)
        self.assertTrue(patron._gardening_tool_training)
        self.assertTrue(patron._carpentry_tool_training)
        self.assertTrue(patron._makerspace_training)
        self.assertEqual(len(patron._loans), 0)

    def test_patron_initialization_defaults(self):
        """Test patron initialization with default parameters"""
        patron = Patron(1, "Test User", 25)

        self.assertEqual(patron._outstanding_fees, 0.0)
        self.assertFalse(patron._gardening_tool_training)
        self.assertFalse(patron._carpentry_tool_training)
        self.assertFalse(patron._makerspace_training)


if __name__ == '__main__':
    unittest.main()
