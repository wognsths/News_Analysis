import numpy as np

def cos_sim(a, b):
    a, b = np.array(a), np.array(b)
    return (a / np.linalg.norm(a)).T @ (b / np.linalg.norm(b))

def cos_sim_matrix(A, t):
    """
    - A: (N, 1536) matrix
    Returns:
        - Cos-Similarity matrix (shape: (N, N))
    """
    norms = np.linalg.norm(A, axis=1, keepdims=True)
    normalized_A = A / norms
    return np.round(np.dot(normalized_A, normalized_A.T), t)
