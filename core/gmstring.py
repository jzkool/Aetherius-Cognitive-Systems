import json
import hashlib
from datetime import datetime

def generate_gmstring(g, depth, parent_id, op_code):
    operands = [round(float(x), 12) for x in g.flatten()]
    
    payload = {
        "depth": depth,
        "parent_id": parent_id,
        "op_code": op_code,
        "operands": operands,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # Canonicalize
    canonical_json = json.dumps(payload, sort_keys=True, separators=(',', ':'))
    checksum = hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()
    
    payload["checksum"] = checksum
    return payload
