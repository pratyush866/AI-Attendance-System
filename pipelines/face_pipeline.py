import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st

from pipelines.database.db import get_all_students

DEFAULT_FACE_THRESHOLD = 0.52

def get_threshold_label(threshold: float) -> str:
    """Helper to return an intuitive status label for a given threshold value."""
    if threshold < 0.46:
        return "🔒 Strict (High Precision - Minimizes False Matches)"
    elif threshold <= 0.58:
        return "🎯 Balanced / Recommended (Optimal for Classroom Photos)"
    else:
        return "📸 Lenient (Higher Recall - Tolerates Angles & Lighting)"

@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector() 

    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, facerec

def get_face_embeddings(image_np):
    detector, sp, facerec = load_dlib_models()
    faces = detector(image_np, 1)

    encodings = []
    for face in faces:
        shape = sp(image_np, face)
        face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1) # 128 embedding
        encodings.append(np.array(face_descriptor, dtype=np.float64))
    return encodings

@st.cache_resource
def get_trained_model():
    X = []
    y = []

    student_db = get_all_students()

    if not student_db:
        return None
    
    for student in student_db:
        embedding = student.get('face_embedding')
        if embedding:
            if isinstance(embedding, str):
                try:
                    import json
                    embedding = json.loads(embedding)
                except Exception:
                    continue
            X.append(np.array(embedding, dtype=np.float64))
            y.append(student.get('student_id'))

    if len(X) == 0:
        return None
    
    clf = None
    all_unique_ids = sorted(list(set(y)))
    if len(all_unique_ids) >= 2:
        try:
            clf = SVC(kernel='linear', probability=True, class_weight='balanced')
            clf.fit(X, y)
        except Exception:
            clf = None

    return {'clf': clf, 'X': X, 'y': y}

def train_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)

def predict_attendance(class_image_np, threshold=None):
    """
    Performs face detection and nearest-neighbor metric matching on a classroom image.
    
    Args:
        class_image_np (np.ndarray): Image as a numpy RGB array.
        threshold (float, optional): Nearest-neighbor Euclidean distance cutoff.
                                     Faces with distance <= threshold are recognized.
                                     Defaults to session setting or DEFAULT_FACE_THRESHOLD (0.52).

    Returns:
        tuple: (detected_students_dict, all_student_ids, num_faces_found)
               detected_students_dict maps student_id -> {
                   'distance': float,
                   'confidence': float, # 0-100%
                   'threshold': float,
                   'matched': True
               }
    """
    encodings = get_face_embeddings(class_image_np)
    detected_student = {}

    model_data = get_trained_model()
    if not model_data or not model_data.get('X'):
        return detected_student, [], len(encodings)

    # Determine effective threshold
    if threshold is None:
        try:
            threshold = float(st.session_state.get('face_match_threshold', DEFAULT_FACE_THRESHOLD))
        except Exception:
            threshold = DEFAULT_FACE_THRESHOLD

    X_train = np.array(model_data['X'], dtype=np.float64)  # (N, 128)
    y_train = np.array(model_data['y'])                   # (N,)
    all_students = sorted(list(set(y_train.tolist())))

    for encoding in encodings:
        if len(X_train) == 0:
            continue

        # Nearest-Neighbor matching across all enrolled face embeddings (Euclidean distance)
        distances = np.linalg.norm(X_train - encoding, axis=1)
        best_idx = int(np.argmin(distances))
        best_distance = float(distances[best_idx])
        matched_student_id = int(y_train[best_idx])

        # If closest enrolled embedding is within the tuned threshold
        if best_distance <= threshold:
            # Map distance to intuitive confidence percentage:
            # 0.0 distance = 100% confidence; distance at threshold = 60% confidence
            denom = max(threshold * 2.0, 0.01)
            confidence = max(10.0, min(99.9, (1.0 - (best_distance / denom)) * 100.0))

            # If student was detected in multiple faces/crops, keep the best (closest) match
            if matched_student_id not in detected_student or best_distance < detected_student[matched_student_id]['distance']:
                detected_student[matched_student_id] = {
                    'distance': round(best_distance, 3),
                    'confidence': round(confidence, 1),
                    'threshold': round(threshold, 3),
                    'matched': True
                }

    return detected_student, all_students, len(encodings)
