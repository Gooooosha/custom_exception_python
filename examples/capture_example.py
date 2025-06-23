from custom_exception_python import init, capture_exception

init("http://6c2ccd2b-6826-4cf5-9297-72d26cb70d04@127.0.0.1:8039/0")

try:
    1 / 0
except Exception as e:
    capture_exception(e, level="high")
