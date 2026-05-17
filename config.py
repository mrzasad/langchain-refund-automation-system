import os
from dotenv import load_dotenv

load_dotenv()

# LLM Configuration
LLM_MODEL = "gpt-3.5-turbo"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Refund Policy
REFUND_POLICY_DAYS = 30  # Days within which refund claim must be submitted

# Prompts
EXTRACTION_PROMPT = """Extract the delivery date and claim date from the following customer complaint ticket.
Return the dates in YYYY-MM-DD format.

Complaint Ticket:
{complaint_text}

Provide the response in this exact format:
DELIVERY_DATE: YYYY-MM-DD
CLAIM_DATE: YYYY-MM-DD
"""

EMAIL_GENERATION_PROMPT = """Generate a professional email response for a customer refund {decision}.

Details:
- Customer Name: {customer_name}
- Order ID: {order_id}
- Delivery Date: {delivery_date}
- Claim Date: {claim_date}
- Days Lapsed: {days_lapsed}
- Refund Policy: Refunds are allowed only within {policy_days} days of delivery
- Decision: {decision}
- Reason: {reason}

Write a professional, empathetic email that explains the decision clearly and factually."""