import chromadb
import uuid

class DBManager:
    def __init__(self, persist_directory="./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name="documents")

    def add_document(self, text, metadata=None):
        """
        Adds a document to the ChromaDB collection.
        """
        doc_id = str(uuid.uuid4())
        self.collection.add(
            documents=[text],
            metadatas=[metadata] if metadata else None,
            ids=[doc_id]
        )
        return doc_id

    def query_documents(self, query_text, n_results=3):
        """
        Queries the collection for relevant documents.
        """
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results['documents'][0] if results['documents'] else []
    
    def clear_database(self):
        self.client.delete_collection("documents")
        self.collection = self.client.get_or_create_collection(name="documents")
