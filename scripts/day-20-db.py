from pydantic import BaseModel
from typing import Union
import re
import numpy as np


class Document(BaseModel):
    id: str
    content: str


class Model:
    def __init__(self):
        self.STOPWORDS = set(
            """的 了 和 與 並 且 或 如果 因為 所以 而 但是 以及 目前 然後 就 是 有 在 到 於 從
為 以 被 這 那 一個 一些 可以 不 要 會 用 上 下 中 內 外 後 前 再 更 等 等等 之 其 讓
對 把 也 很 多 少 像 例如 比 如 同時 並且 以及 此 相關 主要 通常 常見 常用 使用
the a an and or but if so to of in on at for from by with is are was were be as into that this those these
""".split()
        )

    def clean_text(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^\w\u4e00-\u9fff]+", " ", text)
        return [char for char in text.split() if char not in self.STOPWORDS]

    def embed(self, text: str) -> list[float]:
        return [float(ord(c)) for c in text]


class VectorDatabase:
    def __init__(self):
        self.documents: list[Document] = []
        self.idf: dict[str, float] = {}
        self.vector_documents: list[dict[str, float]] = []
        self.model = Model()

    def add_document(self, doc: Union[Document, list[Document]]):
        if isinstance(doc, Document):
            self.documents.append(doc)
            self.vector_documents.append(
                {"id": doc.id, "vector": self.model.embed(doc.content)}
            )
        elif isinstance(doc, list):
            self.documents.extend(doc)
            for d in doc:
                self.vector_documents.append(
                    {"id": d.id, "vector": self.model.embed(d.content)}
                )

    def query(self, text: str) -> dict[str, float]:
        cleaned_text = self.model.clean_text(text)
        query_vector = self.model.embed(" ".join(cleaned_text))
        return {"query_vector": query_vector}

    def cosine_similarity(self, vec1: list[float], vec2: list[float]) -> float:
        # 取最大長度
        max_len = max(len(vec1), len(vec2))
        # 補零
        v1 = np.pad(vec1, (0, max_len - len(vec1)))
        v2 = np.pad(vec2, (0, max_len - len(vec2)))
        return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

    def retrieve(self, query_vector: list[float], top_k: int = 5) -> list[Document]:
        similarities = []
        for doc_vector, doc in zip(self.vector_documents, self.documents):
            sim = self.cosine_similarity(query_vector, doc_vector["vector"])
            similarities.append((sim, doc))
        similarities.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in similarities[:top_k]]


if __name__ == "__main__":
    db = VectorDatabase()
    db.add_document(
        [
            Document(id="1", content="測試這是一個測試文件"),
            Document(id="2", content="我喜歡貓咪咖啡廳"),
            Document(id="3", content="這是一個關於 Python 程式設計的文件"),
        ]
    )

    query_result = db.query("喝咖啡的地方")
    retrieved_docs = db.retrieve(query_result["query_vector"], top_k=2)

    for doc in retrieved_docs:
        print(f"Retrieved Document ID: {doc.id}, Content: {doc.content}")
