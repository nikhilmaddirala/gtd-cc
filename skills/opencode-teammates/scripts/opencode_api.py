from __future__ import annotations

import json
import os
import urllib.error
import urllib.request


class OpenCodeAPIError(RuntimeError):
    pass


def server_url() -> str:
    return os.environ.get("OPENCODE_SERVER_URL", "http://127.0.0.1:4098").rstrip("/")


def _request(
    method: str, path: str, body: dict | None = None, timeout: int = 20
) -> dict | list:
    base = server_url()
    url = f"{base}{path}"
    payload = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=payload, method=method)
    req.add_header("content-type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        detail = ""
        try:
            detail = exc.read().decode("utf-8", errors="replace")
        except Exception:
            detail = ""
        raise OpenCodeAPIError(
            f"opencode API {method} {path} failed ({exc.code}): {detail[:200]}"
        )
    except urllib.error.URLError as exc:
        raise OpenCodeAPIError(f"cannot reach opencode server at {base}: {exc.reason}")


def health() -> dict:
    data = _request("GET", "/global/health")
    if not isinstance(data, dict):
        raise OpenCodeAPIError("invalid /global/health response")
    return data


def create_session(title: str, permissions: list[dict] | None = None) -> str:
    body: dict = {"title": title}
    if permissions is not None:
        body["permission"] = permissions
    data = _request("POST", "/session", body)
    if not isinstance(data, dict) or not data.get("id"):
        raise OpenCodeAPIError("session creation returned no id")
    return str(data["id"])


def _model_obj(model: str) -> dict | None:
    model = model.strip()
    if not model:
        return None
    if "/" not in model:
        return None
    provider_id, model_id = model.split("/", 1)
    provider_id = provider_id.strip()
    model_id = model_id.strip()
    if not provider_id or not model_id:
        return None
    return {"providerID": provider_id, "modelID": model_id}


def prompt_async(
    session_id: str, text: str, agent: str = "build", model: str = ""
) -> None:
    body: dict = {"parts": [{"type": "text", "text": text}]}
    if agent:
        body["agent"] = agent
    model_obj = _model_obj(model)
    if model_obj:
        body["model"] = model_obj
    _request("POST", f"/session/{session_id}/prompt_async", body)


def abort_session(session_id: str) -> None:
    _request("POST", f"/session/{session_id}/abort")


def delete_session(session_id: str) -> None:
    _request("DELETE", f"/session/{session_id}")


def session_status(session_id: str) -> str:
    data = _request("GET", "/session/status")
    if not isinstance(data, dict):
        return "unknown"
    value = data.get(session_id)
    if isinstance(value, dict):
        state = value.get("type")
        return state if isinstance(state, str) else "unknown"
    if isinstance(value, str):
        return value
    return "unknown"
