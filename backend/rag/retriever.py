from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from backend.utils.config import KB_DIR


class KnowledgeBase:
    def __init__(self):
        self.documents = []
        self._load()

    def _load(self):
        self.documents = []
        for path in KB_DIR.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".txt", ".md", ".json"}:
                text = path.read_text(encoding="utf-8", errors="ignore")
                for idx, chunk in enumerate(self._chunks(text)):
                    self.documents.append(
                        {
                            "source": str(path.relative_to(KB_DIR)),
                            "chunk": idx,
                            "text": chunk,
                        }
                    )
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = (
            self.vectorizer.fit_transform([d["text"] for d in self.documents])
            if self.documents
            else None
        )

    @staticmethod
    def _chunks(text, size=900):
        words = text.split()
        return [" ".join(words[i : i + size]) for i in range(0, len(words), size)] or [
            ""
        ]

    def retrieve(self, query: str, k: int = 4):
        if not self.documents or self.matrix is None:
            return []
        q = self.vectorizer.transform([query])
        scores = cosine_similarity(q, self.matrix)[0]
        indexes = scores.argsort()[::-1][:k]
        return [
            {**self.documents[i], "score": round(float(scores[i]), 4)}
            for i in indexes
            if scores[i] > 0
        ]
