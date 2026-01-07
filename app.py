"""
ChronoReason Streamlit Dashboard
Interactive narrative consistency analyzer with visualization
"""

import streamlit as st
import sys
import os
from pathlib import Path
import csv
import io

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from ingestion.chunker import chunk_text
from retrieval.pathway_store import PathwayStore
from reasoning.claim_extractor import extract_claims
from reasoning.claim_validator import validate_claim
from reasoning.contradiction_score import contradiction_score
from reasoning.decision_engine import final_decision
from reasoning.timeline_builder import build_timeline
from visualization.timeline_graph import draw_timeline

# Page config
st.set_page_config(
    page_title="ChronoReason",
    page_icon="⏱️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5em;
        font-weight: bold;
        color: #0066cc;
        margin-bottom: 10px;
    }
    .metric-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "processed" not in st.session_state:
    st.session_state.processed = False
if "results" not in st.session_state:
    st.session_state.results = None

# Sidebar
with st.sidebar:
    st.title("⚙️ Configuration")
    
    mode = st.radio(
        "Select Mode:",
        ["Quick Analysis", "Detailed Analysis", "Custom Input"],
        help="Choose analysis mode"
    )
    
    st.divider()
    
    chunk_size = st.slider(
        "Chunk Size (words)",
        min_value=100,
        max_value=2000,
        value=800,
        step=100
    )
    
    overlap = st.slider(
        "Chunk Overlap (words)",
        min_value=0,
        max_value=500,
        value=100,
        step=50
    )
    
    threshold = st.slider(
        "Consistency Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.6,
        step=0.1,
        help="Score above this indicates inconsistency"
    )
    
    st.divider()
    
    st.info(
        "💡 **Tip:** Higher threshold = stricter consistency check"
    )

# Main content
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<p class="main-header">⏱️ ChronoReason</p>', unsafe_allow_html=True)
with col2:
    st.caption("v1.0 - Narrative Consistency Analyzer")

st.write(
    "Analyze narrative consistency by validating claims against evidence using "
    "semantic search and AI-powered reasoning."
)

st.divider()

# Mode: Quick Analysis
if mode == "Quick Analysis":
    st.subheader("🚀 Quick Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Backstory")
        backstory_option = st.selectbox(
            "Select sample backstory:",
            ["backstory1.txt", "backstory2.txt", "backstory3.txt"],
            label_visibility="collapsed"
        )
        
        backstory_path = Path(f"data/sample/{backstory_option}")
        if backstory_path.exists():
            with open(backstory_path) as f:
                backstory = f.read()
            st.text_area(
                "Backstory content:",
                value=backstory,
                height=300,
                disabled=True,
                label_visibility="collapsed"
            )
        else:
            st.warning(f"Sample file not found: {backstory_option}")
            backstory = ""
    
    with col2:
        st.write("### Story")
        story_path = Path("data/sample/In_search_of_the_castaways.txt")
        
        if story_path.exists():
            with open(story_path) as f:
                story_content = f.read()
            
            preview_lines = story_content.split('\n')[:20]
            preview = '\n'.join(preview_lines)
            
            st.text_area(
                "Story preview:",
                value=preview,
                height=300,
                disabled=True,
                label_visibility="collapsed"
            )
        else:
            st.warning("Story file not found")
            story_content = ""
    
    if st.button("▶️ Analyze", use_container_width=True, key="analyze_quick"):
        if backstory and story_content:
            with st.spinner("Processing..."):
                try:
                    chunks = chunk_text(story_content, chunk_size=chunk_size, overlap=overlap)
                    store = PathwayStore(chunks)
                    claims = extract_claims(backstory)
                    
                    validations = []
                    evidence_list = []
                    
                    for claim in claims:
                        evidence = store.search(claim, top_k=3)
                        evidence_list.append(evidence)
                        result = validate_claim(claim, " ".join(evidence))
                        validations.append(result)
                    
                    score = contradiction_score(validations)
                    decision = final_decision(score, threshold=threshold)
                    
                    st.session_state.results = {
                        "score": score,
                        "decision": decision,
                        "claims": claims,
                        "validations": validations,
                        "evidence": evidence_list,
                    }
                    st.session_state.processed = True
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Mode: Detailed Analysis
elif mode == "Detailed Analysis":
    st.subheader("🔬 Detailed Analysis")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.write("### Input Backstory")
        backstory = st.text_area(
            "Enter backstory:",
            height=200,
            placeholder="Paste your backstory here...",
            label_visibility="collapsed"
        )
    
    with col2:
        st.write("### Input Story")
        story_content = st.text_area(
            "Enter story:",
            height=200,
            placeholder="Paste your story here...",
            label_visibility="collapsed"
        )
    
    if st.button("▶️ Analyze", use_container_width=True, key="analyze_detailed"):
        if backstory and story_content:
            with st.spinner("Processing..."):
                try:
                    chunks = chunk_text(story_content, chunk_size=chunk_size, overlap=overlap)
                    store = PathwayStore(chunks)
                    claims = extract_claims(backstory)
                    
                    validations = []
                    evidence_list = []
                    
                    for claim in claims:
                        evidence = store.search(claim, top_k=3)
                        evidence_list.append(evidence)
                        result = validate_claim(claim, " ".join(evidence))
                        validations.append(result)
                    
                    score = contradiction_score(validations)
                    decision = final_decision(score, threshold=threshold)
                    
                    st.session_state.results = {
                        "score": score,
                        "decision": decision,
                        "claims": claims,
                        "validations": validations,
                        "evidence": evidence_list,
                    }
                    st.session_state.processed = True
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Mode: Custom Input
else:
    st.subheader("✏️ Custom Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        backstory = st.text_area(
            "Backstory (narrative to verify):",
            height=250,
            placeholder="Enter the narrative...",
        )
    
    with col2:
        story_content = st.text_area(
            "Story (evidence source):",
            height=250,
            placeholder="Enter the source text...",
        )
    
    if st.button("▶️ Analyze", use_container_width=True, key="analyze_custom"):
        if backstory and story_content:
            with st.spinner("Processing..."):
                try:
                    chunks = chunk_text(story_content, chunk_size=chunk_size, overlap=overlap)
                    store = PathwayStore(chunks)
                    claims = extract_claims(backstory)
                    
                    validations = []
                    evidence_list = []
                    
                    for claim in claims:
                        evidence = store.search(claim, top_k=3)
                        evidence_list.append(evidence)
                        result = validate_claim(claim, " ".join(evidence))
                        validations.append(result)
                    
                    score = contradiction_score(validations)
                    decision = final_decision(score, threshold=threshold)
                    
                    st.session_state.results = {
                        "score": score,
                        "decision": decision,
                        "claims": claims,
                        "validations": validations,
                        "evidence": evidence_list,
                    }
                    st.session_state.processed = True
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Results Display
if st.session_state.processed and st.session_state.results:
    st.divider()
    st.subheader("📊 Analysis Results")
    
    results = st.session_state.results
    score = results["score"]
    decision = results["decision"]
    claims = results["claims"]
    validations = results["validations"]
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Contradiction Score", f"{score:.2%}")
    
    with col2:
        consistency = "✅ CONSISTENT" if decision == 1 else "❌ INCONSISTENT"
        st.metric("Result", consistency)
    
    with col3:
        st.metric("Claims", len(claims))
    
    with col4:
        contradictions = sum(1 for v in validations if v == "contradict")
        st.metric("Contradictions", contradictions)
    
    st.divider()
    
    # Detailed analysis
    st.subheader("📋 Claim Analysis")
    
    for i, (claim, validation) in enumerate(zip(claims, validations), 1):
        with st.expander(f"Claim {i}: {claim[:60]}..."):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**Claim:** {claim}")
                if "evidence" in results and i-1 < len(results["evidence"]):
                    st.write("**Evidence:**")
                    for ev in results["evidence"][i-1]:
                        st.caption(f"• {ev[:100]}...")
            
            with col2:
                if validation == "support":
                    st.success(f"✅ {validation.upper()}")
                elif validation == "contradict":
                    st.error(f"❌ {validation.upper()}")
                else:
                    st.warning(f"⚠️ {validation.upper()}")
    
    st.divider()
    
    # Statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Validation Breakdown")
        validation_counts = {
            "Support": sum(1 for v in validations if v == "support"),
            "Contradict": sum(1 for v in validations if v == "contradict"),
            "Neutral": sum(1 for v in validations if v == "neutral")
        }
        
        for label, count in validation_counts.items():
            pct = (count / len(validations) * 100) if validations else 0
            st.write(f"{label}: {count} ({pct:.1f}%)")
    
    with col2:
        st.write("### Interpretation")
        if score < 0.3:
            st.success("✅ **Highly Consistent**")
        elif score < 0.6:
            st.info("ℹ️ **Mostly Consistent**")
        elif score < threshold:
            st.warning("⚠️ **Moderately Inconsistent**")
        else:
            st.error("❌ **Highly Inconsistent**")
    
    st.divider()
    
    # Export
    st.subheader("📥 Export")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow(["Claim", "Validation"])
        for claim, validation in zip(claims, validations):
            writer.writerow([claim[:100], validation])
        
        st.download_button(
            label="📊 CSV",
            data=csv_buffer.getvalue(),
            file_name="chronoreason_results.csv",
            mime="text/csv"
        )
    
    with col2:
        text_export = f"""ChronoReason Results
Score: {score:.2%}
Status: {"CONSISTENT" if decision == 1 else "INCONSISTENT"}

Claims: {len(claims)}
Contradictions: {sum(1 for v in validations if v == "contradict")}
"""
        for i, (claim, validation) in enumerate(zip(claims, validations), 1):
            text_export += f"\n{i}. [{validation.upper()}] {claim}\n"
        
        st.download_button(
            label="📄 TXT",
            data=text_export,
            file_name="chronoreason_results.txt",
            mime="text/plain"
        )

# Footer
st.divider()
st.caption("🏛️ ChronoReason v1.0 | Narrative Consistency Analyzer")
