"""Minimal status page for the Telegram bot (Alloy preview)."""
import html, json, os, re, urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(os.environ.get("STATUS_PORT", "3000"))

def token():
    t = os.environ.get("TELEGRAM_BOT_TOKEN")
    if t:
        return t
    m = re.search(r'TELEGRAM_BOT_TOKEN\s*=\s*"([^"]+)"', open("/workspace/python.py").read())
    return m.group(1) if m else ""

def get_me():
    try:
        with urllib.request.urlopen(f"https://api.telegram.org/bot{token()}/getMe", timeout=10) as r:
            return json.load(r)
    except Exception as e:
        body = getattr(e, "read", lambda: b"")()
        try:
            return json.loads(body)
        except Exception:
            return {"ok": False, "description": type(e).__name__}

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        info = get_me()
        ok = info.get("ok")
        if ok:
            r = info["result"]
            detail = f"Connected as <b>@{html.escape(r.get('username',''))}</b> ({html.escape(r.get('first_name',''))})"
        else:
            detail = "Telegram API check failed: " + html.escape(str(info.get("description", "unknown")))
        color = "#15803d" if ok else "#b91c1c"
        page = f"""<!doctype html><html><head><meta charset=utf-8><title>Telegram Gemini Bot</title></head>
<body style="font-family:system-ui,sans-serif;background:#f8fafc;color:#0f172a;display:flex;justify-content:center;padding:48px">
<div style="max-width:560px;width:100%;background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:32px;display:flex;flex-direction:column;gap:16px">
<h1 style="margin:0">Telegram Gemini Bot</h1>
<p style="margin:0;color:#475569">Polling bot that replies to text messages using Gemini (gemini-1.5-flash).</p>
<div style="padding:12px 16px;border-radius:8px;background:#f1f5f9"><span style="color:{color};font-weight:600">{'● Online' if ok else '● Offline'}</span> &mdash; {detail}</div>
<p style="margin:0;color:#64748b;font-size:14px">Bot runs in the <code>bot</code> compose service; logs: <code>docker compose -f docker-compose.alloy.yaml logs -f bot</code></p>
</div></body></html>"""
        b = page.encode()
        self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)

HTTPServer(("0.0.0.0", PORT), H).serve_forever()
