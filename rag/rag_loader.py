import os
import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer


class RAGLoader:

    def __init__(self):

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        self.csv_path = os.path.join(base_dir, "data", "tourism_places.csv")
        self.db_path = os.path.join(base_dir, "vector_db")

        self.client = chromadb.PersistentClient(path=self.db_path)

        self.collection = self.client.get_or_create_collection(
            name="tourism"
        )

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def build_database(self):

        data = pd.read_csv(self.csv_path)

        # Database already exists
        if self.collection.count() > 0:
            return

        for index, row in data.iterrows():

            text = f"{row['Place']} : {row['Description']}"

            embedding = self.model.encode(text).tolist()

            self.collection.add(
                ids=[str(index)],
                documents=[text],
                embeddings=[embedding]
            )

    def search(self, query):

        embedding = self.model.encode(query).tolist()

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=1
        )

        if len(results["documents"][0]) == 0:
            return ""

        return results["documents"][0][0]