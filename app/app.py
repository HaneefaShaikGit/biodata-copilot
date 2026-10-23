import streamlit as st

from biodata_copilot.ai.copilot import run_question
from biodata_copilot.ai.questions import QUESTIONS


st.set_page_config(
    page_title="BioData Copilot",
    page_icon="🧬",
    layout="wide",
)


st.title("🧬 BioData Copilot")

st.write(
    "Explore clinical and genomic patterns from the "
    "TCGA Breast Cancer PanCancer Atlas dataset."
)

st.info(
    "BioData Copilot uses verified SQL results for numerical facts. "
    "AI is used only to explain those results."
)


question_options = {
    details["question"]: number
    for number, details in QUESTIONS.items()
}


selected_question = st.selectbox(
    "Choose a question",
    question_options.keys(),
)


if st.button("Analyze"):

    choice = question_options[selected_question]

    with st.spinner("Running analysis..."):

        question, result, explanation = run_question(choice)


    st.subheader("Verified SQL Result")

    st.dataframe(
        result,
        use_container_width=True,
    )


    st.subheader("BioData Copilot Explanation")

    st.write(explanation)


    st.caption(
        "Results describe the selected dataset only and should not "
        "be interpreted as medical advice or causal conclusions."
    )