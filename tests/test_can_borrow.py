"""
Test suite for library borrowing eligibility functionality.

This module tests the can_borrow function using Pairwise Testing technique.

Parameters to be tested:
- member_type: "student", "staff", "public" (3 values)
- books_borrowed: 0, 5, 10 (3 values)
- has_overdue: True, False (2 values)

Total possible combinations: 3 × 3 × 2 = 18
Pairwise testing reduces this to 9 test cases while covering all pairs.

Author: Test Suite for FIT2107 Assignment
"""

import unittest
import sys
import os

# Add src directory to path to import library module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from library import can_borrow


class TestCanBorrow(unittest.TestCase):
    """
    Test class for library borrowing eligibility using Pairwise Testing technique.

    This test suite covers all pairwise combinations of the three parameters:
    - member_type × books_borrowed
    - member_type × has_overdue
    - books_borrowed × has_overdue
    """

    def test_pairwise_combination_1(self):
        """
        Test pairwise combination 1:
        member_type="student", books_borrowed=0, has_overdue=False
        Expected: True (student with 0 books and no overdue can borrow)
        """
        result = can_borrow("student", 0, False)
        self.assertTrue(result)

    def test_pairwise_combination_2(self):
        """
        Test pairwise combination 2:
        member_type="student", books_borrowed=5, has_overdue=True
        Expected: False (has overdue books)
        """
        result = can_borrow("student", 5, True)
        self.assertFalse(result)

    def test_pairwise_combination_3(self):
        """
        Test pairwise combination 3:
        member_type="student", books_borrowed=10, has_overdue=False
        Expected: False (student exceeded limit of 5 books)
        """
        result = can_borrow("student", 10, False)
        self.assertFalse(result)

    def test_pairwise_combination_4(self):
        """
        Test pairwise combination 4:
        member_type="staff", books_borrowed=0, has_overdue=True
        Expected: False (has overdue books)
        """
        result = can_borrow("staff", 0, True)
        self.assertFalse(result)

    def test_pairwise_combination_5(self):
        """
        Test pairwise combination 5:
        member_type="staff", books_borrowed=5, has_overdue=False
        Expected: True (staff with 5 books and no overdue can borrow)
        """
        result = can_borrow("staff", 5, False)
        self.assertTrue(result)

    def test_pairwise_combination_6(self):
        """
        Test pairwise combination 6:
        member_type="staff", books_borrowed=10, has_overdue=True
        Expected: False (has overdue books)
        """
        result = can_borrow("staff", 10, True)
        self.assertFalse(result)

    def test_pairwise_combination_7(self):
        """
        Test pairwise combination 7:
        member_type="public", books_borrowed=0, has_overdue=True
        Expected: False (has overdue books)
        """
        result = can_borrow("public", 0, True)
        self.assertFalse(result)

    def test_pairwise_combination_8(self):
        """
        Test pairwise combination 8:
        member_type="public", books_borrowed=5, has_overdue=False
        Expected: False (public member exceeded limit of 3 books)
        """
        result = can_borrow("public", 5, False)
        self.assertFalse(result)

    def test_pairwise_combination_9(self):
        """
        Test pairwise combination 9:
        member_type="public", books_borrowed=10, has_overdue=False
        Expected: False (public member exceeded limit of 3 books)
        """
        result = can_borrow("public", 10, False)
        self.assertFalse(result)

    # ========== Additional Edge Case Tests ==========

    def test_pairwise_boundary_student_at_limit(self):
        """
        Test boundary case:
        member_type="student", books_borrowed=4, has_overdue=False
        Expected: True (student with 4 books can borrow one more, limit is 5)
        """
        result = can_borrow("student", 4, False)
        self.assertTrue(result)

    def test_pairwise_boundary_staff_at_limit(self):
        """
        Test boundary case:
        member_type="staff", books_borrowed=9, has_overdue=False
        Expected: True (staff with 9 books can borrow one more, limit is 10)
        """
        result = can_borrow("staff", 9, False)
        self.assertTrue(result)

    def test_pairwise_boundary_public_at_limit(self):
        """
        Test boundary case:
        member_type="public", books_borrowed=2, has_overdue=False
        Expected: True (public member with 2 books can borrow one more, limit is 3)
        """
        result = can_borrow("public", 2, False)
        self.assertTrue(result)

    def test_pairwise_invalid_member_type(self):
        """
        Test error handling:
        member_type="invalid", books_borrowed=0, has_overdue=False
        Expected: ValueError (invalid member type)
        """
        with self.assertRaises(ValueError) as context:
            can_borrow("invalid", 0, False)
        self.assertIn("Invalid member type", str(context.exception))


if __name__ == '__main__':
    unittest.main()
