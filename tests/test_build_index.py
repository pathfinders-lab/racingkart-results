from build_index import build_index_html


def _summaries():
    return [
        {"study_id": "keigo-mpc-q6", "author": "keigo", "study_name": "mpc-q6",
         "best_value": 129.0, "delta_develop": -1.8, "n_trials": 2,
         "generated_at": "2026-06-22T09:00:00Z", "develop_value": 130.8},
        {"study_id": "keigo-mpc-q5", "author": "keigo", "study_name": "mpc-q5",
         "best_value": 130.1, "delta_develop": -0.7, "n_trials": 2,
         "generated_at": "2026-06-20T09:00:00Z", "develop_value": 130.8},
    ]


def test_build_index_lists_studies_with_links():
    html = build_index_html(_summaries())
    assert "<!DOCTYPE html>" in html
    assert "keigo-mpc-q6" in html
    assert 'href="studies/keigo-mpc-q6.html"' in html
    # overall best = lowest best_value
    assert "129.0" in html


def test_build_index_empty():
    html = build_index_html([])
    assert "<!DOCTYPE html>" in html
