import numpy as np
import io
import librosa
import streamlit as st

@st.cache_resource
def load_voice_encoder():
    from resemblyzer import VoiceEncoder
    return VoiceEncoder()

def _extract_audio_bytes(audio_source):
    if audio_source is None:
        return None
    if isinstance(audio_source, (bytes, bytearray)):
        return bytes(audio_source)
    if hasattr(audio_source, 'getvalue'):
        return audio_source.getvalue()
    if hasattr(audio_source, 'read'):
        return audio_source.read()
    return None

def get_voice_embedding(audio_source):
    """Extract 256-dimensional voice embedding vector from raw audio bytes or Streamlit audio object."""
    try:
        raw_bytes = _extract_audio_bytes(audio_source)
        if not raw_bytes or len(raw_bytes) < 100:
            return None

        from resemblyzer import preprocess_wav
        encoder = load_voice_encoder()

        # Load audio into 16kHz mono float array
        audio, sr = librosa.load(io.BytesIO(raw_bytes), sr=16000)
        if len(audio) < 160: # less than 10ms
            return None

        wav = preprocess_wav(audio)
        if len(wav) == 0:
            return None

        embedding = encoder.embed_utterance(wav)
        # Normalize embedding vector
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm

        return embedding.tolist()
    except Exception as e:
        print(f"[Voice Pipeline Error]: {e}")
        return None

def identify_speaker(new_embedding, candidates_dict, threshold=0.65):
    """Match a voice embedding against a dictionary of student embeddings {student_id: [vector]}."""
    if not new_embedding or not candidates_dict:
        return None, 0.0

    emb_arr = np.array(new_embedding, dtype=np.float32)
    norm = np.linalg.norm(emb_arr)
    if norm > 0:
        emb_arr = emb_arr / norm

    best_sid = None
    best_score = -1.0

    for sid, stored_embedding in candidates_dict.items():
        if stored_embedding:
            try:
                if isinstance(stored_embedding, str):
                    import json
                    stored_embedding = json.loads(stored_embedding)
                stored_arr = np.array(stored_embedding, dtype=np.float32)
                s_norm = np.linalg.norm(stored_arr)
                if s_norm > 0:
                    stored_arr = stored_arr / s_norm
                
                # Cosine similarity
                similarity = float(np.dot(emb_arr, stored_arr))
                if similarity > best_score:
                    best_score = similarity
                    best_sid = sid
            except Exception:
                continue

    if best_score >= threshold:
        return best_sid, best_score

    return None, max(best_score, 0.0)

def process_bulk_audio(audio_source, candidates_dict, threshold=0.60):
    """Segment classroom audio and match each speaker segment against candidate student embeddings."""
    try:
        raw_bytes = _extract_audio_bytes(audio_source)
        if not raw_bytes or len(raw_bytes) < 100:
            return {}

        from resemblyzer import preprocess_wav
        encoder = load_voice_encoder()

        audio, sr = librosa.load(io.BytesIO(raw_bytes), sr=16000)
        if len(audio) < sr * 0.3:
            return {}

        # Split continuous audio into active speech intervals
        segments = librosa.effects.split(audio, top_db=25)
        identified_results = {}

        for start, end in segments:
            # Skip very short audio blips (< 0.4 seconds)
            if (end - start) < sr * 0.4:
                continue

            segment_audio = audio[start:end]
            wav = preprocess_wav(segment_audio)
            if len(wav) == 0:
                continue

            embedding = encoder.embed_utterance(wav)
            norm = np.linalg.norm(embedding)
            if norm > 0:
                embedding = embedding / norm

            sid, score = identify_speaker(embedding.tolist(), candidates_dict, threshold)
            if sid:
                if sid not in identified_results or score > identified_results[sid]:
                    identified_results[sid] = score

        return identified_results
    except Exception as e:
        print(f"[Bulk Voice Processing Error]: {e}")
        return {}