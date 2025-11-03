"""
Library borrowing module for testing purposes.

This module provides library borrowing eligibility functionality to be tested
using Pairwise Testing technique.
"""


def can_borrow(member_type, books_borrowed, has_overdue):
    """
    Determine if a library member can borrow more books.

    Args:
        member_type (str): Type of member - "student", "staff", or "public"
        books_borrowed (int): Current number of books borrowed (0-10)
        has_overdue (bool): Whether the member has overdue books

    Returns:
        bool: True if member can borrow, False otherwise

    Business Rules:
        - Students can borrow up to 5 books
        - Staff can borrow up to 10 books
        - Public members can borrow up to 3 books
        - No one can borrow if they have overdue books
    """
    # Cannot borrow if there are overdue books
    if has_overdue:
        return False

    # Check borrowing limits based on member type
    if member_type == "student":
        return books_borrowed < 5
    elif member_type == "staff":
        return books_borrowed < 10
    elif member_type == "public":
        return books_borrowed < 3
    else:
        raise ValueError(f"Invalid member type: {member_type}")
