#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python -m unittest discover -s "$ROOT/tests" -v
python "$ROOT/scripts/rq_coverage.py" --questions "$ROOT/templates/research_questions.csv" --mapping "$ROOT/templates/rq_evidence_map.csv"
echo "G1/G2: 预置模板处于pending；未完成人工审核时不应通过。"
