import streamlit as st
import pandas as pd
from datetime import datetime
from typing import List, Dict
import sys

# LangChain imports
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

# Local imports
from models import DateExtraction, RefundDecision, ComplaintTicket
from utils import calculate_days_lapsed, determine_refund_decision, validate_dates
from config import EXTRACTION_PROMPT, EMAIL_GENERATION_PROMPT, REFUND_POLICY_DAYS, OPENAI_API_KEY, LLM_MODEL

# Page Configuration
st.set_page_config(
    page_title="Refund Automation System",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🤖 Refund Automation System")
st.markdown("---")

# Initialize session state
if "results_df" not in st.session_state:
    st.session_state.results_df = None
if "emails" not in st.session_state:
    st.session_state.emails = {}

# Sidebar Configuration
st.sidebar.header("⚙️ Configuration")
policy_days = st.sidebar.number_input(
    "Refund Policy Days",
    min_value=1,
    max_value=365,
    value=REFUND_POLICY_DAYS
)

st.sidebar.markdown("---")
st.sidebar.info(
    f"**Policy**: Refunds are allowed only within {policy_days} days of delivery date."
)

# Main Content
tab1, tab2, tab3 = st.tabs(["📊 Data Input", "⚙️ Processing", "📧 Email Generation"])

# ============================================================================
# TAB 1: DATA INPUT
# ============================================================================
with tab1:
    st.header("Step 1: Load Customer Complaint Data")
    
    upload_col, template_col = st.columns(2)
    
    with upload_col:
        st.subheader("Upload Excel File")
        uploaded_file = st.file_uploader(
            "Upload customer complaints (Excel format)",
            type=["xlsx", "xls"],
            help="Columns should include: customer_name, order_id, complaint_text, complaint_date"
        )
        
        if uploaded_file:
            try:
                df = pd.read_excel(uploaded_file)
                st.session_state.input_df = df
                
                st.success(f"✅ Loaded {len(df)} complaint tickets")
                st.subheader("Data Preview")
                st.dataframe(df, use_container_width=True, height=400)
                
                # Display data info
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Tickets", len(df))
                col2.metric("Columns", len(df.columns))
                col3.metric("Date Loaded", datetime.now().strftime("%Y-%m-%d %H:%M"))
                
            except Exception as e:
                st.error(f"❌ Error loading file: {str(e)}")
    
    with template_col:
        st.subheader("Sample Data Template")
        sample_data = {
            "customer_name": ["John Doe", "Jane Smith"],
            "order_id": ["ORD-001", "ORD-002"],
            "complaint_text": [
                "Order delivered on 2026-04-01. Received damaged product on 2026-04-05. Requesting refund.",
                "Item delivered on 2026-04-10. Quality issues found. Submitted claim on 2026-05-15."
            ],
            "complaint_date": ["2026-04-05", "2026-05-15"]
        }
        sample_df = pd.DataFrame(sample_data)
        st.dataframe(sample_df, use_container_width=True, height=300)
        
        # Download template
        csv = sample_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Template",
            data=csv,
            file_name="complaint_template.csv",
            mime="text/csv"
        )

# ============================================================================
# TAB 2: PROCESSING
# ============================================================================
with tab2:
    st.header("Step 2: Process Complaints & Extract Dates")
    
    if "input_df" not in st.session_state:
        st.warning("⚠️ Please upload data in the 'Data Input' tab first")
    else:
        st.subheader(f"Processing {len(st.session_state.input_df)} Tickets")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            if st.button("🚀 Start Processing", key="process_btn"):
                st.session_state.processing = True
        
        if st.session_state.get("processing"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Initialize LLM
            try:
                llm = ChatOpenAI(
                    model=LLM_MODEL,
                    api_key=OPENAI_API_KEY,
                    temperature=0
                )
                
                # Initialize Pydantic Parser
                parser = PydanticOutputParser(pydantic_object=DateExtraction)
                
                # Create Prompt Template
                prompt = PromptTemplate(
                    template=EXTRACTION_PROMPT,
                    input_variables=["complaint_text"],
                    partial_variables={"format_instructions": parser.get_format_instructions()}
                )
                
                # Build LCEL Chain (RunnableSequence)
                chain = prompt | llm | parser
                
                results = []
                df = st.session_state.input_df
                
                for idx, row in df.iterrows():
                    # Update progress
                    progress = (idx + 1) / len(df)
                    progress_bar.progress(progress)
                    status_text.text(f"Processing: {idx + 1}/{len(df)} - {row['customer_name']}")
                    
                    try:
                        # Extract dates using LLM
                        extraction_result = chain.invoke({
                            "complaint_text": row['complaint_text']
                        })
                        
                        delivery_date = extraction_result.delivery_date
                        claim_date = extraction_result.claim_date
                        
                        # Validate dates
                        if not validate_dates(delivery_date, claim_date):
                            raise ValueError("Invalid date format extracted")
                        
                        # Calculate days lapsed
                        days_lapsed = calculate_days_lapsed(delivery_date, claim_date)
                        
                        # Determine refund decision
                        decision, reason = determine_refund_decision(days_lapsed, policy_days)
                        
                        results.append({
                            "customer_name": row['customer_name'],
                            "order_id": row['order_id'],
                            "complaint_text": row['complaint_text'],
                            "delivery_date": delivery_date,
                            "claim_date": claim_date,
                            "days_lapsed": days_lapsed,
                            "decision": decision,
                            "reason": reason,
                            "policy_days": policy_days
                        })
                        
                    except Exception as e:
                        st.warning(f"⚠️ Error processing {row['customer_name']}: {str(e)}")
                        results.append({
                            "customer_name": row['customer_name'],
                            "order_id": row['order_id'],
                            "complaint_text": row['complaint_text'],
                            "delivery_date": "ERROR",
                            "claim_date": "ERROR",
                            "days_lapsed": 0,
                            "decision": "MANUAL_REVIEW",
                            "reason": str(e),
                            "policy_days": policy_days
                        })
                
                # Create results dataframe
                st.session_state.results_df = pd.DataFrame(results)
                
                status_text.text("✅ Processing Complete!")
                st.success("All tickets processed successfully!")
                st.session_state.processing = False
                
            except Exception as e:
                st.error(f"❌ Error initializing LLM: {str(e)}")
                st.info("Make sure OPENAI_API_KEY is set in your environment")
        
        # Display Results
        if st.session_state.results_df is not None:
            st.markdown("---")
            st.subheader("📋 Processing Results")
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            df_results = st.session_state.results_df
            approved = len(df_results[df_results['decision'] == 'APPROVED'])
            rejected = len(df_results[df_results['decision'] == 'REJECTED'])
            manual = len(df_results[df_results['decision'] == 'MANUAL_REVIEW'])
            
            col1.metric("Total Processed", len(df_results))
            col2.metric("Approved ✅", approved, delta=f"{(approved/len(df_results)*100):.1f}%")
            col3.metric("Rejected ❌", rejected, delta=f"{(rejected/len(df_results)*100):.1f}%")
            col4.metric("Manual Review 🔍", manual)
            
            # Display results table
            st.dataframe(
                df_results[[
                    "customer_name", "order_id", "delivery_date", 
                    "claim_date", "days_lapsed", "decision"
                ]],
                use_container_width=True,
                height=400
            )
            
            # Display detailed results
            with st.expander("📊 View Detailed Analysis"):
                st.dataframe(df_results, use_container_width=True)
            
            # Download results
            csv_results = df_results.to_csv(index=False)
            st.download_button(
                label="📥 Download Results (CSV)",
                data=csv_results,
                file_name=f"refund_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

# ============================================================================
# TAB 3: EMAIL GENERATION
# ============================================================================
with tab3:
    st.header("Step 3: Generate Response Emails")
    
    if st.session_state.results_df is None:
        st.warning("⚠️ Please process complaints in the 'Processing' tab first")
    else:
        st.subheader("Generate Personalized Email Responses")
        
        if st.button("📧 Generate All Emails", key="email_btn"):
            st.session_state.generating_emails = True
        
        if st.session_state.get("generating_emails"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Initialize LLM for email generation
                llm = ChatOpenAI(
                    model=LLM_MODEL,
                    api_key=OPENAI_API_KEY,
                    temperature=0.7  # Slightly higher for more creative responses
                )
                
                emails = {}
                df_results = st.session_state.results_df
                
                for idx, row in df_results.iterrows():
                    progress = (idx + 1) / len(df_results)
                    progress_bar.progress(progress)
                    status_text.text(f"Generating email: {idx + 1}/{len(df_results)}")
                    
                    try:
                        # Create email prompt
                        email_prompt = PromptTemplate(
                            template=EMAIL_GENERATION_PROMPT,
                            input_variables=[
                                "decision", "customer_name", "order_id",
                                "delivery_date", "claim_date", "days_lapsed",
                                "policy_days", "reason"
                            ]
                        )
                        
                        # Build email generation chain
                        email_chain = email_prompt | llm
                        
                        # Generate email
                        email_response = email_chain.invoke({
                            "decision": row['decision'],
                            "customer_name": row['customer_name'],
                            "order_id": row['order_id'],
                            "delivery_date": row['delivery_date'],
                            "claim_date": row['claim_date'],
                            "days_lapsed": row['days_lapsed'],
                            "policy_days": row['policy_days'],
                            "reason": row['reason']
                        })
                        
                        emails[row['order_id']] = email_response.content
                        
                    except Exception as e:
                        emails[row['order_id']] = f"Error generating email: {str(e)}"
                
                st.session_state.emails = emails
                status_text.text("✅ Email generation complete!")
                st.success("All emails generated successfully!")
                st.session_state.generating_emails = False
                
            except Exception as e:
                st.error(f"❌ Error generating emails: {str(e)}")
        
        # Display Generated Emails
        if st.session_state.emails:
            st.markdown("---")
            st.subheader("📧 Generated Emails")
            
            df_results = st.session_state.results_df
            
            for idx, row in df_results.iterrows():
                order_id = row['order_id']
                if order_id in st.session_state.emails:
                    with st.expander(f"{order_id} - {row['customer_name']} ({row['decision']})"):
                        st.markdown(f"**Subject:** Refund Decision - Order {order_id}")
                        st.markdown(f"**Decision:** {row['decision']}")
                        st.markdown(f"**Delivery Date:** {row['delivery_date']}")
                        st.markdown(f"**Claim Date:** {row['claim_date']}")
                        st.markdown(f"**Days Lapsed:** {row['days_lapsed']}")
                        st.markdown("---")
                        st.write(st.session_state.emails[order_id])
                        
                        # Copy button
                        st.text_area(
                            "Email Content",
                            value=st.session_state.emails[order_id],
                            height=200,
                            disabled=True,
                            label_visibility="collapsed"
                        )
            
            # Download all emails
            email_content = ""
            for idx, row in df_results.iterrows():
                order_id = row['order_id']
                if order_id in st.session_state.emails:
                    email_content += f"{'='*80}\n"
                    email_content += f"Order ID: {order_id}\n"
                    email_content += f"Customer: {row['customer_name']}\n"
                    email_content += f"Decision: {row['decision']}\n"
                    email_content += f"{'='*80}\n\n"
                    email_content += st.session_state.emails[order_id]
                    email_content += "\n\n"
            
            st.download_button(
                label="📥 Download All Emails",
                data=email_content,
                file_name=f"refund_emails_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 12px;'>
    <p>🤖 Refund Automation System | Powered by LangChain & OpenAI | v1.0</p>
    </div>
    """,
    unsafe_allow_html=True
)