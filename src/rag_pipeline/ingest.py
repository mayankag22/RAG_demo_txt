import os
from typing import List

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


DATA_DIR = "data/sample_policies"
INDEX_DIR = "data/faiss_index"


def load_text_policies(data_dir: str) -> List:
    docs = []
    for fname in os.listdir(data_dir):
        if fname.lower().endswith(".txt"):
            path = os.path.join(data_dir, fname)
            loader = TextLoader(path, encoding="utf-8")
            docs.extend(loader.load())
    return docs


def chunk_docs(docs, chunk_size: int = 600, chunk_overlap: int = 100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\nSection", "\n\n", "\n", " "],
    )
    return splitter.split_documents(docs)


def build_faiss_index(chunks, index_dir: str = INDEX_DIR):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vs = FAISS.from_documents(chunks, embedding=embeddings)
    os.makedirs(index_dir, exist_ok=True)
    vs.save_local(index_dir)
    return vs


if __name__ == "__main__":
    docs = load_text_policies(DATA_DIR)
    chunks = chunk_docs(docs)
    build_faiss_index(chunks)
    print(f"Ingested {len(docs)} docs into {len(chunks)} chunks and built FAISS index at {INDEX_DIR}")
