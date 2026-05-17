from datetime import datetime
from typing import Tuple

def calculate_days_lapsed(delivery_date: str, claim_date: str) -> int:
    """
    Calculate the number of days between delivery date and claim date.
    
    Args:
        delivery_date: Date in YYYY-MM-DD format
        claim_date: Date in YYYY-MM-DD format
    
    Returns:
        Number of days lapsed
    """
    try:
        delivery = datetime.strptime(delivery_date, "%Y-%m-%d")
        claim = datetime.strptime(claim_date, "%Y-%m-%d")
        days_lapsed = (claim - delivery).days
        return days_lapsed
    except ValueError as e:
        raise ValueError(f"Invalid date format: {e}")

def determine_refund_decision(days_lapsed: int, policy_days: int = 30) -> Tuple[str, str]:
    """
    Determine if refund should be APPROVED or REJECTED based on days lapsed.
    
    Args:
        days_lapsed: Number of days between delivery and claim
        policy_days: Days allowed for refund claim (default: 30)
    
    Returns:
        Tuple of (decision: str, reason: str)
    """
    if days_lapsed < 0:
        return "REJECTED", f"Claim date cannot be before delivery date"
    elif days_lapsed <= policy_days:
        return "APPROVED", f"Claim submitted within {policy_days} days of delivery ({days_lapsed} days lapsed)"
    else:
        return "REJECTED", f"Claim submitted {days_lapsed} days after delivery. Policy allows claims within {policy_days} days"

def validate_dates(delivery_date: str, claim_date: str) -> bool:
    """Validate date format"""
    try:
        datetime.strptime(delivery_date, "%Y-%m-%d")
        datetime.strptime(claim_date, "%Y-%m-%d")
        return True
    except ValueError:
        return False