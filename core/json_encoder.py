import json
import numpy as np


class AetheriusJSONEncoder(json.JSONEncoder):
    """
    Custom JSON encoder that handles numpy types, sets, and other
    non-serializable objects produced by the geometric engine.
    Prevents TypeError crashes during persistent memory saves.
    """
    def default(self, obj):
        # numpy integer types
        if isinstance(obj, (np.integer,)):
            return int(obj)
        # numpy floating types
        if isinstance(obj, (np.floating,)):
            return float(obj)
        # numpy arrays -> nested lists
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        # numpy booleans
        if isinstance(obj, np.bool_):
            return bool(obj)
        # Python sets -> lists
        if isinstance(obj, set):
            return list(obj)
        # numpy void (structured array elements)
        if isinstance(obj, np.void):
            return None
        return super().default(obj)


def safe_json_dump(data, file_handle, **kwargs):
    """Convenience wrapper that always uses AetheriusJSONEncoder."""
    json.dump(data, file_handle, cls=AetheriusJSONEncoder, **kwargs)
