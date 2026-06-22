"""Shared HTML skeleton (Pathfinders dark theme) for the results site."""

_CSS = """
:root { --bg:#111418; --card:#1a1f26; --text:#e8e8e8; --sub:#9aa0a6; --accent:#e10600; --good:#4caf50; }
* { box-sizing: border-box; }
body { margin:0; background:var(--bg); color:var(--text); font-family:system-ui,sans-serif; }
.wrap { max-width:1100px; margin:0 auto; padding:24px; }
h1,h2 { font-weight:600; }
.cards { display:grid; grid-template-columns:repeat(auto-fit,minmax(160px,1fr)); gap:12px; }
.card { background:var(--card); border-radius:8px; padding:12px; }
.card .label { color:var(--sub); font-size:12px; }
.card .big { font-size:22px; font-weight:700; }
table { width:100%; border-collapse:collapse; font-size:13px; }
th,td { text-align:left; padding:6px 8px; border-bottom:1px solid #2a2f36; }
th { color:var(--sub); font-weight:500; }
a { color:#636EFA; text-decoration:none; }
.good { color:var(--good); }
.tabs { display:flex; gap:6px; margin:12px 0; flex-wrap:wrap; }
.tab { background:var(--card); color:var(--sub); padding:4px 10px; border-radius:4px; cursor:pointer; }
.tab.active { background:var(--accent); color:#fff; }
.panel { display:none; } .panel.active { display:block; }
"""

_TAB_JS = """
function showTab(id){
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  document.querySelectorAll('.panel').forEach(p=>p.classList.remove('active'));
  document.getElementById('tab-'+id).classList.add('active');
  document.getElementById('panel-'+id).classList.add('active');
}
"""


def page(title: str, body: str, *, head_extra: str = "") -> str:
    """Wrap body in a full HTML document with the shared theme."""
    return (
        "<!DOCTYPE html>\n"
        '<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>{title}</title><style>{_CSS}</style>{head_extra}"
        f"<script>{_TAB_JS}</script></head>"
        f'<body><div class="wrap">{body}</div></body></html>'
    )
