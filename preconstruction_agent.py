from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


class PreConstructionAgent:
    """Automates core pre-construction planning activities for a project."""

    def __init__(self, project: Dict[str, Any]):
        self.project = project or {}
        self.project_name = self.project.get("project_name", "Untitled Project")

    def assess_risk(self, project: Dict[str, Any] | None = None) -> Dict[str, Any]:
        data = project or self.project
        level = "Low"
        controls: List[str] = [
            "site documentation review",
            "baseline cost tracking",
        ]

        if data.get("has_historic_constraints") or data.get("has_utility_conflicts"):
            level = "Medium"
            controls = [
                "utility conflict resolution",
                "permit and code validation",
                "stakeholder coordination",
            ]

        environmental_issues = data.get("environmental_issues") or []
        if (
            data.get("has_historic_constraints")
            and data.get("has_utility_conflicts")
        ) or environmental_issues:
            level = "High"
            controls = [
                "environmental review",
                "utility conflict resolution",
                "stakeholder coordination",
                "risk register updates",
            ]

        return {"level": level, "controls": controls}

    def generate_plan(self) -> Dict[str, Any]:
        project = self.project
        risk = self.assess_risk(project)
        checklist = [
            "site_survey",
            "geotechnical_study",
            "environmental_screening",
            "permit_review",
            "utility_mapping",
            "cost_estimation",
            "schedule_baseline",
            "subcontractor_prequalification",
        ]

        if project.get("has_utility_conflicts"):
            checklist.append("utility_conflict_resolution")

        if project.get("has_historic_constraints"):
            checklist.append("historic_review")

        return {
            "project_name": project.get("project_name", self.project_name),
            "project_type": project.get("project_type", "general"),
            "location": project.get("location", "Unassigned"),
            "checklist": checklist,
            "timeline_days": project.get("timeline_days", 0),
            "risk_level": risk["level"],
            "risk_controls": risk["controls"],
        }

    def summary_report(self) -> Dict[str, Any]:
        project = self.project
        goals = [
            "Confirm site conditions and feasibility",
            "Verify budget, permitting, and schedule alignment",
            "Resolve critical risks before mobilization",
        ]

        kpis = {
            "budget": project.get("budget_usd", 0),
            "timeline_days": project.get("timeline_days", 0),
            "site_area_sqft": project.get("site_area_sqft", 0),
        }

        summary = (
            f"Pre-construction activities for {self.project_name} should focus on site "
            "readiness, budget validation, and risk mitigation before construction begins."
        )

        return {
            "goals": goals,
            "kpis": kpis,
            "summary": summary,
        }

    def to_google_doc(self) -> str:
        plan = self.generate_plan()
        risk = self.assess_risk(self.project)
        report = self.summary_report()

        checklist_html = "".join(
            f"<li>{item.replace('_', ' ').title()}</li>" for item in plan["checklist"]
        )
        risk_controls_html = "".join(
            f"<li>{item}</li>" for item in risk["controls"]
        )
        goals_html = "".join(f"<li>{goal}</li>" for goal in report["goals"])

        return f"""
<html>
  <head>
    <meta charset="utf-8" />
    <title>{self.project_name} - Pre-Construction Activities</title>
  </head>
  <body>
    <h1>{self.project_name}</h1>
    <p><strong>Project Type:</strong> {plan['project_type']}</p>
    <p><strong>Location:</strong> {plan['location']}</p>
    <p><strong>Timeline:</strong> {plan['timeline_days']} days</p>

    <h2>Risk Level</h2>
    <p>{risk['level']}</p>

    <h2>Risk Controls</h2>
    <ul>{risk_controls_html}</ul>

    <h2>Checklist</h2>
    <ul>{checklist_html}</ul>

    <h2>Goals</h2>
    <ul>{goals_html}</ul>

    <h2>Key KPI Summary</h2>
    <ul>
      <li>Budget: ${report['kpis']['budget']:,}</li>
      <li>Timeline: {report['kpis']['timeline_days']} days</li>
      <li>Site Area: {report['kpis']['site_area_sqft']} sq ft</li>
    </ul>

    <p>{report['summary']}</p>
  </body>
</html>
""".strip()


def load_project_from_file(file_path: str | Path) -> Dict[str, Any]:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    parser = argparse.ArgumentParser(description="Automate pre-construction activities for a project.")
    parser.add_argument(
        "--input",
        default="project_input.json",
        help="Path to a JSON file containing project data.",
    )
    parser.add_argument(
        "--format",
        choices=["json", "gdoc"],
        default="json",
        help="Output format: 'json' for JSON or 'gdoc' for Google Docs-friendly HTML.",
    )
    args = parser.parse_args()

    project = load_project_from_file(args.input)
    agent = PreConstructionAgent(project)

    if args.format == "gdoc":
        print(agent.to_google_doc())
    else:
        print(json.dumps({
            "plan": agent.generate_plan(),
            "risk": agent.assess_risk(project),
            "report": agent.summary_report(),
        }, indent=2))


if __name__ == "__main__":
    main()
