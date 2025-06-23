import traceback

def build_stacktrace(tb):
    stack = traceback.extract_tb(tb)
    frames = []
    for frame in stack:
        try:
            with open(frame.filename, encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except Exception:
            lines = []

        lineno = frame.lineno - 1
        pre_context = lines[max(0, lineno - 5):lineno]
        context_line = lines[lineno].strip() if 0 <= lineno < len(lines) else ""
        post_context = lines[lineno + 1:lineno + 6]

        frames.append({
            "filename": frame.filename.split("/")[-1],
            "abs_path": frame.filename,
            "function": frame.name,
            "module": frame.name,
            "lineno": frame.lineno,
            "pre_context": [line.strip() for line in pre_context],
            "context_line": context_line,
            "post_context": [line.strip() for line in post_context],
            "in_app": True
        })

    return {"frames": frames}
