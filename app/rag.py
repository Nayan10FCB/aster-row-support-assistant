from pathlib import Path
from typing import List, Dict
import re

import chromadb
import yaml
from sentence_transformers import SentenceTransformer


KNOWLEDGE_BASE_DIR = Path("knowledge-base")
CHROMA_DIR = Path("chroma_db")

COLLECTION_NAME = "aster_row_knowledge"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


class RAGSystem:

    def __init__(self):

        print("Loading embedding model...")

        self.embedding_model = SentenceTransformer(
            EMBEDDING_MODEL
        )

        self.chroma_client = chromadb.PersistentClient(
            path=str(CHROMA_DIR)
        )

        self.collection = (
            self.chroma_client.get_or_create_collection(
                name=COLLECTION_NAME
            )
        )

    def load_documents(self) -> List[Dict]:
        """Load all Markdown knowledge-base documents."""

        documents = []

        for file_path in sorted(
            KNOWLEDGE_BASE_DIR.glob("*.md")
        ):

            text = file_path.read_text(
                encoding="utf-8"
            )

            metadata, body = self._parse_front_matter(
                text
            )

            sections = self._split_into_sections(
                body
            )

            for section_number, section in enumerate(
                sections
            ):

                if not section["text"].strip():
                    continue

                documents.append(
                    {
                        "id": (
                            f"{file_path.stem}-"
                            f"{section_number}"
                        ),
                        "text": section["text"],
                        "filename": file_path.name,
                        "heading": section["heading"],
                        "metadata": metadata,
                    }
                )

        return documents

    def _parse_front_matter(self, text: str):
        """Extract YAML front matter."""

        if not text.startswith("---"):
            return {}, text

        match = re.match(
            r"^---\s*\n(.*?)\n---\s*\n(.*)$",
            text,
            re.DOTALL,
        )

        if not match:
            return {}, text

        metadata_text = match.group(1)
        body = match.group(2)

        metadata = yaml.safe_load(
            metadata_text
        ) or {}

        return metadata, body

    def _split_into_sections(self, text: str):
        """Split Markdown content using headings."""

        lines = text.splitlines()

        sections = []

        current_heading = "Document"
        current_lines = []

        for line in lines:

            if line.startswith("#"):

                if current_lines:

                    sections.append(
                        {
                            "heading": current_heading,
                            "text": "\n".join(
                                current_lines
                            ).strip(),
                        }
                    )

                current_heading = (
                    line.lstrip("#").strip()
                )

                current_lines = []

            else:

                current_lines.append(line)

        if current_lines:

            sections.append(
                {
                    "heading": current_heading,
                    "text": "\n".join(
                        current_lines
                    ).strip(),
                }
            )

        return sections

    def index_documents(self):
        """Create local embeddings and store them in ChromaDB."""

        documents = self.load_documents()

        if not documents:

            raise RuntimeError(
                "No knowledge-base documents found."
            )

        print(
            f"Found {len(documents)} sections."
        )

        ids = [
            document["id"]
            for document in documents
        ]

        texts = [
            document["text"]
            for document in documents
        ]

        print("Creating embeddings...")

        embeddings = self.embedding_model.encode(
            texts,
            show_progress_bar=True
        ).tolist()

        metadatas = []

        for document in documents:

            metadata = {
                **document["metadata"],
                "filename": document["filename"],
                "heading": document["heading"],
            }

            metadata = {
                key: str(value)
                for key, value in metadata.items()
                if value is not None
            }

            metadatas.append(metadata)

        self.collection.upsert(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        print(
            f"Indexed {len(documents)} "
            "knowledge-base sections."
        )

    def search(
        self,
        query: str,
        n_results: int = 5
    ):
        """
        Retrieve relevant ACTIVE knowledge-base sections.

        Superseded and draft documents are excluded.
        """

        query_embedding = self.embedding_model.encode(
            [query]
        )[0].tolist()

        # Retrieve more candidates first because some
        # results may be filtered out by document status.
        candidate_count = max(
            n_results * 3,
            10
        )

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=candidate_count,
            include=[
                "documents",
                "metadatas",
                "distances"
            ],
        )

        retrieved = []

        if not results.get("documents"):
            return retrieved

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for i in range(len(documents)):

            metadata = metadatas[i]

            status = str(
                metadata.get(
                    "status",
                    ""
                )
            ).lower().strip()

            # Only current/active documents are allowed.
            if status != "active":
                continue

            retrieved.append(
                {
                    "text": documents[i],
                    "metadata": metadata,
                    "distance": distances[i],
                }
            )

            if len(retrieved) >= n_results:
                break

        return retrieved