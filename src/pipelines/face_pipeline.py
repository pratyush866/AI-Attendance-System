import dlib
import numpy as np
import face_recognition_models
import streamlit as st
import logging
from src.database.db import get_all_students

@st.cache_resource
def load_dlib_models():
    """
    Load pre-trained dlib face detector, 68-point shape predictor,
    and 128-dimensional deep metric ResNet face recognition model.
    """
    detector = dlib.get_frontal_face_detector()
    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )
    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )
    return detector, sp, facerec


def get_face_embeddings(image_np, upsample=1):
    """
    Detect faces in an image and compute 128-d embeddings for each detected face.
    Returns: list of (embedding_np, face_rectangle)
    """
    try:
        detector, sp, facerec = load_dlib_models()
        # upsample: 1 for normal photos, 2 for distant/classroom photos
        faces = detector(image_np, upsample)
        encodings = []

        for face in faces:
            shape = sp(image_np, face)
            face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1)
            encodings.append(np.array(face_descriptor))
        return encodings
    except Exception as e:
        logging.error(f"Error in get_face_embeddings: {e}")
        return []


def compute_similarity(emb1, emb2):
    """
    Computes both Euclidean distance (norm) and Cosine similarity.
    For dlib 128-d embeddings:
    - Euclidean Distance < 0.60 indicates a true positive face match.
    - Cosine Similarity > 0.65 indicates high confidence.
    """
    e1 = np.array(emb1)
    e2 = np.array(emb2)
    dist = float(np.linalg.norm(e1 - e2))
    # Normalized cosine similarity
    dot = np.dot(e1, e2)
    norm = np.linalg.norm(e1) * np.linalg.norm(e2)
    cos_sim = float(dot / norm) if norm > 0 else 0.0
    return dist, cos_sim


def match_face_against_candidates(face_encoding, candidates, distance_threshold=0.58):
    """
    Compare a single detected face against a list of candidate students.
    Candidates format: [{'student_id': 1, 'name': 'Akash', 'face_embedding': [...]}, ...]
    Returns: (best_student, best_distance, best_similarity) or (None, None, None)
    """
    best_candidate = None
    min_dist = 999.0
    best_similarity = 0.0

    for cand in candidates:
        cand_emb = cand.get('face_embedding')
        if not cand_emb:
            continue
        dist, cos_sim = compute_similarity(face_encoding, cand_emb)
        if dist < min_dist:
            min_dist = dist
            best_similarity = cos_sim
            best_candidate = cand

    if min_dist <= distance_threshold and best_candidate:
        return best_candidate, min_dist, best_similarity
    return None, min_dist, best_similarity


def predict_attendance(class_image_np, candidate_students=None, distance_threshold=0.58):
    """
    Detects all faces in a classroom photo and matches them directly against
    the list of candidates (or all students if none provided).
    Uses vector distance matching (eliminates fragile 1-sample SVM).
    Returns:
    - detected_students: dict {student_id: {'name': str, 'dist': float, 'similarity': float}}
    - candidate_ids: list of all candidate student IDs
    - total_faces_in_photo: int
    """
    if candidate_students is None:
        candidate_students = get_all_students()

    candidate_ids = [c['student_id'] for c in candidate_students]
    encodings = get_face_embeddings(class_image_np, upsample=1)

    # If few faces detected in large photo, retry with upsample=2 for small/back-row faces
    if len(encodings) == 0 and class_image_np.shape[0] > 600:
        encodings = get_face_embeddings(class_image_np, upsample=2)

    detected_students = {}

    for encoding in encodings:
        matched_student, dist, sim = match_face_against_candidates(
            encoding, candidate_students, distance_threshold=distance_threshold
        )
        if matched_student:
            sid = matched_student['student_id']
            # If already detected, keep the best (lowest distance) match
            if sid not in detected_students or dist < detected_students[sid]['dist']:
                detected_students[sid] = {
                    'name': matched_student['name'],
                    'dist': dist,
                    'similarity': sim
                }

    return detected_students, candidate_ids, len(encodings)


def verify_student_selfie(selfie_image_np, registered_embedding, threshold=0.58):
    """
    Verifies that:
    1. There is exactly one face in the selfie.
    2. The face matches the registered student face embedding.
    Returns: (is_valid, is_match, score_or_error_msg)
    """
    encodings = get_face_embeddings(selfie_image_np, upsample=1)
    if len(encodings) == 0:
        return False, False, "No face detected in selfie! Please face the camera with good lighting."
    if len(encodings) > 1:
        return False, False, "Multiple faces detected! Please ensure only your face is visible."

    if not registered_embedding:
        # If student has not enrolled their face before, this selfie becomes their enrolled face
        return True, True, 1.0

    dist, sim = compute_similarity(encodings[0], registered_embedding)
    is_match = dist <= threshold
    if is_match:
        confidence = max(0.0, min(1.0, 1.0 - (dist / threshold) * 0.5))
        return True, True, round(confidence, 2)
    else:
        return True, False, f"Face mismatch! (Confidence too low: dist={dist:.2f}, required <= {threshold})"


def train_classifier():
    """Kept for backward compatibility with old references."""
    st.cache_resource.clear()
    return True
