import platform

class Config:
    dsn = None
    release = None
    environment = None
    server_name = platform.node()
    sdk_name = "custom.python"
    sdk_version = "0.1.0"
    parsed_dsn = {}

    @classmethod
    def init(cls, dsn: str, release=None, environment=None):
        cls.dsn = dsn
        cls.release = release
        cls.environment = environment

        try:
            protocol, rest = dsn.split("//")
            public_key, rest = rest.split("@")
            host, project_id = rest.rsplit("/", 1)
            cls.parsed_dsn = {
                "protocol": protocol.rstrip(":"),
                "public_key": public_key,
                "host": host,
                "project_id": project_id
            }
        except Exception:
            raise ValueError("Invalid DSN format")
