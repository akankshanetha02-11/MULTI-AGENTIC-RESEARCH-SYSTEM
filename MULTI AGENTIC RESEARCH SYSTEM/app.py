
import streamlit as st
import time

from src.agents.agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain,
)


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Multi-Agent Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# 2. CUSTOM CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700&display=swap');

/* Main background */

.stApp {
    background-color: #07111f;
    background-image:
        radial-gradient(
            circle at top left,
            rgba(0,191,255,0.12),
            transparent 35%
        ),
        radial-gradient(
            circle at bottom right,
            rgba(124,58,237,0.10),
            transparent 35%
        ),
        linear-gradient(
            180deg,
            #07111f 0%,
            #0a1729 100%
        );
}

/* General font */

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Main container */

.block-container {
    max-width: 1350px !important;
    padding: 2rem 3rem 4rem !important;
}

/* Hide Streamlit header and footer */

#MainMenu, footer, header {
    visibility: hidden;
}

/* Default text */

.stMarkdown,
.stMarkdown p,
.stMarkdown li,
[data-testid="stMarkdownContainer"] {
    color: #e2e8f0 !important;
    opacity: 1 !important;
}

/* Hero */

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(38px, 6vw, 70px);
    font-weight: 800;
    color: #ffffff !important;
    text-align: center;
    line-height: 1.2;
    margin-top: 15px;
    margin-bottom: 15px;
}

.hero-subtitle {
    color: #cbd5e1 !important;
    font-size: 17px;
    text-align: center;
    line-height: 1.8;
    max-width: 700px;
    margin: auto;
}

.hero-eyebrow {
    color: #38bdf8 !important;
    text-align: center;
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    letter-spacing: 4px;
    font-weight: 500;
}

/* Section headings */

.section-heading {
    color: #ffffff !important;
    font-family: 'Syne', sans-serif;
    font-size: 25px;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 18px;
}

/* Divider */

hr {
    border-color: #29435e !important;
    margin-top: 30px;
    margin-bottom: 30px;
}

/* Input */

.stTextInput label {
    color: #7dd3fc !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 13px !important;
}

.stTextInput input {
    background: #17283d !important;
    color: #ffffff !important;
    border: 1px solid #3b607d !important;
    border-radius: 10px !important;
    font-size: 16px !important;
    padding: 12px !important;
}

.stTextInput input::placeholder {
    color: #94a3b8 !important;
}

.stTextInput input:focus {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 0 2px rgba(56,189,248,0.2) !important;
}

/* Buttons */

.stButton button {
    background: linear-gradient(
        135deg,
        #0284c7,
        #7c3aed
    ) !important;

    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    padding: 12px !important;
    width: 100%;
    transition: 0.2s ease;
}

.stButton button:hover {
    box-shadow: 0 8px 25px rgba(56,189,248,0.3);
    transform: translateY(-2px);
}

/* Containers */

[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(16,30,48,0.85) !important;
    border: 1px solid #29435e !important;
    border-radius: 14px !important;
}

/* Pipeline text */

.step-number {
    color: #38bdf8 !important;
    font-family: 'DM Mono', monospace;
    font-size: 14px;
    font-weight: 600;
}

.step-title {
    color: #ffffff !important;
    font-size: 16px;
    font-weight: 700;
}

.step-description {
    color: #cbd5e1 !important;
    font-size: 13px;
}

.status-waiting {
    color: #94a3b8 !important;
}

.status-running {
    color: #38bdf8 !important;
}

.status-done {
    color: #4ade80 !important;
}

/* Report headings */

.stMarkdown h1 {
    color: #ffffff !important;
    font-size: 34px !important;
    font-weight: 800 !important;
    line-height: 1.4 !important;
    margin-top: 25px !important;
}

.stMarkdown h2 {
    color: #7dd3fc !important;
    font-size: 26px !important;
    font-weight: 700 !important;
    margin-top: 30px !important;
    margin-bottom: 15px !important;
}

.stMarkdown h3 {
    color: #c4b5fd !important;
    font-size: 21px !important;
    font-weight: 700 !important;
    margin-top: 22px !important;
}

/* Report paragraphs */

.stMarkdown p {
    color: #e2e8f0 !important;
    font-size: 16px !important;
    line-height: 1.9 !important;
}

/* Bold */

.stMarkdown strong,
.stMarkdown b {
    color: #ffffff !important;
    font-weight: 700 !important;
}

/* Lists */

.stMarkdown li {
    color: #e2e8f0 !important;
    line-height: 1.9 !important;
    margin-bottom: 7px;
}

/* Links */

.stMarkdown a {
    color: #38bdf8 !important;
}

/* Tables */

.stMarkdown table {
    width: 100% !important;
    border-collapse: collapse !important;
}

.stMarkdown th {
    background: #1e3a5a !important;
    color: #ffffff !important;
    padding: 12px !important;
    border: 1px solid #475569 !important;
}

.stMarkdown td {
    background: #13243a !important;
    color: #e2e8f0 !important;
    padding: 12px !important;
    border: 1px solid #334155 !important;
}

/* Inline code */

.stMarkdown code {
    background: #1e293b !important;
    color: #67e8f9 !important;
    padding: 4px 7px;
    border-radius: 5px;
}

/* Code blocks */

.stMarkdown pre {
    background: #0b1220 !important;
    border: 1px solid #334155;
    border-radius: 10px;
}

/* Expanders */

[data-testid="stExpander"] {
    background: #101e30 !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
}

[data-testid="stExpander"] summary {
    color: #7dd3fc !important;
}

/* Download button */

.stDownloadButton button {
    background: #0369a1 !important;
    color: #ffffff !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    border: none !important;
}

/* Footer */

.footer-text {
    color: #94a3b8 !important;
    text-align: center;
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    line-height: 2;
}

/* Spinner */

.stSpinner {
    color: #38bdf8 !important;
}

/* Mobile */

@media(max-width: 768px) {

    .block-container {
        padding: 1rem !important;
    }

    .hero-title {
        font-size: 38px;
    }

    .section-heading {
        font-size: 21px;
    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# 3. SESSION STATE
# ============================================================

if "results" not in st.session_state:
    st.session_state.results = {}

if "running" not in st.session_state:
    st.session_state.running = False

if "done" not in st.session_state:
    st.session_state.done = False


# ============================================================
# 4. HELPER FUNCTIONS
# ============================================================

def extract_text(value):
    """Convert model output into readable text."""

    if isinstance(value, str):
        return value

    if hasattr(value, "content"):
        return str(value.content)

    return str(value)


def render_step(placeholder, num, title, state, desc):

    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("● RUNNING", "status-running"),
        "done": ("✓ DONE", "status-done"),
    }

    label, status_class = status_map[state]

    with placeholder.container():

        with st.container(border=True):

            col1, col2, col3 = st.columns(
                [0.6, 3.2, 1.2]
            )

            with col1:
                st.markdown(
                    f'<p class="step-number">{num}</p>',
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown(
                    f'<p class="step-title">{title}</p>',
                    unsafe_allow_html=True
                )

            with col3:
                st.markdown(
                    f'<p class="{status_class}">{label}</p>',
                    unsafe_allow_html=True
                )

            st.markdown(
                f'<p class="step-description">{desc}</p>',
                unsafe_allow_html=True
            )


def update_pipeline(placeholders, results, running=False):

    steps = [
        ("01", "Search Agent", "search",
         "Gathers recent and reliable web information"),

        ("02", "Reader Agent", "reader",
         "Scrapes and extracts detailed content"),

        ("03", "Writer Chain", "writer",
         "Creates the complete research report"),

        ("04", "Critic Chain", "critic",
         "Reviews and evaluates the research report"),
    ]

    next_step = None

    if running:
        for _, _, key, _ in steps:
            if key not in results:
                next_step = key
                break

    for i, (num, title, key, desc) in enumerate(steps):

        if key in results:
            state = "done"
        elif running and key == next_step:
            state = "running"
        else:
            state = "waiting"

        render_step(
            placeholders[i],
            num,
            title,
            state,
            desc
        )


# ============================================================
# 5. HERO SECTION
# ============================================================

st.markdown(
    '<p class="hero-eyebrow">MULTI-AGENT AI SYSTEM</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<h1 class="hero-title">Researcher Agent</h1>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <p class="hero-subtitle">
        Four specialized AI agents collaborate —
        searching, scraping, writing and critiquing —
        to deliver a professional research report on any topic.
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# 6. INPUT AND PIPELINE LAYOUT
# ============================================================

col_input, col_spacer, col_pipeline = st.columns(
    [5, 0.4, 4]
)

pipeline_placeholders = []

with col_input:

    st.markdown(
        '<p class="section-heading">Research Topic</p>',
        unsafe_allow_html=True
    )

    with st.container(border=True):

        topic = st.text_input(
            "Enter your research topic",
            placeholder="e.g. Future of LLM in Tech Industry",
            key="topic_input"
        )

        run_btn = st.button(
            "⚡ Run Research Pipeline",
            use_container_width=True
        )

    st.markdown(
        '<p class="section-heading">Try These Topics</p>',
        unsafe_allow_html=True
    )

    examples = [
        "Future of LLM in Tech Industry",
        "Latest AI Agents in 2026",
        "Roadmap for AGI development",
    ]

    for example in examples:

        st.markdown(
            f"💡 {example}"
        )


with col_pipeline:

    st.markdown(
        '<p class="section-heading">Pipeline</p>',
        unsafe_allow_html=True
    )

    for _ in range(4):
        pipeline_placeholders.append(st.empty())

    update_pipeline(
        pipeline_placeholders,
        st.session_state.results,
        st.session_state.running
    )


# ============================================================
# 7. START PIPELINE
# ============================================================

if run_btn:

    if not topic.strip():

        st.warning(
            "Please enter a research topic first."
        )

    else:

        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False

        st.rerun()


# ============================================================
# 8. MULTI-AGENT EXECUTION
# ============================================================

if (
    st.session_state.running
    and not st.session_state.done
):

    results = st.session_state.results

    topic_val = st.session_state.topic_input

    try:

        # ----------------------------------------------------
        # STEP 1: SEARCH AGENT
        # ----------------------------------------------------

        if "search" not in results:

            with st.spinner(
                "🔍 Search Agent is gathering information..."
            ):

                search_agent = build_search_agent()

                sr = search_agent.invoke({
                    "messages": [
                        (
                            "user",
                            f"""
                            Find recent, reliable and detailed
                            information about: {topic_val}

                            Return relevant URLs, summaries,
                            publication dates and useful sources.
                            """
                        )
                    ]
                })

                results["search"] = extract_text(
                    sr["messages"][-1].content
                )

                st.session_state.results = dict(results)

                update_pipeline(
                    pipeline_placeholders,
                    results,
                    running=True
                )


        # ----------------------------------------------------
        # STEP 2: READER AGENT
        # ----------------------------------------------------

        if "reader" not in results:

            with st.spinner(
                "📄 Reader Agent is scraping resources..."
            ):

                reader_agent = build_reader_agent()

                rr = reader_agent.invoke({
                    "messages": [
                        (
                            "user",
                            f"""
                            Based on the following search results
                            about '{topic_val}', select the most
                            relevant URL and scrape it for detailed
                            information.

                            Search Results:

                            {results['search'][:800]}

                            Return extracted content clearly.
                            """
                        )
                    ]
                })

                results["reader"] = extract_text(
                    rr["messages"][-1].content
                )

                st.session_state.results = dict(results)

                update_pipeline(
                    pipeline_placeholders,
                    results,
                    running=True
                )


        # ----------------------------------------------------
        # STEP 3: WRITER CHAIN
        # ----------------------------------------------------

        if "writer" not in results:

            with st.spinner(
                "✍️ Writer is creating the research report..."
            ):

                research_combined = f"""
                SEARCH RESULTS:

                {results['search']}

                DETAILED SCRAPED CONTENT:

                {results['reader']}
                """

                writer_output = writer_chain.invoke({
                    "topic": topic_val,
                    "research": research_combined
                })

                results["writer"] = extract_text(
                    writer_output
                )

                st.session_state.results = dict(results)

                update_pipeline(
                    pipeline_placeholders,
                    results,
                    running=True
                )


        # ----------------------------------------------------
        # STEP 4: CRITIC CHAIN
        # ----------------------------------------------------

        if "critic" not in results:

            with st.spinner(
                "🧐 Critic is reviewing the report..."
            ):

                critic_output = critic_chain.invoke({
                    "report": results["writer"]
                })

                results["critic"] = extract_text(
                    critic_output
                )

                st.session_state.results = dict(results)

                update_pipeline(
                    pipeline_placeholders,
                    results,
                    running=False
                )


        # ----------------------------------------------------
        # COMPLETED
        # ----------------------------------------------------

        st.session_state.results = dict(results)
        st.session_state.running = False
        st.session_state.done = True

        st.success(
            "Research pipeline completed successfully!"
        )

        st.rerun()


    except Exception as e:

        st.session_state.results = dict(results)
        st.session_state.running = False

        st.error(
            f"Research pipeline failed: {str(e)}"
        )

        with st.expander("View Error Details"):
            st.exception(e)


# ============================================================
# 9. RESULTS DISPLAY
# ============================================================

r = st.session_state.results

if r:

    st.divider()

    st.markdown(
        '<p class="section-heading">📊 Research Results</p>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # SEARCH RESULTS
    # --------------------------------------------------------

    if "search" in r:

        with st.expander(
            "🔍 Search Agent Results",
            expanded=False
        ):

            st.subheader("Search Agent Output")

            st.markdown(
                r["search"],
                unsafe_allow_html=False
            )


    # --------------------------------------------------------
    # READER RESULTS
    # --------------------------------------------------------

    if "reader" in r:

        with st.expander(
            "📄 Scraped Content",
            expanded=False
        ):

            st.subheader("Reader Agent Output")

            st.markdown(
                r["reader"],
                unsafe_allow_html=False
            )


    # --------------------------------------------------------
    # FINAL REPORT
    # --------------------------------------------------------

    if "writer" in r:

        st.divider()

        st.markdown(
            '<p class="section-heading">📝 Final Research Report</p>',
            unsafe_allow_html=True
        )

        with st.container(border=True):

            st.markdown(
                r["writer"],
                unsafe_allow_html=False
            )

        st.download_button(
            label="⬇ Download Research Report (.md)",
            data=r["writer"],
            file_name=(
                f"research_report_{int(time.time())}.md"
            ),
            mime="text/markdown",
            use_container_width=True
        )


    # --------------------------------------------------------
    # CRITIC FEEDBACK
    # --------------------------------------------------------

    if "critic" in r:

        st.divider()

        st.markdown(
            '<p class="section-heading">🧐 Critic Feedback</p>',
            unsafe_allow_html=True
        )

        with st.container(border=True):

            st.markdown(
                r["critic"],
                unsafe_allow_html=False
            )


# ============================================================
# 10. FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <p class="footer-text">
        ResearchAgent<br>
        Powered by LangChain Multi-Agent Pipeline<br>
        Built with Python and Streamlit
    </p>
    """,
    unsafe_allow_html=True
)

