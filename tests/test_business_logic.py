"""
Comprehensive tests for business_logic.py to achieve high coverage.
Tests all methods in BusinessLogic class with various conditions.
"""

import unittest
from datetime import datetime, timedelta
from src.business_logic import BusinessLogic
from src.patron import Patron
from src.borrowable_item import BorrowableItem
from src.loan import Loan


class TestBusinessLogic(unittest.TestCase):
    """Test suite for BusinessLogic class"""

    def setUp(self):
        """Set up test fixtures"""
        self.business_logic = BusinessLogic()

    # ===== Tests for check_loan_allowed() =====

    def test_check_loan_allowed_invalid_item(self):
        """Test with invalid item type"""
        patron = Patron(1, "Test User", 25)
        result, reason = self.business_logic.check_loan_allowed(patron, "not_an_item")
        self.assertFalse(result)
        self.assertEqual(reason, "Invalid item")

    def test_check_loan_allowed_no_copies_available(self):
        """Test when no copies available"""
        patron = Patron(1, "Test User", 25)
        item = BorrowableItem(1, "Test Book", "Fiction Book", num_copies=2, on_loan=2)
        result, reason = self.business_logic.check_loan_allowed(patron, item)
        self.assertFalse(result)
        self.assertEqual(reason, "No copies available")

    def test_check_loan_allowed_minor_loan_limit(self):
        """Test Minor patron loan limit (3 loans)"""
        patron = Patron(1, "Minor User", 15)
        item = BorrowableItem(1, "Test Book", "Fiction Book")

        # Add 3 loans to reach limit
        for i in range(3):
            loan_item = BorrowableItem(i+10, f"Book {i}", "Fiction Book")
            patron.add_loan(loan_item, 14)

        result, reason = self.business_logic.check_loan_allowed(patron, item)
        self.assertFalse(result)
        self.assertEqual(reason, "Loan limit reached for Minor")

    def test_check_loan_allowed_regular_loan_limit(self):
        """Test Regular patron loan limit (5 loans)"""
        patron = Patron(1, "Regular User", 25)
        item = BorrowableItem(1, "Test Book", "Fiction Book")

        # Add 5 loans to reach limit
        for i in range(5):
            loan_item = BorrowableItem(i+10, f"Book {i}", "Fiction Book")
            patron.add_loan(loan_item, 14)

        result, reason = self.business_logic.check_loan_allowed(patron, item)
        self.assertFalse(result)
        self.assertEqual(reason, "Loan limit reached for Regular")

    def test_check_loan_allowed_elderly_loan_limit(self):
        """Test Elderly patron loan limit (10 loans)"""
        patron = Patron(1, "Elderly User", 70)
        item = BorrowableItem(1, "Test Book", "Fiction Book")

        # Add 10 loans to reach limit
        for i in range(10):
            loan_item = BorrowableItem(i+10, f"Book {i}", "Fiction Book")
            patron.add_loan(loan_item, 14)

        result, reason = self.business_logic.check_loan_allowed(patron, item)
        self.assertFalse(result)
        self.assertEqual(reason, "Loan limit reached for Elderly")

    def test_check_loan_allowed_outstanding_fees(self):
        """Test patron with outstanding fees"""
        patron = Patron(1, "Test User", 25, outstanding_fees=10.0)
        item = BorrowableItem(1, "Test Book", "Fiction Book")

        result, reason = self.business_logic.check_loan_allowed(patron, item)
        self.assertFalse(result)
        self.assertEqual(reason, "Outstanding fees must be paid")

    def test_check_loan_allowed_reference_book(self):
        """Test reference book cannot be borrowed"""
        patron = Patron(1, "Test User", 25)
        item = BorrowableItem(1, "Encyclopedia", "Reference Book")

        result, reason = self.business_logic.check_loan_allowed(patron, item)
        self.assertFalse(result)
        self.assertEqual(reason, "Reference books cannot be borrowed")

    def test_check_loan_allowed_minor_gardening_tool(self):
        """Test minor cannot borrow gardening tools"""
        patron = Patron(1, "Minor User", 15, gardening_tool_training=True)
        item = BorrowableItem(1, "Shovel", "Gardening Tool")

        result, reason = self.business_logic.check_loan_allowed(patron, item)
        self.assertFalse(result)
        self.assertEqual(reason, "Minors cannot borrow tools")

    def test_check_loan_allowed_minor_carpentry_tool(self):
        """Test minor cannot borrow carpentry tools"""
        patron = Patron(1, "Minor User", 15, carpentry_tool_training=True)
        item = BorrowableItem(1, "Hammer", "Carpentry Tool")

        result, reason = self.business_logic.check_loan_allowed(patron, item)
        self.assertFalse(result)
        self.assertEqual(reason, "Minors cannot borrow tools")

    def test_check_loan_allowed_no_gardening_training(self):
        """Test adult without gardening training"""
        patron = Patron(1, "Test User", 25, gardening_tool_training=False)
        item = BorrowableItem(1, "Shovel", "Gardening Tool")

        result, reason = self.business_logic.check_loan_allowed(patron, item)
        self.assertFalse(result)
        self.assertEqual(reason, "Gardening tool training required")

    def test_check_loan_allowed_no_carpentry_training(self):
        """Test adult without carpentry training"""
        patron = Patron(1, "Test User", 25, carpentry_tool_training=False)
        item = BorrowableItem(1, "Hammer", "Carpentry Tool")

        result, reason = self.business_logic.check_loan_allowed(patron, item)
        self.assertFalse(result)
        self.assertEqual(reason, "Carpentry tool training required")

    def test_check_loan_allowed_duplicate_item_type(self):
        """Test patron already has same item type on loan"""
        patron = Patron(1, "Test User", 25)
        existing_item = BorrowableItem(1, "Book 1", "Fiction Book")
        new_item = BorrowableItem(2, "Book 2", "Fiction Book")

        patron.add_loan(existing_item, 14)

        result, reason = self.business_logic.check_loan_allowed(patron, new_item)
        self.assertFalse(result)
        self.assertEqual(reason, "Already have a Fiction Book on loan")

    def test_check_loan_allowed_laptop_zero_period(self):
        """Test laptop with zero loan period"""
        patron = Patron(1, "Test User", 25)
        item = BorrowableItem(1, "Laptop", "Laptop")

        # This tests the specific item restrictions branch
        # Laptop has loan_period=3, so it should be allowed
        result, reason = self.business_logic.check_loan_allowed(patron, item)
        self.assertTrue(result)
        self.assertEqual(reason, "Loan allowed")

    def test_check_loan_allowed_success_fiction_book(self):
        """Test successful loan of fiction book"""
        patron = Patron(1, "Test User", 25)
        item = BorrowableItem(1, "Test Book", "Fiction Book")

        result, reason = self.business_logic.check_loan_allowed(patron, item)
        self.assertTrue(result)
        self.assertEqual(reason, "Loan allowed")

    def test_check_loan_allowed_success_gardening_tool(self):
        """Test successful loan of gardening tool"""
        patron = Patron(1, "Test User", 25, gardening_tool_training=True)
        item = BorrowableItem(1, "Shovel", "Gardening Tool")

        result, reason = self.business_logic.check_loan_allowed(patron, item)
        self.assertTrue(result)
        self.assertEqual(reason, "Loan allowed")

    def test_check_loan_allowed_success_carpentry_tool(self):
        """Test successful loan of carpentry tool"""
        patron = Patron(1, "Test User", 25, carpentry_tool_training=True)
        item = BorrowableItem(1, "Hammer", "Carpentry Tool")

        result, reason = self.business_logic.check_loan_allowed(patron, item)
        self.assertTrue(result)
        self.assertEqual(reason, "Loan allowed")

    # ===== Tests for _get_loan_period() =====

    def test_get_loan_period_fiction_book(self):
        """Test loan period for fiction book"""
        period = self.business_logic._get_loan_period("Fiction Book")
        self.assertEqual(period, 21)

    def test_get_loan_period_nonfiction_book(self):
        """Test loan period for non-fiction book"""
        period = self.business_logic._get_loan_period("Non-Fiction Book")
        self.assertEqual(period, 21)

    def test_get_loan_period_magazine(self):
        """Test loan period for magazine"""
        period = self.business_logic._get_loan_period("Magazine")
        self.assertEqual(period, 7)

    def test_get_loan_period_dvd(self):
        """Test loan period for DVD"""
        period = self.business_logic._get_loan_period("DVD")
        self.assertEqual(period, 7)

    def test_get_loan_period_laptop(self):
        """Test loan period for laptop"""
        period = self.business_logic._get_loan_period("Laptop")
        self.assertEqual(period, 3)

    def test_get_loan_period_study_room(self):
        """Test loan period for study room"""
        period = self.business_logic._get_loan_period("Study Room")
        self.assertEqual(period, 1)

    def test_get_loan_period_gardening_tool(self):
        """Test loan period for gardening tool"""
        period = self.business_logic._get_loan_period("Gardening Tool")
        self.assertEqual(period, 14)

    def test_get_loan_period_carpentry_tool(self):
        """Test loan period for carpentry tool"""
        period = self.business_logic._get_loan_period("Carpentry Tool")
        self.assertEqual(period, 14)

    def test_get_loan_period_unknown_type(self):
        """Test loan period for unknown item type (default)"""
        period = self.business_logic._get_loan_period("Unknown Type")
        self.assertEqual(period, 14)

    # ===== Tests for process_loan() =====

    def test_process_loan_not_allowed(self):
        """Test process_loan when loan is not allowed"""
        patron = Patron(1, "Test User", 25, outstanding_fees=10.0)
        item = BorrowableItem(1, "Test Book", "Fiction Book")

        success, message = self.business_logic.process_loan(patron, item)
        self.assertFalse(success)
        self.assertEqual(message, "Outstanding fees must be paid")

    def test_process_loan_success(self):
        """Test successful loan processing"""
        patron = Patron(1, "Test User", 25)
        item = BorrowableItem(1, "Test Book", "Fiction Book")

        initial_loan_count = len(patron._loans)
        initial_on_loan = item._on_loan

        success, message = self.business_logic.process_loan(patron, item)

        self.assertTrue(success)
        self.assertEqual(message, "Loan successful. Due in 21 days.")
        self.assertEqual(len(patron._loans), initial_loan_count + 1)
        self.assertEqual(item._on_loan, initial_on_loan + 1)

    # ===== Tests for check_return_allowed() =====

    def test_check_return_allowed_item_not_on_loan(self):
        """Test return when patron doesn't have the item"""
        patron = Patron(1, "Test User", 25)

        result, reason = self.business_logic.check_return_allowed(patron, 999)
        self.assertFalse(result)
        self.assertEqual(reason, "Item not on loan to this patron")

    def test_check_return_allowed_success(self):
        """Test successful return check"""
        patron = Patron(1, "Test User", 25)
        item = BorrowableItem(1, "Test Book", "Fiction Book")
        patron.add_loan(item, 14)

        result, reason = self.business_logic.check_return_allowed(patron, 1)
        self.assertTrue(result)
        self.assertEqual(reason, "Return allowed")

    # ===== Tests for process_return() =====

    def test_process_return_not_allowed(self):
        """Test return when not allowed"""
        patron = Patron(1, "Test User", 25)

        success, message, fees = self.business_logic.process_return(patron, 999)
        self.assertFalse(success)
        self.assertEqual(message, "Item not on loan to this patron")
        self.assertEqual(fees, 0.0)

    def test_process_return_no_fees(self):
        """Test return with no overdue fees"""
        patron = Patron(1, "Test User", 25)
        item = BorrowableItem(1, "Test Book", "Fiction Book")
        patron.add_loan(item, 14)  # Due in future

        success, message, fees = self.business_logic.process_return(patron, 1)
        self.assertTrue(success)
        self.assertEqual(message, "Return successful. No fees.")
        self.assertEqual(fees, 0.0)

    def test_process_return_with_fees(self):
        """Test return with overdue fees"""
        patron = Patron(1, "Test User", 25)
        item = BorrowableItem(1, "Test Book", "Fiction Book")

        # Create overdue loan (due 5 days ago)
        due_date = datetime.now().date() - timedelta(days=5)
        loan = Loan(item, due_date)
        patron._loans.append(loan)
        item._on_loan += 1

        initial_fees = patron._outstanding_fees

        success, message, fees = self.business_logic.process_return(patron, 1)
        self.assertTrue(success)
        self.assertEqual(fees, 5.0)
        self.assertIn("Overdue fee:", message)
        self.assertEqual(patron._outstanding_fees, initial_fees + 5.0)

    # ===== Tests for check_makerspace_access() =====

    def test_check_makerspace_access_under_18(self):
        """Test makerspace access for patron under 18"""
        patron = Patron(1, "Minor User", 15, makerspace_training=True)

        result, reason = self.business_logic.check_makerspace_access(patron)
        self.assertFalse(result)
        self.assertEqual(reason, "Must be 18 or older to access makerspace")

    def test_check_makerspace_access_no_training(self):
        """Test makerspace access without training"""
        patron = Patron(1, "Test User", 25, makerspace_training=False)

        result, reason = self.business_logic.check_makerspace_access(patron)
        self.assertFalse(result)
        self.assertEqual(reason, "Makerspace training required")

    def test_check_makerspace_access_success(self):
        """Test successful makerspace access"""
        patron = Patron(1, "Test User", 25, makerspace_training=True)

        result, reason = self.business_logic.check_makerspace_access(patron)
        self.assertTrue(result)
        self.assertEqual(reason, "Access granted")


if __name__ == '__main__':
    unittest.main()
