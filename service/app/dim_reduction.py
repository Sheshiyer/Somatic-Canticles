"""
Dimensionality reduction for pgvector compatibility.

pgvector HNSW/IVFFlat indexes support max 2000 dimensions.
Our embeddings are 4096-dim (nv-embed-v1) and 2048-dim (nemotron-vl).
This module provides PCA-based compression to fit within the limit.

Target dimension: 1536 (within 2000 limit, with headroom for future models).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from numpy.typing import NDArray

TARGET_DIM = 1536


class VectorReducer:
    """
    PCA-based dimensionality reducer.

    Fits on seed vectors, then transforms new vectors.
    Stores the projection matrix for consistent transformation.
    """

    def __init__(self, source_dim: int, target_dim: int = TARGET_DIM):
        self.source_dim = source_dim
        self.target_dim = min(target_dim, source_dim)
        self.projection_matrix: NDArray | None = None
        self.mean: NDArray | None = None
        self._fitted = False

    def fit(self, vectors: NDArray) -> None:
        """
        Fit PCA projection matrix on a corpus of vectors.

        Args:
            vectors: (N, source_dim) array of vectors
        """
        if vectors.ndim != 2 or vectors.shape[1] != self.source_dim:
            raise ValueError(
                f"Expected vectors of shape (N, {self.source_dim}), got {vectors.shape}"
            )

        self.mean = vectors.mean(axis=0)
        centered = vectors - self.mean

        cov = np.cov(centered, rowvar=False)

        eigenvalues, eigenvectors = np.linalg.eigh(cov)

        sorted_indices = np.argsort(eigenvalues)[::-1]
        eigenvectors = eigenvectors[:, sorted_indices]

        self.projection_matrix = eigenvectors[:, : self.target_dim]
        self._fitted = True

    def transform(self, vectors: NDArray) -> NDArray:
        """Transform vectors from source_dim to target_dim."""
        if not self._fitted or self.projection_matrix is None or self.mean is None:
            raise RuntimeError("Reducer not fitted. Call fit() first.")

        if vectors.ndim == 1:
            vectors = vectors.reshape(1, -1)

        centered = vectors - self.mean
        return centered @ self.projection_matrix

    def fit_transform(self, vectors: NDArray) -> NDArray:
        """Fit on vectors, then transform them."""
        self.fit(vectors)
        return self.transform(vectors)

    def to_json(self) -> str:
        """Serialize projection matrix and mean to JSON string."""
        if self.projection_matrix is None or self.mean is None:
            raise RuntimeError("Nothing to serialize. Call fit() first.")
        data = {
            "source_dim": self.source_dim,
            "target_dim": self.target_dim,
            "projection_matrix": self.projection_matrix.tolist(),
            "mean": self.mean.tolist(),
        }
        return json.dumps(data)

    @classmethod
    def from_json(cls, json_str: str) -> "VectorReducer":
        """Deserialize from JSON string (from DB)."""
        data = json.loads(json_str)
        reducer = cls(source_dim=data["source_dim"], target_dim=data["target_dim"])
        reducer.projection_matrix = np.array(data["projection_matrix"])
        reducer.mean = np.array(data["mean"])
        reducer._fitted = True
        return reducer

    def save(self, path: Path) -> None:
        """Save projection matrix and mean to disk."""
        if self.projection_matrix is None or self.mean is None:
            raise RuntimeError("Nothing to save. Call fit() first.")
        data = {
            "source_dim": self.source_dim,
            "target_dim": self.target_dim,
            "projection_matrix": self.projection_matrix.tolist(),
            "mean": self.mean.tolist(),
        }
        path.write_text(json.dumps(data), encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> "VectorReducer":
        """Load projection matrix and mean from disk."""
        data = json.loads(path.read_text(encoding="utf-8"))
        reducer = cls(source_dim=data["source_dim"], target_dim=data["target_dim"])
        reducer.projection_matrix = np.array(data["projection_matrix"])
        reducer.mean = np.array(data["mean"])
        reducer._fitted = True
        return reducer


def build_reducer_from_pilot(
    vectors_path: Path, target_dim: int = TARGET_DIM
) -> VectorReducer:
    """
    Build a reducer from pilot seed vectors.

    Args:
        vectors_path: Path to .npy file with seed vectors
        target_dim: Target dimension (default 1536)
    """
    vectors = np.load(str(vectors_path))
    source_dim = vectors.shape[1]
    reducer = VectorReducer(source_dim=source_dim, target_dim=target_dim)
    reducer.fit(vectors)
    return reducer