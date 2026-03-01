"""
Streamlit Web UI for Automation Auditor.
Simple interface for running code audits via web browser.
"""
import streamlit as st
from pathlib import Path
import tempfile
from datetime import datetime
from src.graph import build_audit_graph
from src.utils.rubric_loader import load_rubric
from src.state import AgentState, RubricDimension
from src.utils.config import Config


st.set_page_config(
    page_title="Automation Auditor",
    page_icon="🤖",
    layout="wide"
)

# Header
st.title("🤖 Automation Auditor")
st.markdown("**Enterprise Multi-Agent Code Review System**")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # LLM Provider Selection
    st.markdown("### LLM Provider")
    provider = st.selectbox(
        "Choose Provider",
        ["deepseek", "groq", "openai", "anthropic"],
        index=0,  # Default to DeepSeek (cheap and unlimited)
        help="Select which LLM provider to use for judge evaluations"
    )
    
    # Update config based on selection (override .env)
    Config.LLM_PROVIDER = provider
    
    # Validate API key for selected provider
    api_key_valid = False
    if provider == "groq" and Config.GROQ_API_KEY:
        api_key_valid = True
    elif provider == "deepseek" and Config.DEEPSEEK_API_KEY:
        api_key_valid = True
    elif provider == "openai" and Config.OPENAI_API_KEY:
        api_key_valid = True
    elif provider == "anthropic" and Config.ANTHROPIC_API_KEY:
        api_key_valid = True
    
    if not api_key_valid:
        st.error(f"❌ {provider.upper()} API key not configured! Please add to .env file.")
    
    # Show provider info
    provider_info = {
        "groq": "🚀 Fast & Free (100K tokens/day limit)",
        "deepseek": "💰 Cheap & Unlimited ($0.02/audit)",
        "openai": "🔥 Premium ($0.50/audit)",
        "anthropic": "🧠 Advanced ($0.40/audit)"
    }
    st.info(provider_info.get(provider, "Selected provider"))
    
    st.markdown("---")
    st.markdown("### System Status")
    
    # Check API keys (Config already imported at top)
    
    groq_status = "✅" if Config.GROQ_API_KEY else "❌"
    deepseek_status = "✅" if Config.DEEPSEEK_API_KEY else "❌"
    google_status = "✅" if Config.GOOGLE_API_KEY else "❌"
    openai_status = "✅" if Config.OPENAI_API_KEY else "❌"
    
    st.markdown(f"**Groq API**: {groq_status}")
    st.markdown(f"**DeepSeek API**: {deepseek_status}")
    st.markdown(f"**OpenAI API**: {openai_status}")
    st.markdown(f"**Google API**: {google_status}")
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    This system uses:
    - **3 Detective Agents** (parallel)
    - **3 Judge Agents** (dialectical)
    - **1 Chief Justice** (synthesis)
    
    **Cost**: $0 (free tiers)
    """)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📦 Repository Input")
    repo_url = st.text_input(
        "GitHub Repository URL",
        value="https://github.com/IbnuEyni/10Acweek2",  # Pre-fill with your repo
        placeholder="https://github.com/username/repository",
        help="Enter the GitHub repository URL to audit (without .git suffix)"
    )
    
    # Normalize URL (remove .git suffix if present)
    if repo_url and repo_url.endswith('.git'):
        repo_url = repo_url[:-4]
        st.info(f"ℹ️ Normalized URL to: {repo_url}")

with col2:
    st.header("📄 Report (Optional)")
    pdf_file = st.file_uploader(
        "Upload PDF Report",
        type=['pdf', 'md'],
        help="Optional: Upload architectural report for analysis"
    )

# Run audit button
st.markdown("---")

if st.button("🚀 Run Audit", type="primary", use_container_width=True):
    if not repo_url:
        st.error("❌ Please enter a GitHub repository URL")
    else:
        # Create progress indicators
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Save uploaded PDF if provided
            pdf_path = "temp_report.pdf"
            if pdf_file:
                with open(pdf_path, "wb") as f:
                    f.write(pdf_file.getbuffer())
                status_text.text("📄 PDF uploaded successfully")
            else:
                # Create dummy PDF path
                pdf_path = "reports/interim_report.md"
            
            progress_bar.progress(10)
            status_text.text("⚖️ Loading evaluation rubric...")
            
            # Load rubric
            rubric = load_rubric()
            dimensions = [RubricDimension(**d) for d in rubric["dimensions"]]
            
            progress_bar.progress(20)
            status_text.text("🔧 Building audit graph...")
            
            # Initialize state
            initial_state: AgentState = {
                "repo_url": repo_url,
                "pdf_path": pdf_path,
                "rubric_dimensions": dimensions,
                "evidences": {},
                "opinions": [],
                "final_report": "",
                "errors": []
            }
            
            # Build graph
            graph = build_audit_graph()
            
            progress_bar.progress(30)
            status_text.text("🔍 Detective Layer: Collecting evidence...")
            
            # Execute audit
            with st.spinner("Running audit pipeline..."):
                result = graph.invoke(initial_state)
            
            progress_bar.progress(100)
            status_text.text("✅ Audit complete!")
            
            # Save report to disk
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = Path("audit/streamlit_runs")
            output_dir.mkdir(parents=True, exist_ok=True)
            report_path = output_dir / f"audit_report_{timestamp}.md"
            report_path.write_text(result["final_report"])
            st.info(f"📁 Report saved to: {report_path}")
            
            # Display results
            st.markdown("---")
            st.success("🎉 Audit completed successfully!")
            
            # Statistics
            col1, col2, col3, col4 = st.columns(4)
            
            evidence_count = sum(len(v) for v in result.get("evidences", {}).values())
            opinion_count = len(result.get("opinions", []))
            error_count = len(result.get("errors", []))
            report_size = len(result.get("final_report", ""))
            
            with col1:
                st.metric("Evidence Collected", evidence_count)
            with col2:
                st.metric("Judicial Opinions", opinion_count)
            with col3:
                st.metric("Report Size", f"{report_size:,} chars")
            with col4:
                st.metric("Errors", error_count)
            
            # Display report
            st.markdown("---")
            st.header("📋 Audit Report")
            
            # Create tabs for different views
            tab1, tab2, tab3 = st.tabs(["📄 Full Report", "📊 Evidence", "⚖️ Opinions"])
            
            with tab1:
                st.markdown(result["final_report"])
                
                # Download button
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                st.download_button(
                    label="⬇️ Download Report",
                    data=result["final_report"],
                    file_name=f"audit_report_{timestamp}.md",
                    mime="text/markdown"
                )
            
            with tab2:
                st.subheader("Evidence Collected")
                evidences = result.get("evidences", {})
                
                for category, evidence_list in evidences.items():
                    with st.expander(f"📌 {category} ({len(evidence_list)} items)"):
                        for evidence in evidence_list:
                            st.markdown(f"**Goal**: {evidence.goal}")
                            st.markdown(f"**Found**: {'✅ Yes' if evidence.found else '❌ No'}")
                            st.markdown(f"**Confidence**: {evidence.confidence:.2%}")
                            st.markdown(f"**Rationale**: {evidence.rationale}")
                            st.markdown(f"**Location**: `{evidence.location}`")
                            if evidence.content:
                                st.code(evidence.content[:200] + "..." if len(evidence.content) > 200 else evidence.content)
                            st.markdown("---")
            
            with tab3:
                st.subheader("Judicial Opinions")
                opinions = result.get("opinions", [])
                
                # Group by criterion
                from collections import defaultdict
                opinions_by_criterion = defaultdict(list)
                for opinion in opinions:
                    opinions_by_criterion[opinion.criterion_id].append(opinion)
                
                for criterion_id, criterion_opinions in opinions_by_criterion.items():
                    with st.expander(f"⚖️ {criterion_id}"):
                        for opinion in criterion_opinions:
                            judge_emoji = {
                                "Prosecutor": "⚖️",
                                "Defense": "🛡️",
                                "TechLead": "🔧"
                            }
                            
                            st.markdown(f"### {judge_emoji.get(opinion.judge, '👨‍⚖️')} {opinion.judge}")
                            st.metric("Score", f"{opinion.score}/5")
                            st.markdown(f"**Argument**: {opinion.argument}")
                            if opinion.cited_evidence:
                                st.markdown(f"**Evidence**: {', '.join(opinion.cited_evidence[:3])}")
                            st.markdown("---")
            
            # Errors (if any)
            if error_count > 0:
                st.warning(f"⚠️ {error_count} errors encountered during audit")
                with st.expander("View Errors"):
                    for error in result["errors"]:
                        st.error(error)
        
        except Exception as e:
            progress_bar.progress(0)
            status_text.text("")
            st.error(f"❌ Audit failed: {str(e)}")
            st.exception(e)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Automation Auditor v1.0 | Enterprise Multi-Agent Code Review System</p>
    <p>Powered by LangGraph, Groq Llama 3.3, and Gemini 2.5 Flash</p>
</div>
""", unsafe_allow_html=True)
