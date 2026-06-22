"""Render a single study JSON to an HTML dashboard string (B-layout: tabs + KPI)."""

import json

from template import page


def objective_formula(objective: dict) -> str:
    """Build a human formula from objective.terms, e.g. 'time + 0.005·e_y_rms'."""
    parts = []
    for term in objective.get("terms", []):
        w, m = term.get("weight", 1.0), term["metric"]
        parts.append(m if w == 1.0 and not parts else f"{w:g}·{m}")
    return " + ".join(parts) if parts else "?"


def _fmt(x, nd=3):
    return "—" if x is None else (f"{x:.{nd}f}" if isinstance(x, float) else str(x))


def _kpi(label: str, big: str, sub: str = "") -> str:
    return f'<div class="card"><div class="label">{label}</div><div class="big">{big}</div><div class="label">{sub}</div></div>'


def build_study_html(doc: dict) -> str:
    sid = doc["study_id"]
    best = doc.get("best_trial")
    dev = doc.get("develop_value")
    formula = objective_formula(doc.get("objective", {}))

    # KPI cards
    best_v = _fmt(best["value"]) if best else "—"
    delta = _fmt(best.get("delta_develop")) if best else "—"
    imp = doc.get("param_importance") or {}
    top2 = ", ".join(sorted(imp, key=imp.get, reverse=True)[:2]) or "—"
    kpis = "".join([
        _kpi("Best value", best_v, f"objective: {formula}"),
        _kpi("vs develop", delta, f"develop={_fmt(dev)}"),
        _kpi("valid rate", _fmt(doc.get("valid_rate")), f'{doc.get("n_valid")}/{doc.get("n_complete")}'),
        _kpi("key factors", top2, "importance top2"),
    ])

    # params table (dynamic keys from best trial or first trial)
    sample = (best or (doc["trials"][0] if doc["trials"] else {})) or {}
    pkeys = list((sample.get("params") or {}).keys())
    head = "".join(f"<th>{k}</th>" for k in pkeys)
    rows = ""
    for t in doc["trials"]:
        cls = (
            ""
            if (t.get("value") is not None and t["value"] < doc["objective"]["penalty"])
            else ' style="color:#9aa0a6"'
        )
        cells = "".join(f"<td>{_fmt((t.get('params') or {}).get(k), 0)}</td>" for k in pkeys)
        rows += f'<tr{cls}><td>{t["number"]}</td><td>{_fmt(t.get("value"))}</td><td>{t.get("exit_reason", "")}</td>{cells}</tr>'
    ptable = f"<table><tr><th>#</th><th>value</th><th>exit</th>{head}</tr>{rows}</table>"

    # data for the score-progression chart (plotly via CDN)
    chart_data = [
        {
            "x": t["number"],
            "y": t.get("value"),
            "ok": (t.get("value") is not None and t["value"] < doc["objective"]["penalty"]),
        }
        for t in doc["trials"]
    ]
    chart = (
        '<div id="chart" style="height:320px"></div>'
        f"<script>const DATA={json.dumps(chart_data)};"
        "const ok=DATA.filter(d=>d.ok), bad=DATA.filter(d=>!d.ok);"
        'Plotly.newPlot("chart",['
        '{x:ok.map(d=>d.x),y:ok.map(d=>d.y),mode:"markers",name:"ok",marker:{color:"#4caf50"}},'
        '{x:bad.map(d=>d.x),y:bad.map(d=>d.y),mode:"markers",name:"penalty",marker:{color:"#e10600"}}'
        '],{paper_bgcolor:"#111418",plot_bgcolor:"#111418",font:{color:"#e8e8e8"},'
        'xaxis:{title:"trial"},yaxis:{title:"value"},margin:{t:20}});</script>'
    )

    body = (
        f"<h1>{sid}</h1>"
        '<div class="tabs">'
        "<div class=\"tab active\" id=\"tab-ov\" onclick=\"showTab('ov')\">概要</div>"
        "<div class=\"tab\" id=\"tab-sc\" onclick=\"showTab('sc')\">スコア推移</div>"
        "<div class=\"tab\" id=\"tab-pa\" onclick=\"showTab('pa')\">パラメータ</div>"
        "</div>"
        f'<div class="panel active" id="panel-ov"><div class="cards">{kpis}</div></div>'
        f'<div class="panel" id="panel-sc">{chart}</div>'
        f'<div class="panel" id="panel-pa">{ptable}</div>'
    )
    head_extra = '<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>'
    return page(sid, body, head_extra=head_extra)
