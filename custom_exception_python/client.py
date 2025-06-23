import uuid
import sys
import json
import requests
from datetime import datetime, timezone
from .config import Config
from .utils import build_stacktrace


class ErrorClient:
    @staticmethod
    def build_payload(exc: Exception, tb, level="error"):
        event_id = uuid.uuid4().hex
        return {
            "event_id": event_id,
            "timestamp": datetime.utcnow().replace(tzinfo=timezone.utc).isoformat(),
            "level": level,
            "exception": {
                "values": [{
                    "type": type(exc).__name__,
                    "value": str(exc),
                    "mechanism": {"type": "generic", "handled": True},
                    "stacktrace": build_stacktrace(tb)
                }]
            },
            "platform": "python",
            "release": Config.release or "dev",
            "environment": Config.environment or "production",
            "server_name": Config.server_name,
            "sdk": {
                "name": Config.sdk_name,
                "version": Config.sdk_version
            },
            "contexts": {
                "runtime": {
                    "name": sys.implementation.name,
                    "version": sys.version.split()[0],
                    "build": sys.version
                }
            },
            "extra": {"sys.argv": sys.argv},
            "modules": {"requests": requests.__version__}
        }

    @staticmethod
    def send(payload: dict):
        dsn = Config.parsed_dsn
        if not dsn:
            return

        envelope = {
            "envelope_headers": {
                "event_id": payload["event_id"],
                "sent_at": datetime.utcnow().replace(tzinfo=timezone.utc).isoformat(),
                "trace": {
                    "trace_id": uuid.uuid4().hex,
                    "environment": Config.environment or "production",
                    "release": Config.release or "dev",
                    "public_key": dsn["public_key"],
                    "sample_rate": "1.0"
                }
            },
            "items": [{
                "item_header": {
                    "type": "event",
                    "content_type": "application/json",
                    "length": len(json.dumps(payload))
                },
                "payload": payload
            }]
        }

        url = f"{dsn['protocol']}://{dsn['host']}/{dsn['project_id']}"
        try:
            requests.post(url, json=envelope, timeout=5)
        except Exception:
            pass
