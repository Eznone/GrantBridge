"""
FAISS vector store for semantic search.
"""

import logging
import pickle
from typing import List, Tuple, Optional, Dict, Any
from pathlib import Path

import numpy as np

logger = logging.getLogger(__name__)


class VectorStore:
    """
    FAISS-based vector store for semantic similarity search.
    """

    def __init__(self, dimension: int = 768, index_path: str = None):
        """
        Initialize the vector store.

        Args:
            dimension: Embedding dimension (default: 768 for Slate)
            index_path: Path to save/load the index
        """
        self.dimension = dimension
        self.index_path = index_path or "data/faiss_index.pkl"
        self.index = None
        self.id_map = {}  # Maps FAISS index to grant/org IDs
        self.metadata = {}  # Stores metadata for each item

        # Try to import FAISS
        try:
            import faiss

            self.faiss = faiss
            self._initialize_index()
        except ImportError:
            logger.warning(
                "FAISS not installed. Install with: "
                "pip install faiss-cpu (or faiss-gpu)"
            )
            self.faiss = None

    def _initialize_index(self):
        """Initialize or load the FAISS index."""
        if self.faiss is None:
            return

        # Try to load existing index
        if Path(self.index_path).exists():
            try:
                self.load()
                logger.info(f"Loaded FAISS index from {self.index_path}")
                return
            except Exception as e:
                logger.warning(f"Could not load index: {e}")

        # Create new index
        self.index = self.faiss.IndexFlatL2(self.dimension)
        logger.info(f"Created new FAISS index (dimension={self.dimension})")

    def add_vectors(
        self,
        vectors: List[List[float]],
        ids: List[int],
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> bool:
        """
        Add vectors to the index.

        Args:
            vectors: List of embedding vectors
            ids: List of corresponding IDs (grant IDs, org IDs, etc.)
            metadata: Optional metadata for each vector

        Returns:
            True if successful, False otherwise
        """
        if self.faiss is None or self.index is None:
            logger.error("FAISS not available")
            return False

        try:
            # Convert to numpy array
            vectors_np = np.array(vectors, dtype=np.float32)

            # Add to index
            start_idx = self.index.ntotal
            self.index.add(vectors_np)

            # Update ID mapping
            for i, item_id in enumerate(ids):
                faiss_idx = start_idx + i
                self.id_map[faiss_idx] = item_id

                if metadata and i < len(metadata):
                    self.metadata[item_id] = metadata[i]

            logger.info(f"Added {len(vectors)} vectors to index")
            return True

        except Exception as e:
            logger.error(f"Error adding vectors: {e}")
            return False

    def search(
        self, query_vector: List[float], k: int = 10, return_metadata: bool = True
    ) -> List[Tuple[int, float, Optional[Dict[str, Any]]]]:
        """
        Search for similar vectors.

        Args:
            query_vector: Query embedding vector
            k: Number of results to return
            return_metadata: Whether to include metadata

        Returns:
            List of tuples (id, distance, metadata)
        """
        if self.faiss is None or self.index is None:
            logger.error("FAISS not available")
            return []

        try:
            # Convert to numpy array
            query_np = np.array([query_vector], dtype=np.float32)

            # Search
            distances, indices = self.index.search(query_np, k)

            # Convert results
            results = []
            for i, faiss_idx in enumerate(indices[0]):
                if faiss_idx == -1:  # No more results
                    break

                item_id = self.id_map.get(int(faiss_idx))
                if item_id is None:
                    continue

                distance = float(distances[0][i])

                # Convert distance to similarity score (0-100)
                # L2 distance: smaller is better, so invert it
                similarity = max(0, 100 - (distance * 10))

                meta = None
                if return_metadata:
                    meta = self.metadata.get(item_id)

                results.append((item_id, similarity, meta))

            return results

        except Exception as e:
            logger.error(f"Error searching vectors: {e}")
            return []

    def remove_vectors(self, ids: List[int]) -> bool:
        """
        Remove vectors by ID.

        Note: FAISS doesn't support efficient deletion,
        so this rebuilds the index without the specified IDs.

        Args:
            ids: List of IDs to remove

        Returns:
            True if successful, False otherwise
        """
        if self.faiss is None or self.index is None:
            logger.error("FAISS not available")
            return False

        try:
            # Get all vectors except those to remove
            vectors_to_keep = []
            ids_to_keep = []
            metadata_to_keep = []

            for faiss_idx, item_id in self.id_map.items():
                if item_id not in ids:
                    # Reconstruct vector from index
                    vector = self.index.reconstruct(int(faiss_idx))
                    vectors_to_keep.append(vector.tolist())
                    ids_to_keep.append(item_id)

                    if item_id in self.metadata:
                        metadata_to_keep.append(self.metadata[item_id])

            # Rebuild index
            self.index = self.faiss.IndexFlatL2(self.dimension)
            self.id_map = {}
            self.metadata = {}

            if vectors_to_keep:
                self.add_vectors(vectors_to_keep, ids_to_keep, metadata_to_keep)

            logger.info(f"Removed {len(ids)} vectors from index")
            return True

        except Exception as e:
            logger.error(f"Error removing vectors: {e}")
            return False

    def update_vector(
        self,
        item_id: int,
        vector: List[float],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Update a vector (remove old, add new).

        Args:
            item_id: ID of the item to update
            vector: New embedding vector
            metadata: Optional new metadata

        Returns:
            True if successful, False otherwise
        """
        # Remove old vector
        self.remove_vectors([item_id])

        # Add new vector
        return self.add_vectors([vector], [item_id], [metadata] if metadata else None)

    def save(self, path: Optional[str] = None) -> bool:
        """
        Save the index to disk.

        Args:
            path: Optional path to save to (uses self.index_path if None)

        Returns:
            True if successful, False otherwise
        """
        if self.faiss is None or self.index is None:
            logger.error("FAISS not available")
            return False

        save_path = path or self.index_path

        try:
            # Create directory if needed
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)

            # Save index and metadata
            data = {
                "index": self.faiss.serialize_index(self.index),
                "id_map": self.id_map,
                "metadata": self.metadata,
                "dimension": self.dimension,
            }

            with open(save_path, "wb") as f:
                pickle.dump(data, f)

            logger.info(f"Saved FAISS index to {save_path}")
            return True

        except Exception as e:
            logger.error(f"Error saving index: {e}")
            return False

    def load(self, path: Optional[str] = None) -> bool:
        """
        Load the index from disk.

        Args:
            path: Optional path to load from (uses self.index_path if None)

        Returns:
            True if successful, False otherwise
        """
        if self.faiss is None:
            logger.error("FAISS not available")
            return False

        load_path = path or self.index_path

        try:
            with open(load_path, "rb") as f:
                data = pickle.load(f)

            self.index = self.faiss.deserialize_index(data["index"])
            self.id_map = data["id_map"]
            self.metadata = data["metadata"]
            self.dimension = data["dimension"]

            logger.info(f"Loaded FAISS index from {load_path}")
            return True

        except Exception as e:
            logger.error(f"Error loading index: {e}")
            return False

    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the index.

        Returns:
            Dictionary with index statistics
        """
        if self.index is None:
            return {
                "available": False,
                "total_vectors": 0,
            }

        return {
            "available": True,
            "total_vectors": self.index.ntotal,
            "dimension": self.dimension,
            "index_path": self.index_path,
        }


# Made with Bob
