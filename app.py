import streamlit as st
import tempfile
import ollama

from image_analysis import analyze_image
from suggestions import generate_suggestions

from rag import (
    load_knowledge,
    create_embeddings,
    create_vector_database,
    search_knowledge
)

from llm import generate_ai_advice


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Photography Assistant",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# CUSTOM CSS
#
# IMPORTANT:
# CSS is the ONLY place where we use HTML/CSS syntax.
# Visible app content below uses normal Streamlit components.
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       MAIN PAGE
       ===================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 5% 0%,
                rgba(99, 102, 241, 0.08),
                transparent 30%
            ),
            radial-gradient(
                circle at 95% 0%,
                rgba(236, 72, 153, 0.07),
                transparent 28%
            ),
            #0e1016;
    }


    .block-container {
        max-width: 1120px;
        padding-top: 4rem;
        padding-bottom: 2rem;
    }


    /* =====================================================
       HERO
       ===================================================== */

    .hero-icon {
        text-align: center;
        font-size: 42px;
        margin-top: 0;
        margin-bottom: 4px;
    }


    .hero-title {
        text-align: center;
        font-size: 40px;
        font-weight: 700;
        line-height: 1.2;
        color: #f5f5f7;
        margin-bottom: 6px;
    }


    .hero-subtitle {
        text-align: center;
        font-size: 16px;
        color: #9ca3af;
        margin-bottom: 22px;
    }


    /* =====================================================
       SECTION HEADINGS
       ===================================================== */

    h2 {
        font-size: 32px !important;
        margin-top: 0.8rem !important;
        margin-bottom: 0.5rem !important;
    }


    /* =====================================================
       UPLOAD BOX
       ===================================================== */

    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.025);
        border: 1px dashed rgba(255, 255, 255, 0.22);
        border-radius: 14px;
        padding: 8px;
    }


    /* =====================================================
       FEATURE CARDS
       ===================================================== */

    .feature-card {
        height: 205px;
        min-height: 205px;
        box-sizing: border-box;
    }


    .feature-card h3 {
        font-size: 23px;
        margin-top: 0;
        margin-bottom: 16px;
    }


    .feature-card p {
        font-size: 15px;
        line-height: 1.6;
        color: #d7dbe5;
    }


    /* =====================================================
       BORDERED STREAMLIT CONTAINERS
       ===================================================== */

    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px !important;
        border-color: rgba(255, 255, 255, 0.13) !important;
        background: rgba(255, 255, 255, 0.015);
    }


    /* =====================================================
       BUTTONS
       ===================================================== */

    .stButton > button {
        border-radius: 10px;
        min-height: 42px;
        font-weight: 600;
    }


    /* =====================================================
       METRICS
       ===================================================== */

    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.025);
        border: 1px solid rgba(255, 255, 255, 0.10);
        border-radius: 14px;

        /* Same size for all five analysis cards */
        height: 145px;
        min-height: 145px;

        box-sizing: border-box;
        padding: 18px 20px;

        overflow: hidden;
    }


    /* =====================================================
       METRIC LABELS
       ===================================================== */

    [data-testid="stMetricLabel"] {
        font-size: 16px !important;
        line-height: 1.3 !important;

        white-space: normal !important;
        overflow: visible !important;
        text-overflow: clip !important;

        word-break: normal !important;
    }


    /* =====================================================
       METRIC VALUES
       ===================================================== */

    [data-testid="stMetricValue"] {
        font-size: 19px !important;
        line-height: 1.3 !important;

        white-space: normal !important;
        overflow: visible !important;
        text-overflow: clip !important;

        word-break: normal !important;
        overflow-wrap: anywhere !important;

        margin-top: 10px !important;
    }


    /* =====================================================
       FIX STREAMLIT INTERNAL METRIC VALUE ELEMENT
       ===================================================== */

    [data-testid="stMetricValue"] > div {
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: clip !important;
        word-break: normal !important;
        overflow-wrap: anywhere !important;
    }


    /* =====================================================
       FIX ALL INNER ELEMENTS RESPONSIBLE FOR ELLIPSIS
       ===================================================== */

    [data-testid="stMetricValue"] * {
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: clip !important;
        word-break: normal !important;
        overflow-wrap: anywhere !important;
    }


    /* =====================================================
       KEEP METRIC COLUMNS ALIGNED
       ===================================================== */

    [data-testid="stHorizontalBlock"] {
        align-items: stretch;
    }


    /* =====================================================
       IMAGES
       ===================================================== */

    [data-testid="stImage"] img {
        border-radius: 14px;
    }


    /* =====================================================
       FOOTER
       ===================================================== */

    .footer-text {
        text-align: center;
        color: #747c8f;
        font-size: 12px;
        line-height: 1.8;
        margin-top: 5px;
    }


    /* =====================================================
       MOBILE
       ===================================================== */

    @media (max-width: 768px) {

        .block-container {
            padding-top: 2.5rem;
        }

        .hero-title {
            font-size: 30px;
        }

        .hero-icon {
            font-size: 36px;
        }

        .feature-card {
            height: auto;
            min-height: 170px;
        }

        [data-testid="stMetric"] {
            height: 130px;
            min-height: 130px;
            padding: 14px;
        }

        [data-testid="stMetricLabel"] {
            font-size: 14px !important;
        }

        [data-testid="stMetricValue"] {
            font-size: 19px !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# RAG SYSTEM
# =========================================================

@st.cache_resource
def load_rag_system():

    documents = load_knowledge()

    model, embeddings = create_embeddings(
        documents
    )

    index = create_vector_database(
        embeddings
    )

    return documents, model, index


# =========================================================
# SESSION STATE
# =========================================================

if "result" not in st.session_state:
    st.session_state.result = None

if "suggestions" not in st.session_state:
    st.session_state.suggestions = []

if "relevant_tips" not in st.session_state:
    st.session_state.relevant_tips = []

if "ai_advice" not in st.session_state:
    st.session_state.ai_advice = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# =========================================================
# HERO
# =========================================================

st.markdown(
    '<div class="hero-icon">📸</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-title">AI Photography Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">'
    'Analyze • Improve • Learn • Capture Better'
    '</div>',
    unsafe_allow_html=True
)


st.divider()


# =========================================================
# NEW PHOTO BUTTON
# =========================================================

if st.session_state.result is not None:

    _, button_column = st.columns(
        [5, 1]
    )

    with button_column:

        if st.button(
            "🔄 New Photo",
            use_container_width=True
        ):

            st.session_state.result = None
            st.session_state.suggestions = []
            st.session_state.relevant_tips = []
            st.session_state.ai_advice = None
            st.session_state.chat_history = []

            st.rerun()


# =========================================================
# UPLOAD SECTION
# =========================================================

st.header("📤 Upload Your Photo")

st.caption(
    "Upload a JPG, JPEG or PNG image to get personalized photography feedback."
)


uploaded_file = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)


# =========================================================
# IF NO PHOTO
# =========================================================

if uploaded_file is None:

    st.info(
        "👆 Upload a photo above to get started."
    )


# =========================================================
# IF PHOTO IS UPLOADED
# =========================================================

else:

    st.success(
        f"✅ {uploaded_file.name} uploaded successfully."
    )

    st.write("")


    # =====================================================
    # PHOTO PREVIEW
    # =====================================================

    photo_column, analysis_column = st.columns(
        [1.3, 0.7],
        gap="large"
    )


    with photo_column:

        st.subheader("🖼️ Photo Preview")

        st.image(
            uploaded_file,
            use_container_width=True
        )


    with analysis_column:

        st.subheader("🔍 Analyze")

        st.write(
            "The assistant will examine:"
        )

        st.write(
            """
            • Brightness
            • Contrast
            • Composition
            • Sharpness
            • Visual detail
            """
        )

        st.write("")

        analyze_button = st.button(
            "✨ Analyze My Photo",
            type="primary",
            use_container_width=True
        )


        # =================================================
        # ANALYSIS
        # =================================================

        if analyze_button:

            with st.spinner(
                "Analyzing your photograph..."
            ):

                # -----------------------------------------
                # SAVE IMAGE
                # -----------------------------------------

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".jpg"
                ) as temp_file:

                    temp_file.write(
                        uploaded_file.getvalue()
                    )

                    image_path = temp_file.name


                # -----------------------------------------
                # IMAGE ANALYSIS
                # -----------------------------------------

                result = analyze_image(
                    image_path
                )


                # -----------------------------------------
                # SUGGESTIONS
                # -----------------------------------------

                suggestions = generate_suggestions(
                    result
                )


                # -----------------------------------------
                # RAG
                # -----------------------------------------

                documents, model, index = (
                    load_rag_system()
                )


                query = f"""
                Photography advice for an image with:

                Brightness: {result['brightness']}
                Contrast: {result['contrast']}
                Composition: {result['composition']}
                Sharpness: {result['sharpness']}
                Visual Detail: {result['visual_detail']}
                """


                relevant_tips = search_knowledge(
                    query,
                    documents,
                    model,
                    index
                )


                # -----------------------------------------
                # AI ADVICE
                # -----------------------------------------

                ai_advice = generate_ai_advice(
                    result,
                    relevant_tips
                )


                # -----------------------------------------
                # SAVE
                # -----------------------------------------

                st.session_state.result = result

                st.session_state.suggestions = (
                    suggestions
                )

                st.session_state.relevant_tips = (
                    relevant_tips
                )

                st.session_state.ai_advice = (
                    ai_advice
                )

                st.session_state.chat_history = []


            st.success(
                "🎉 Analysis completed successfully!"
            )

            st.rerun()


# =========================================================
# RESULTS
# =========================================================

if st.session_state.result is not None:

    result = st.session_state.result

    suggestions = st.session_state.suggestions

    relevant_tips = (
        st.session_state.relevant_tips
    )

    ai_advice = (
        st.session_state.ai_advice
    )


    st.divider()


    # =====================================================
    # ANALYSIS RESULTS
    # =====================================================

    st.header("📊 Photo Analysis")

    st.caption(
        "Technical analysis of your uploaded photograph."
    )


    # =====================================================
    # ANALYSIS METRICS
    # =====================================================

    metric1, metric2, metric3, metric4, metric5 = st.columns(
        5,
        gap="small"
    )


    with metric1:

        st.metric(
            label="☀️ Brightness",
            value=result["brightness"]
        )


    with metric2:

        st.metric(
            label="◐ Contrast",
            value=result["contrast"]
        )


    with metric3:

        st.metric(
            label="🖼️ Composition",
            value=result["composition"]
        )


    with metric4:

        st.metric(
            label="🎯 Sharpness",
            value=result["sharpness"]
        )


    with metric5:

        st.metric(
            label="🔎 Detail",
            value=result["visual_detail"]
        )


    # =====================================================
    # TECHNICAL DETAILS
    # =====================================================

    with st.expander(
        "📐 Technical Details"
    ):

        detail1, detail2, detail3, detail4, detail5 = (
            st.columns(5)
        )


        with detail1:

            st.write("**Image Size**")

            st.write(
                f"{result['width']} × "
                f"{result['height']}"
            )


        with detail2:

            st.write("**Brightness**")

            st.write(
                result["brightness_value"]
            )


        with detail3:

            st.write("**Contrast**")

            st.write(
                result["contrast_value"]
            )


        with detail4:

            st.write("**Sharpness**")

            st.write(
                result["sharpness_value"]
            )


        with detail5:

            st.write("**Visual Detail**")

            st.write(
                result["visual_detail_value"]
            )


    # =====================================================
    # SUGGESTIONS
    # =====================================================

    st.header("💡 Photography Suggestions")

    st.caption(
        "Practical improvements based on the image analysis."
    )


    suggestion_columns = st.columns(
        2,
        gap="medium"
    )


    for index, suggestion in enumerate(
        suggestions
    ):

        with suggestion_columns[index % 2]:

            with st.container(
                border=True
            ):

                st.write(
                    f"💡 **Tip {index + 1}**"
                )

                st.write(
                    suggestion
                )


    # =====================================================
    # AI ADVICE
    # =====================================================

    st.header("🤖 AI Photography Advice")

    with st.container(
        border=True
    ):

        st.write(
            "✨ **Personalized Advice**"
        )

        st.write(
            ai_advice
        )


    # =====================================================
    # RAG KNOWLEDGE
    # =====================================================

    with st.expander(
        "📚 Photography knowledge used by AI"
    ):

        if relevant_tips:

            for index, tip in enumerate(
                relevant_tips
            ):

                st.write(
                    f"**Knowledge {index + 1}**"
                )

                st.write(
                    tip
                )

                if index < len(relevant_tips) - 1:
                    st.divider()

        else:

            st.info(
                "No relevant knowledge was retrieved."
            )


    # =====================================================
    # CHAT
    # =====================================================

    st.header(
        "💬 Ask Your Photography Assistant"
    )

    st.caption(
        "Ask follow-up questions about your photograph."
    )


    # -----------------------------------------------------
    # CHAT HISTORY
    # -----------------------------------------------------

    for message in st.session_state.chat_history:

        with st.chat_message(
            message["role"]
        ):

            st.write(
                message["content"]
            )


    # -----------------------------------------------------
    # CHAT INPUT
    # -----------------------------------------------------

    user_question = st.chat_input(
        "Ask something about your photo..."
    )


    if user_question:

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": user_question
            }
        )


        with st.spinner(
            "AI is thinking..."
        ):

            chat_prompt = f"""
You are an AI photography assistant.

The user uploaded a photograph.

Here is the technical analysis:

Brightness:
{result["brightness"]}

Brightness value:
{result["brightness_value"]}

Contrast:
{result["contrast"]}

Contrast value:
{result["contrast_value"]}

Composition:
{result["composition"]}

Sharpness:
{result["sharpness"]}

Sharpness value:
{result["sharpness_value"]}

Visual detail:
{result["visual_detail"]}

Visual detail value:
{result["visual_detail_value"]}

Image dimensions:
{result["width"]} x {result["height"]}


Relevant photography knowledge:

{chr(10).join(relevant_tips)}


Answer the user's question using the information
above.

Give practical photography advice suitable for
a beginner.

Do not invent objects, people, locations or visual
details that are not provided by the analysis.
"""


            messages = [
                {
                    "role": "system",
                    "content": chat_prompt
                }
            ]


            messages.extend(
                st.session_state.chat_history
            )


            response = ollama.chat(
                model="llama3.2",
                messages=messages
            )


            answer = response[
                "message"
            ][
                "content"
            ]


        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": answer
            }
        )


        st.rerun()


# =========================================================
# FEATURES
#
# Only show these when no photo has been analyzed.
# =========================================================

if st.session_state.result is None:

    st.divider()

    st.header(
        "✨ What can this assistant do?"
    )


    feature1, feature2, feature3 = st.columns(
        3,
        gap="medium"
    )


    # =====================================================
    # CARD 1
    # =====================================================

    with feature1:

        with st.container(
            border=True
        ):

            st.markdown(
                "### 🔍 Analyze"
            )

            st.write(
                "Analyze brightness, contrast, "
                "composition, sharpness and "
                "visual detail."
            )

            # Keep cards equal height.
            st.write("")
            st.write("")


    # =====================================================
    # CARD 2
    # =====================================================

    with feature2:

        with st.container(
            border=True
        ):

            st.markdown(
                "### 💡 Improve"
            )

            st.write(
                "Get practical photography "
                "suggestions based on the "
                "technical analysis."
            )

            # Keep cards equal height.
            st.write("")
            st.write("")


    # =====================================================
    # CARD 3
    # =====================================================

    with feature3:

        with st.container(
            border=True
        ):

            st.markdown(
                "### 🤖 Learn"
            )

            st.write(
                "Ask questions and learn "
                "photography concepts using "
                "AI and RAG."
            )

            # Keep cards equal height.
            st.write("")
            st.write("")


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "📸 AI Photography Assistant  •  "
    "Analyze • Improve • Learn"
)

st.caption(
    "Python • OpenCV • RAG • FAISS • "
    "Sentence Transformers • Ollama"
)