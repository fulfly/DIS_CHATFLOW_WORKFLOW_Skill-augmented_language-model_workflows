# Workflows

This directory contains public-safe workflow materials for the DIS disintegration-analysis Chatflow and the TOMO/MYGO formulation-optimization Chatflow.

## Main Files

- `DIS_chatflow.dsl`: Dify workflow export for disintegration visualization analysis.
- `TOMO_chatflow.dsl`: Dify workflow export for TOMO/MYGO sustained-release formulation optimization.
- `node_descriptions.md`: human-readable description of workflow nodes and branch logic.
- `screenshots/DIS_chatflow_workflow.png`: DIS Chatflow screenshot.
- `screenshots/TOMO_chatflow_workflow.png`: TOMO/MYGO Chatflow screenshot.
- `screenshots/TOMO_chatflow_workflow_2.png`: duplicate/alternate TOMO screenshot retained from the reviewed staging set.

## Public-Release Notes

The DSL files should not contain private API keys. Any live deployment should configure model providers, Dify credentials, and endpoint secrets outside the repository.
