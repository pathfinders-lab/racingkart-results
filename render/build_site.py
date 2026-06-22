"""Entry point: read studies/*.json, write index.html + studies/*.html into out/."""

import json
from pathlib import Path

from build_index import build_index_html
from build_study import build_study_html


def _summary(doc: dict) -> dict:
    best = doc.get("best_trial")
    return {
        "study_id": doc["study_id"],
        "author": doc.get("author", ""),
        "study_name": doc.get("study_name", ""),
        "best_value": best["value"] if best else None,
        "delta_develop": best.get("delta_develop") if best else None,
        "n_trials": doc.get("n_trials"),
        "generated_at": doc.get("generated_at", ""),
        "develop_value": doc.get("develop_value"),
    }


def build_site(repo_root: Path, out_dir: Path) -> None:
    studies_dir = repo_root / "studies"
    out_studies = out_dir / "studies"
    out_studies.mkdir(parents=True, exist_ok=True)

    summaries = []
    for jf in sorted(studies_dir.glob("*.json")):
        doc = json.loads(jf.read_text(encoding="utf-8"))
        summaries.append(_summary(doc))
        (out_studies / f"{doc['study_id']}.html").write_text(
            build_study_html(doc), encoding="utf-8"
        )
    (out_dir / "index.html").write_text(build_index_html(summaries), encoding="utf-8")


def main() -> None:
    build_site(repo_root=Path(__file__).resolve().parent.parent, out_dir=Path("out"))
    print("wrote out/index.html and out/studies/*.html")


if __name__ == "__main__":
    main()
