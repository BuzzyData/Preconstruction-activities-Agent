# Preconstruction-activities-Agent

A lightweight Python agent for automating pre-construction planning activities.

## Features

- Generates a pre-construction checklist for project teams
- Assesses project risk using site, utility, and environmental signals
- Produces a concise summary report for stakeholders
- Can be run as a CLI for quick project planning

## Usage

Run with a JSON project file:

```bash
python preconstruction_agent.py --input project_input.json
```

Generate Google Docs-friendly HTML output:

```bash
python preconstruction_agent.py --input project_input.json --format gdoc
```

You can also run it without an argument to use the default sample file:

```bash
python preconstruction_agent.py
```

## JSON input example

The project input file should look like this:

```json
{
  "project_name": "Oak Terrace Residences",
  "project_type": "residential",
  "location": "Austin, TX",
  "site_area_sqft": 48000,
  "budget_usd": 12000000,
  "timeline_days": 240,
  "has_historic_constraints": false,
  "has_utility_conflicts": true,
  "environmental_issues": ["stormwater runoff"]
}
```

## Google Docs export format

The `--format gdoc` option creates HTML that is easy to paste into a Google Doc.

```bash
python preconstruction_agent.py --input project_input.json --format gdoc
```

Example output snippet:

```html
<html>
  <head>
    <meta charset="utf-8" />
    <title>Oak Terrace Residences - Pre-Construction Activities</title>
  </head>
  <body>
    <h1>Oak Terrace Residences</h1>
    <p><strong>Project Type:</strong> residential</p>
    <p><strong>Location:</strong> Austin, TX</p>
    <h2>Risk Level</h2>
    <p>High</p>
    <h2>Checklist</h2>
    <ul>
      <li>Site Survey</li>
      <li>Permit Review</li>
    </ul>
  </body>
</html>
```

Copy the generated HTML into a Google Doc and paste it in without formatting if needed.

## Example in Python

```python
from preconstruction_agent import PreConstructionAgent

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
print(plan)
```
