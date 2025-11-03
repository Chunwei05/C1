"""
Discount calculation module for testing purposes.

This module provides discount calculation functionality to be tested
using Equivalence Partitioning and Boundary Value Analysis techniques.
"""


def calculate_discount(price, discount_percentage):
    """
    Calculate the discounted price based on original price and discount percentage.

    Args:
        price (float): Original price of the item
        discount_percentage (float): Discount percentage (0-100)

    Returns:
        float: Price after applying discount

    Raises:
        ValueError: If discount_percentage is negative or greater than 100
        ValueError: If price is negative
    """
    if price < 0:
        raise ValueError("Price cannot be negative")

    if discount_percentage < 0:
        raise ValueError("Discount percentage cannot be negative")

    if discount_percentage > 100:
        raise ValueError("Discount percentage cannot exceed 100")

    discount_amount = price * (discount_percentage / 100)
    return price - discount_amount
