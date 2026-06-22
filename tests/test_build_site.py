import json

from build_site import build_site


def test_build_site_writes_index_and_study_pages(tmp_path):
    studies = tmp_path / "studies"
    studies.mkdir()
    doc = {
        "study_id": "keigo-q6", "author": "keigo", "study_name": "q6",
        "objective": {"terms": [{"metric": "time", "weight": 1.0}], "penalty": 150.0},
        "metric_defs": {}, "develop_value": 130.8, "required_laps": 2,
        "n_trials": 1, "n_complete": 1, "n_valid": 1, "valid_rate": 1.0,
        "best_trial": {"number": 0, "value": 129.0, "delta_develop": -1.8, "metrics": {"time": 129.0}, "params": {"Q0": 1.0}},
        "param_importance": {}, "generated_at": "2026-06-22T00:00:00Z",
        "trials": [{"number": 0, "value": 129.0, "metrics": {"time": 129.0}, "exit_reason": "ok", "params": {"Q0": 1.0}}],
    }
    (studies / "keigo-q6.json").write_text(json.dumps(doc))

    out = tmp_path / "out"
    build_site(repo_root=tmp_path, out_dir=out)

    assert (out / "index.html").is_file()
    assert (out / "studies" / "keigo-q6.html").is_file()
    assert "keigo-q6" in (out / "index.html").read_text()
