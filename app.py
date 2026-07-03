import streamlit as st
import tempfile

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from graph.workflow import app

@st.cache_resource
def load_embedding_model():
    return HuggingFaceEmbeddings(
        model_name="BAAI/bge-base-en-v1.5"
    )

embedding_model = load_embedding_model()

st.set_page_config(
    page_title="Agentic Corrective RAG",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Agentic Corrective RAG")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDF files",
    type=["pdf"],
    accept_multiple_files=True
)

# ---------------- PDF Processing ----------------

uploaded_names = sorted(
    [file.name for file in uploaded_files]
) if uploaded_files else []

if not uploaded_files:
    st.session_state.pop("uploaded_vector_db", None)
    st.session_state.pop("uploaded_files", None)
    st.session_state.pop("messages", None)
    st.rerun()


if (
    uploaded_files and
    st.session_state.get("uploaded_files") != uploaded_names
):

    with st.spinner("Processing PDFs..."):

        documents = []

        for uploaded_file in uploaded_files:

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as tmp_file:

                tmp_file.write(
                    uploaded_file.read()
                )

                tmp_path = tmp_file.name

            loader = PyMuPDFLoader(
                tmp_path
            )

            docs = loader.load()

            documents.extend(
                docs
            )

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        chunked_docs = splitter.split_documents(
            documents
        )

        uploaded_db = Chroma.from_documents(
            documents=chunked_docs,
            embedding=embedding_model
        )

        st.session_state.uploaded_vector_db = uploaded_db
        st.session_state.uploaded_files = uploaded_names

        st.sidebar.success(
            f"Indexed {len(chunked_docs)} chunks."
        )

# ------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask anything..."):

    if "uploaded_vector_db" not in st.session_state:
        st.warning("Please upload at least one PDF first.")
        st.stop()

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            result = app.invoke(
                {
                    "question": prompt,

                    # use uploaded DB if available
                    "vector_db": st.session_state.get(
                        "uploaded_vector_db",
                        None
                    )
                }
            )

            response = result["answer"]

        st.markdown(response)

        if result.get("route") == "local":
            st.caption(
                f"Source: Uploaded Document | Retrieval Score: {result['retrieval_score']:.3f}"
            )

        elif result.get("route") == "web":
            st.caption(
                f"Source: Web Search | Retrieval Score: {result['retrieval_score']:.3f}"
            )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )