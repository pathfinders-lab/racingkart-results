from build_study import build_study_html, objective_formula


def _doc():
    return {
        "study_id": "keigo-mpc-q6",
        "study_name": "mpc-q6",
        "author": "keigo",
        "objective": {"terms": [{"metric": "time", "weight": 1.0}], "penalty": 150.0},
        "metric_defs": {"time": {"unit": "s", "description": "..."}},
        "develop_value": 130.8,
        "required_laps": 2,
        "n_trials": 2, "n_complete": 2, "n_valid": 1, "valid_rate": 0.5,
        "best_trial": {"number": 1, "value": 129.0, "delta_develop": -1.8,
                       "metrics": {"time": 129.0, "e_y_rms": 0.12},
                       "params": {"Q0": 2.8e6, "Q1": 9.1e7}},
        "param_importance": {"Q0": 0.6, "Q1": 0.4},
        "trials": [
            {"number": 0, "value": 150.0, "metrics": None, "exit_reason": "crash", "params": {"Q0": 9.8e6}},
            {"number": 1, "value": 129.0, "metrics": {"time": 129.0, "e_y_rms": 0.12},
             "exit_reason": "ok", "params": {"Q0": 2.8e6}},
        ],
    }


def test_objective_formula_from_terms():
    assert objective_formula({"terms": [{"metric": "time", "weight": 1.0}]}) == "time"
    assert objective_formula(
        {"terms": [{"metric": "time", "weight": 1.0}, {"metric": "e_y_rms", "weight": 0.005}]}
    ) == "time + 0.005·e_y_rms"


def test_build_study_html_contains_key_facts():
    html = build_study_html(_doc())
    assert "<!DOCTYPE html>" in html
    assert "keigo-mpc-q6" in html
    assert "129.0" in html          # best value
    assert "-1.8" in html           # delta_develop
    assert "Q0" in html             # params column (dynamic key)
    assert "DATA" in html           # inline data for the chart
