from pydantic import BaseModel
from typing import List, Union, Optional
import hashlib
import math
import random


class Document(BaseModel):
    id: str
    content: str


class SimpleTokenizer:
    """
    超輕量 tokenize：
    - 不做斷詞、不移除停用詞
    - 中文：逐字為一個 token（避免下載分詞模型）
    - 英數：連續英數視為一個 token
    - 其他符號/空白：視為分隔
    """

    def tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens: List[str] = []
        buf: List[str] = []

        def flush_buf():
            nonlocal buf
            if buf:
                tokens.append("".join(buf))
                buf = []

        for ch in text:
            if "a" <= ch <= "z" or "0" <= ch <= "9":
                buf.append(ch)
            elif "\u4e00" <= ch <= "\u9fff":  # CJK 統一表意文字區段
                flush_buf()
                tokens.append(ch)
            else:
                # 其他符號視為分隔
                flush_buf()

        flush_buf()
        return tokens

    def hash32(self, token: str) -> int:
        """對單一 token 產生 32-bit 決定性雜湊值。"""
        h = hashlib.sha1(token.encode("utf-8")).digest()
        return int.from_bytes(h[:4], "little")

    def to_hash32(self, tokens: List[str]) -> List[int]:
        """對一串 tokens 產生 32-bit 決定性雜湊值清單。"""
        return [self.hash32(t) for t in tokens]

    def to_ids(self, tokens: List[str], vocab_size: int = 50000) -> List[int]:
        """以 SHA1 的 32-bit 雜湊將 token 決定性映射到整數 ID（可能碰撞）。"""
        hashes = self.to_hash32(tokens)
        return self.to_ids_from_hashes(hashes, vocab_size=vocab_size)

    def to_ids_from_hashes(
        self, hashes: List[int], vocab_size: int = 50000
    ) -> List[int]:
        """將預先計算的 32-bit 雜湊值映射成 vocab ID。"""
        return [h % vocab_size for h in hashes]


class HashingEmbedder:
    """
    以 hashing trick 建立固定長度向量，不需任何外部模型：
    - 將 token 經 SHA1 後映射到固定維度
    - 向量值為計數（bag-of-tokens）
    """

    def __init__(self, dim: int = 128):
        self.dim = dim

    def embed_tokens(self, tokens: List[str]) -> List[float]:
        """為了相容保留：內部仍會計算雜湊（可能重複計算）。"""
        hashes = [
            int.from_bytes(hashlib.sha1(t.encode("utf-8")).digest()[:4], "little")
            for t in tokens
        ]
        return self.embed_hashes(hashes)

    def embed_hashes(self, hashes: List[int]) -> List[float]:
        """使用預先計算的 32-bit 雜湊值映射到固定維度。"""
        vec = [0.0] * self.dim
        for h in hashes:
            idx = h % self.dim
            vec[idx] += 1.0
        return vec


class DenseProjector:
    """
    使用隨機投影將稀疏計數向量壓縮為稠密低維向量。
    - 矩陣元素採用 Rademacher 分佈（+1/-1），可重現（固定 seed）。
    - 投影後做 L2 normalize。
    """

    def __init__(self, k: int, dim: int, seed: int = 42):
        self.k = k
        self.dim = dim
        self.seed = seed
        rng = random.Random(seed)
        # 建立 k x dim 的投影矩陣，元素為 +1 或 -1
        self.matrix: List[List[float]] = []
        for _ in range(k):
            row = [1.0 if rng.random() < 0.5 else -1.0 for _ in range(dim)]
            self.matrix.append(row)

    def project(self, vec: List[float]) -> List[float]:
        # y = R x  （R: k x dim）
        y = [0.0] * self.k
        for i in range(self.k):
            row = self.matrix[i]
            s = 0.0
            for a, b in zip(row, vec):
                s += a * b
            y[i] = s
        # L2 normalize
        norm = math.sqrt(sum(v * v for v in y))
        if norm > 0:
            y = [v / norm for v in y]
        return y


class MockVectorDB:
    """
    超簡易向量資料庫（in-memory）：
    - add: 新增文件並建立向量
    - query: 將查詢文字 tokenize + embedding
    - search: 以 cosine similarity 做最近鄰檢索
    """

    def __init__(self, dim: int = 128, dense_k: Optional[int] = None, seed: int = 42):
        self.tokenizer = SimpleTokenizer()
        self.embedder = HashingEmbedder(dim=dim)
        self.projector = (
            DenseProjector(k=dense_k, dim=dim, seed=seed) if dense_k else None
        )
        self._docs: List[Document] = []
        self._vectors: List[List[float]] = []

    def add(self, doc: Union[Document, List[Document]]):
        docs = [doc] if isinstance(doc, Document) else doc
        for d in docs:
            tokens = self.tokenizer.tokenize(d.content)
            hashes = self.tokenizer.to_hash32(tokens)
            vec = self.embedder.embed_hashes(hashes)
            if self.projector is not None:
                vec = self.projector.project(vec)
            self._docs.append(d)
            self._vectors.append(vec)

    def query(self, text: str) -> dict:
        tokens = self.tokenizer.tokenize(text)
        hashes = self.tokenizer.to_hash32(tokens)
        qvec = self.embedder.embed_hashes(hashes)
        if self.projector is not None:
            qvec = self.projector.project(qvec)
        ids = self.tokenizer.to_ids_from_hashes(hashes)
        return {"query_vector": qvec, "tokens": tokens, "token_ids": ids}

    @staticmethod
    def _cosine_similarity(a: List[float], b: List[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a))
        nb = math.sqrt(sum(y * y for y in b))
        if na == 0 or nb == 0:
            return 0.0
        return dot / (na * nb)

    def search(self, query_vector: List[float], top_k: int = 5) -> List[Document]:
        scored = []
        for vec, doc in zip(self._vectors, self._docs):
            sim = self._cosine_similarity(query_vector, vec)
            scored.append((sim, doc))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored[:top_k]]


if __name__ == "__main__":
    # 測試範例
    test_text = "我喜歡黑色貓貓 meow!"
    tokenizer = SimpleTokenizer()

    tokens = tokenizer.tokenize(test_text)
    print("Tokens:", tokens)
    hashes = tokenizer.to_hash32(tokens)
    print("Token IDs:", tokenizer.to_ids_from_hashes(hashes))
    embedder = HashingEmbedder(dim=16)
    vector = embedder.embed_hashes(hashes)
    print("Sparse Vector (dim=16):", vector)
    # 稠密投影示範（k=8）
    projector = DenseProjector(k=8, dim=16, seed=7)
    dense_vec = projector.project(vector)
    print("Dense Vector (k=8):", dense_vec)

    # 建立 DB：可切換 dense_k=None（稀疏）或 dense_k=64（稠密投影）
    db = MockVectorDB(dim=128, dense_k=64, seed=123)
    db.add(
        [
            Document(id="1", content="測試這是一個測試文件"),
            Document(id="2", content="我喜歡貓咪咖啡廳"),
            Document(id="3", content="這是一個關於 Python 程式設計的文件"),
        ]
    )

    query_text = "我想找貓咪相關的資訊"
    query_result = db.query(query_text)
    print("Query Tokens:", query_result["tokens"])
    print("Query Token IDs:", query_result["token_ids"])
    retrieved_docs = db.search(query_result["query_vector"], top_k=2)

    for doc in retrieved_docs:
        print(f"Retrieved Document ID: {doc.id}, Content: {doc.content}")
