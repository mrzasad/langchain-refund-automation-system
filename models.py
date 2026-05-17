from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DateExtraction(BaseModel):
    """Extracted dates from complaint ticket"""
    delivery_date: str = Field(..., description="Delivery date in YYYY-MM-DD format")
    claim_date: str = Field(..., description="Claim date in YYYY-MM-DD format")

class RefundDecision(BaseModel):
    """Refund decision details"""
    customer_name: str = Field(..., description="Customer name")
    order_id: str = Field(..., description="Order ID")
    delivery_date: str = Field(..., description="Delivery date")
    claim_date: str = Field(..., description="Claim date")
    days_lapsed: int = Field(..., description="Number of days between delivery and claim")
    decision: str = Field(..., description="APPROVED or REJECTED")
    reason: str = Field(..., description="Reason for decision")
    policy_days: int = Field(..., description="Refund policy days")

class ComplaintTicket(BaseModel):
    """Customer complaint ticket structure"""
    customer_name: str
    order_id: str
    complaint_text: str
    complaint_date: str