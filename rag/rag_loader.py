import os
import re

import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer


class RAGLoader:

    def __init__(self):
        base_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        self.csv_path = os.path.join(
            base_dir, "data", "tourism_places.csv"
        )
        self.db_path = os.path.join(base_dir, "vector_db")

        self.client = chromadb.PersistentClient(path=self.db_path)

        self.collection = self.client.get_or_create_collection(
            name="tourism"
        )

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def build_database(self):
        data = pd.read_csv(self.csv_path)

        if self.collection.count() > 0:
            return

        for index, row in data.iterrows():
            text = f"{row['Place']} : {row['Description']}"
            embedding = self.model.encode(text).tolist()

            self.collection.add(
                ids=[str(index)],
                documents=[text],
                embeddings=[embedding],
            )

    def search(self, query):
        # Prioritize explicitly mentioned destinations.
        data = pd.read_csv(self.csv_path)
        matches = []

        for _, row in data.iterrows():
            place = str(row["Place"])

            pattern = (
                r"(?<!\w)"
                + re.escape(place)
                + r"(?!\w)"
            )

            if re.search(pattern, query, re.IGNORECASE):
                matches.append(
                    f"{place} : {row['Description']}"
                )

        if matches:
            return "\n".join(matches)

        # Use semantic search when no explicit destination matches.
        count = self.collection.count()

        if count == 0:
            return ""

        embedding = self.model.encode(query).tolist()

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=min(3, count),
        )

        documents = results.get("documents")

        if not documents or not documents[0]:
            return ""

        return "\n".join(documents[0])
