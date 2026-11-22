import os
import base64
from functools import lru_cache

@lru_cache(maxsize=32)
def get_image_base64(image_path):
    """
    Reads an image file and returns base64 encoded data URI.
    Caches results in memory for instantaneous rendering.
    """
    if not os.path.exists(image_path):
        return None
    try:
        with open(image_path, "rb") as f:
            data = f.read()
        ext = os.path.splitext(image_path)[1].lower().replace(".", "")
        if ext in ["jpg", "jpeg"]:
            mime = "image/jpeg"
        elif ext == "svg":
            mime = "image/svg+xml"
        else:
            mime = "image/png"
        encoded = base64.b64encode(data).decode()
        return f"data:{mime};base64,{encoded}"
    except Exception:
        return None

