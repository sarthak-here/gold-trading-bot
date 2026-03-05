from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
RAG_DIR = BASE_DIR / "01-rag-assistant"
VISION_DIR = BASE_DIR / "02-vision-quality-inspector"


def load_module(module_path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module: {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@st.cache_resource
def load_rag_retriever():
    retriever_module = load_module(RAG_DIR / "retriever.py", "rag_retriever")
    return retriever_module.retrieve_top_k


@st.cache_resource
def load_vision_predictor():
    infer_module = load_module(VISION_DIR / "infer.py", "vision_infer")
    return infer_module.predict_defect_stub


st.set_page_config(page_title="AI Projects Interface", page_icon="🧠", layout="wide")
st.title("🧠 AI Projects — Public Demo Interface")
st.caption("One Streamlit app for the two latest open project starters: RAG Assistant and Vision Quality Inspector.")

rag_tab, vision_tab = st.tabs(["01 · RAG Assistant", "02 · Vision Inspector"])

with rag_tab:
    st.subheader("Ask the RAG Assistant")
    st.write("This uses the current placeholder retrieval pipeline from `01-rag-assistant/retriever.py`.")

    question = st.text_input("Question", placeholder="What is XAUUSD?")

    if st.button("Ask", type="primary", key="ask_rag"):
        if not question.strip():
            st.warning("Please enter a question first.")
        else:
            retrieve_top_k = load_rag_retriever()
            chunks = retrieve_top_k(question, k=3)
            sources = [{"text": c.text, "score": c.score} for c in chunks]

            if not sources:
                answer = "No relevant context found."
            else:
                answer = f"Based on retrieved context: {sources[0]['text']}"

            st.success(answer)
            st.write("**Sources**")
            for idx, src in enumerate(sources, start=1):
                st.markdown(f"{idx}. `{src['score']:.2f}` — {src['text']}")

with vision_tab:
    st.subheader("Inspect Product Image")
    st.write("Upload an image and run the current stub predictor from `02-vision-quality-inspector/infer.py`.")

    uploaded = st.file_uploader("Upload image", type=["png", "jpg", "jpeg", "webp"], key="vision_upload")

    if uploaded is not None:
        st.image(uploaded, caption="Uploaded image", use_container_width=True)

        if st.button("Run Inspection", type="primary", key="run_vision"):
            predictor = load_vision_predictor()

            suffix = Path(uploaded.name).suffix or ".png"
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uploaded.getbuffer())
                temp_path = tmp.name

            try:
                pred = predictor(temp_path)
                st.metric("Prediction", pred.get("label", "unknown"))
                st.metric("Confidence", f"{pred.get('confidence', 0.0):.2%}")
            except Exception as exc:
                st.error(f"Inference failed: {exc}")

st.divider()
st.caption("Tip: run with `streamlit run ai-projects/streamlit_interface.py`")
