"""Render the index page: Overall Best KPI + study table (C-layout)."""

from template import page


def _fmt(x, nd=3):
    return "—" if x is None else (f"{x:.{nd}f}" if isinstance(x, float) else str(x))


def build_index_html(summaries: list[dict]) -> str:
    valid = [s for s in summaries if s.get("best_value") is not None]
    overall = min(valid, key=lambda s: s["best_value"]) if valid else None

    kpi = (
        f'<div class="card"><div class="label">Overall Best</div>'
        f'<div class="big good">{_fmt(overall["best_value"]) if overall else "—"}</div>'
        f'<div class="label">{overall["study_id"] if overall else ""}</div></div>'
        f'<div class="card"><div class="label">Active Studies</div>'
        f'<div class="big">{len(summaries)}</div><div class="label"></div></div>'
    )

    rows = ""
    for s in sorted(summaries, key=lambda s: s.get("generated_at", ""), reverse=True):
        sid = s["study_id"]
        delta = _fmt(s.get("delta_develop"))
        rows += (
            f'<tr><td><a href="studies/{sid}.html">{sid}</a></td>'
            f'<td>{s.get("author","")}</td><td>{_fmt(s.get("best_value"))}</td>'
            f'<td>{delta}</td><td>{s.get("n_trials","")}</td>'
            f'<td>{s.get("generated_at","")[:10]}</td></tr>'
        )
    table = (
        "<table><tr><th>study</th><th>author</th><th>best</th><th>Δdev</th>"
        f"<th>trials</th><th>date</th></tr>{rows}</table>"
    )

    body = f"<h1>Optimization Studies</h1><div class='cards'>{kpi}</div><h2>Studies</h2>{table}"
    return page("racingkart-results", body)
