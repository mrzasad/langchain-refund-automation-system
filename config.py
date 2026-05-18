import os
from dotenv import load_dotenv

load_dotenv()

# LLM Configuration
# Use Groq API (https://console.groq.com/)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")  # groq or openai

if LLM_PROVIDER == "groq":
    # Use configurable model, defaults to gemma-2-9b-it (actively supported)
    # Check available models at: https://console.groq.com/docs/models
    LLM_MODEL = os.getenv("GROQ_MODEL", "gemma-2-9b-it")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    API_KEY = GROQ_API_KEY
    
    # Validate API key
    if not API_KEY:
        raise ValueError(
            "GROQ_API_KEY is not set. Please set it in your .env file or as an environment variable.\n"
            "Get your key from: https://console.groq.com/"
        )
else:
    LLM_MODEL = "gpt-3.5-turbo"
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    API_KEY = OPENAI_API_KEY
    
    # Validate API key
    if not API_KEY:
        raise ValueError(
            "OPENAI_API_KEY is not set. Please set it in your .env file or as an environment variable."
        )

# Refund Policy
REFUND_POLICY_DAYS = 30  # Days within which refund claim must be submitted

# Prompts
EXTRACTION_PROMPT = """You are an expert at extracting dates from customer complaint tickets.
Extract ONLY the delivery date and claim date from the following customer complaint ticket.
Return ONLY a JSON object with the exact structure specified below - no additional text, code, explanation, or markdown.

Complaint Ticket:
{complaint_text}

{format_instructions}

IMPORTANT: 
- Return ONLY the JSON object
- Do NOT include any code, explanations, or additional text
- Do NOT wrap the JSON in markdown code blocks
- The date format must be YYYY-MM-DD
- If you cannot determine a date, return "INVALID" for that field
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