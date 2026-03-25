#!/usr/bin/env python3
"""
Classification prompt template for NSF grants.
To be used with Claude API or subagent calls.
"""

CLASSIFICATION_PROMPT = """Classify each NSF grant into ONE of three categories:

**ENVIRONMENTAL** = Studies exposure/risk factors, environmental monitoring, pollution effects, climate impacts on ecosystems/health, contamination studies, toxicology, water/air quality
**MECHANISTIC** = Basic biology studying pathways, molecular/cellular mechanisms, how biological systems work, disease mechanisms, protein/gene function
**EVERYTHING_ELSE** = Methods/tools/sensors, infrastructure, education/training, technology development, social science, CS/math/physics/astronomy, engineering devices

Return ONLY a JSON object mapping grant ID to category code (ENV, MECH, OTHER).

GRANTS:
{grants_text}

Return JSON format: {{"id1": "ENV", "id2": "OTHER", "id3": "MECH", ...}}"""

def format_batch_for_classification(batch):
    """Format a batch of grants for the classification prompt."""
    lines = []
    for i, g in enumerate(batch, 1):
        title = g.get('title', '')[:100]
        abstract = g.get('abstract', '')[:200]
        directorate = g.get('directorate', '')
        program = g.get('program', '')[:50]
        lines.append(f"{i}. ID:{g['id']} - \"{title}\" - {directorate}/{program} - {abstract}")
    return "\n".join(lines)

if __name__ == "__main__":
    import json
    import sys

    batch_file = sys.argv[1]
    with open(batch_file) as f:
        batch = json.load(f)

    grants_text = format_batch_for_classification(batch)
    prompt = CLASSIFICATION_PROMPT.format(grants_text=grants_text)
    print(prompt)
