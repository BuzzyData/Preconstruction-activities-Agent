from preconstruction_agent import PreConstructionAgent


def test_generate_plan_for_residential_project():
    project = {
        "project_name": "Oak Terrace Residences",
        "project_type": "residential",
        "location": "Austin, TX",
        "site_area_sqft": 48000,
        "budget_usd": 12000000,
        "timeline_days": 240,
        "has_historic_constraints": False,
        "has_utility_conflicts": True,
    }

    agent = PreConstructionAgent(project)
    plan = agent.generate_plan()

    assert plan["project_name"] == "Oak Terrace Residences"
    assert "site_survey" in plan["checklist"]
    assert "permit_review" in plan["checklist"]
    assert plan["timeline_days"] == 240
    assert plan["risk_level"] in {"Low", "Medium", "High"}


def test_high_risk_project_includes_detailed_risk_controls():
    project = {
        "project_name": "Central Transit Hub",
        "project_type": "infrastructure",
        "location": "Denver, CO",
        "site_area_sqft": 120000,
        "budget_usd": 45000000,
        "timeline_days": 420,
        "has_historic_constraints": True,
        "has_utility_conflicts": True,
        "environmental_issues": ["wetlands", "stormwater runoff"],
    }

    agent = PreConstructionAgent(project)
    risk = agent.assess_risk(project)

    assert risk["level"] == "High"
    assert "environmental review" in risk["controls"]
    assert "utility conflict resolution" in risk["controls"]


def test_summary_report_is_actionable():
    project = {
        "project_name": "Harbor Office Expansion",
        "project_type": "commercial",
        "location": "Seattle, WA",
        "site_area_sqft": 35000,
        "budget_usd": 9000000,
        "timeline_days": 180,
    }

    agent = PreConstructionAgent(project)
    report = agent.summary_report()

    assert report["goals"][0].startswith("Confirm")
    assert "budget" in report["kpis"]
    assert report["summary"].startswith("Pre-construction activities")


def test_google_doc_export_is_ready_for_docs():
    project = {
        "project_name": "Harbor Office Expansion",
        "project_type": "commercial",
        "location": "Seattle, WA",
        "site_area_sqft": 35000,
        "budget_usd": 9000000,
        "timeline_days": 180,
    }

    agent = PreConstructionAgent(project)
    doc = agent.to_google_doc()

    assert "<html" in doc.lower()
    assert "Harbor Office Expansion" in doc
    assert "Risk Level" in doc
    assert "Checklist" in doc
