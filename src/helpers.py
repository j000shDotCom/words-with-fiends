def _log_request_status(r, *args, **kwargs):
    parts = [r.status_code, r.request.method, r.request.url]
    if r.request.body:
        parts.append(r.request.body)
    print(*parts)

    if not r.ok:
        parts.append(r.text)
        raise ValueError('Request Failed: ', *parts)

def _wrap_response(r, *args, **kwargs):
    pass
