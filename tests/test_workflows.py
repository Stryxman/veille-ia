from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def workflow():
    return yaml.safe_load((ROOT / ".github/workflows/publish.yml").read_text(encoding="utf-8"))


def test_publication_runs_daily_and_on_demand():
    triggers = workflow()[True]  # YAML 1.1 reads the "on" key as True
    # three slots: GitHub does not guarantee scheduled runs, one run a day is enough
    assert triggers["schedule"] == [
        {"cron": "17 4 * * *"},
        {"cron": "17 10 * * *"},
        {"cron": "17 16 * * *"},
    ]
    assert "workflow_dispatch" in triggers


def test_publication_builds_then_deploys_to_pages():
    jobs = workflow()["jobs"]
    build_steps = jobs["build"]["steps"]
    assert any(step.get("run") == "python -m veille.render --output site" for step in build_steps)
    uses = [step.get("uses", "") for step in build_steps]
    assert any(action.startswith("actions/upload-pages-artifact") for action in uses)
    assert jobs["deploy"]["needs"] == "build"
    deploy_uses = [step.get("uses", "") for step in jobs["deploy"]["steps"]]
    assert any(action.startswith("actions/deploy-pages") for action in deploy_uses)


def test_publication_has_only_the_permissions_it_needs():
    # only the deploy job may publish to Pages; the build job reads external feeds
    assert workflow()["permissions"] == {"contents": "read"}
    assert workflow()["jobs"]["deploy"]["permissions"] == {"pages": "write", "id-token": "write"}


def test_publication_steps_cannot_hang():
    jobs = workflow()["jobs"]
    assert all(job.get("timeout-minutes") for job in jobs.values())


def ci_steps():
    data = yaml.safe_load((ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8"))
    return [step.get("run", "") for step in data["jobs"]["test"]["steps"]]


def test_ci_fails_when_test_coverage_drops_below_85_percent():
    assert any("coverage report --fail-under=85" in run for run in ci_steps())


def test_naming_and_complexity_rules_are_checked():
    import tomllib

    lint = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["tool"]["ruff"]
    assert {"N", "C90"} <= set(lint["lint"]["select"])
    assert lint["lint"]["mccabe"]["max-complexity"] == 10
