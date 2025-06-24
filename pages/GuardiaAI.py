import os
import sys
import warnings
from typing import Optional, List, Any
import streamlit as st
import pandas as pd
import google.generativeai as genai
from pymongo import MongoClient
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain.llms.base import LLM

os.environ["KMP_DUPLICATE_LIB_OK"] = "True"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["PYTORCH_DISABLE_CUDA_MEMORY_CACHING"] = "1"
os.environ["STREAMLIT_SERVER_FILE_WATCHER_TYPE"] = "none"

warnings.filterwarnings("ignore")

try:
    import torch

    torch.set_num_threads(1)
    torch.autograd.set_grad_enabled(False)
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.set_device(0)
except Exception:
    torch = None


st.set_page_config(
    page_title="Crime",
    page_icon="././assets/LogoNobg.png",
    layout="wide",
)


MONGO_URI = "mongodb+srv://zaid_2003:zaid_2003@cluster1.03jozqw.mongodb.net/"
DB_NAME = "Crime"
COLLECTION_NAME = "Train"


class GeminiLLM(LLM):
    model_name: str = "gemini-2.0-flash"
    api_key: str = ""
    _client: Any = None

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"

    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash", **kwargs):
        super().__init__(api_key=api_key, model_name=model_name, **kwargs)
        genai.configure(api_key=api_key)
        object.__setattr__(self, "_client", genai.GenerativeModel(model_name))

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        try:
            return self._client.generate_content(prompt).text
        except Exception as e:
            return f"Error al generar respuesta: {e}"

    @property
    def _llm_type(self) -> str:
        return "gemini"


@st.cache_resource
def init_mongodb():
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        _coll = db[COLLECTION_NAME]
        client.admin.command("ping")
        return _coll, client
    except Exception as e:
        st.error(f"Error al conectar con MongoDB: {e}")
        return None, None


@st.cache_data
def load_and_process_mongo_data(_coll, limit=1000):
    try:
        cursor = _coll.find().limit(limit)
        docs, rows = [], []

        for i, doc in enumerate(cursor):
            doc["_id"] = str(doc["_id"])
            rows.append(doc)

            text = " ".join(f"{k}: {v}" for k, v in doc.items() if k != "_id")
            docs.append(
                Document(
                    page_content=text,
                    metadata={
                        "doc_index": i,
                        "source": "MongoDB",
                        "collection": COLLECTION_NAME,
                        "id": doc["_id"],
                    },
                )
            )
        return docs, pd.DataFrame(rows)
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return None, None


@st.cache_resource
def create_vector_store(_docs):
    if not _docs:
        return None
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu", "trust_remote_code": False},
            encode_kwargs={"normalize_embeddings": True, "batch_size": 32},
            show_progress=False,
        )
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, length_function=len
        )
        texts = splitter.split_documents(_docs)
        return FAISS.from_documents(texts, embeddings, distance_strategy="COSINE")
    except Exception as e:
        st.error(f"Error al crear vector store: {e}")
        return None


def main():
    st.markdown("# Welcome to our Crime Data Project")
    st.markdown("### 🔍 Analiza datos de crimen con IA conversacional")

    with st.sidebar:
        st.header("⚙️ Configuración")
        gem_api_key = st.text_input(
            "API Key de Gemini:",
            type="password",
            help="Obtén tu API key en https://makersuite.google.com/app/apikey",
        )
        data_limit = st.slider("Límite de documentos:", 100, 5000, 1000, 100)
        st.info(f"**Base de datos:** {DB_NAME}\n**Colección:** {COLLECTION_NAME}")
        if st.button("🔄 Reconectar a MongoDB"):
            st.cache_resource.clear()
            st.rerun()

    with st.expander("🔧 Info del sistema"):
        st.write(f"Python: {sys.version}")
        st.write(f"Streamlit: {st.__version__}")
        st.write(f"PyTorch: {torch.__version__ if torch else 'No disponible'}")

    with st.spinner("Conectando a MongoDB..."):
        _coll, _ = init_mongodb()
    if _coll is None:
        st.stop()
    st.success("✅ Conectado a MongoDB")

    if not gem_api_key:
        st.info("👈 Ingresa tu API key para empezar.")
        return

    with st.spinner("Cargando y vectorizando datos..."):
        docs, df = load_and_process_mongo_data(_coll, data_limit)
        vect_store = create_vector_store(docs)
    if vect_store is None:
        st.stop()
    st.success(f"✅ Vectorizados {len(docs)} documentos")

    c1, c2, c3 = st.columns(3)
    c1.metric("Registros", len(df))
    c2.metric("Columnas", len(df.columns))
    c3.metric("Embeddings", len(docs))

    with st.expander("📊 Vista previa"):
        st.dataframe(df.head(10))
        nums = df.select_dtypes("number")
        if nums.shape[1]:
            st.write("**Descriptivos:**")
            st.dataframe(nums.describe())

    llm = GeminiLLM(api_key=gem_api_key)
    st.header("💬 Pregúntale a tus datos")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("¿Qué quieres saber sobre los datos de crimen?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analizando..."):
                try:
                    ctx = "\n".join(
                        d.page_content for d in vect_store.similarity_search(prompt, k=5)
                    )
                    sys_prompt = f"""
Eres un analista de crimen.

Contexto:
{ctx}

Pregunta:
{prompt}

Instrucciones:
- Usa solo el contexto.
- Si falta info, di qué hay disponible.
- Responde en español de forma profesional.
"""
                    ans = llm._call(sys_prompt)
                except Exception as e:
                    ans = f"Error al procesar: {e}"

                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})

    col_a, col_b = st.columns(2)
    if col_a.button("🗑️ Limpiar conversación"):
        st.session_state.messages = []
        st.rerun()
    if col_b.button("🔄 Actualizar datos"):
        st.cache_data.clear()
        st.rerun()


if __name__ == "__main__":
    main()
