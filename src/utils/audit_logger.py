import json
import uuid
import os
from datetime import datetime, timezone


class AuditLogger:
    def __init__(self, log_path: str = "audit_trail.jsonl"):
        self.log_path = log_path

    def log(self, record: dict) -> str:
        audit_id = str(uuid.uuid4())
        entry = {
            "audit_id": audit_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **record,
        }
        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
        return audit_id

    def read_all(self) -> list:
        if not os.path.exists(self.log_path):
            return []
        with open(self.log_path) as f:
            return [json.loads(line) for line in f if line.strip()]
