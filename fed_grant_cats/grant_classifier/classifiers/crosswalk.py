"""
Generalizable Crosswalk Analysis Module

The crosswalk concept: Many research domains follow a pattern of
  INPUT → MECHANISM → OUTPUT

where funding often clusters at the ends but not in the middle.

Examples:
  - Environmental health: Exposure → Biological mechanism → Therapeutic intervention
  - Drug development: Disease target → Pathway → Treatment
  - Climate: Emission source → Climate process → Mitigation technology
  - Social science: Risk factor → Social mechanism → Policy intervention

This module:
1. Defines crosswalk stages for any domain
2. Classifies grants into stages
3. Identifies gaps (underfunded connections)
4. Generates Sankey-ready flow data
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set, Tuple
from collections import defaultdict
import json


@dataclass
class CrosswalkStage:
    """A stage in the crosswalk pipeline."""
    name: str
    description: str
    keywords: List[str] = field(default_factory=list)
    weight: float = 1.0

    # Optional: further subdivisions within this stage
    subtypes: List[str] = field(default_factory=list)


@dataclass
class CrosswalkLink:
    """A connection between stages (e.g., PFAS → oxidative stress)."""
    source_stage: str
    target_stage: str
    source_entity: str  # e.g., "PFAS"
    target_entity: str  # e.g., "oxidative stress"
    grant_count: int = 0
    total_funding: float = 0.0
    grant_ids: List[str] = field(default_factory=list)


@dataclass
class CrosswalkConfig:
    """Configuration for a crosswalk analysis."""
    name: str
    description: str
    stages: List[CrosswalkStage]

    # Define what entities exist at each stage
    # e.g., {"input": ["PFAS", "lead", "PM2.5"], "mechanism": ["oxidative stress", "inflammation"]}
    entities: Dict[str, List[str]] = field(default_factory=dict)

    # Define known connections between entities
    # e.g., [("PFAS", "liver toxicity"), ("lead", "neurotoxicity")]
    known_links: List[Tuple[str, str]] = field(default_factory=list)


class CrosswalkAnalyzer:
    """
    Analyze grants through a crosswalk lens.

    The fundamental insight: Research funding often follows patterns like
    "cause → mechanism → solution" but critical connections are underfunded.
    This analyzer identifies those gaps.
    """

    def __init__(self, config: CrosswalkConfig):
        self.config = config
        self.stage_names = [s.name for s in config.stages]

        # Build keyword lookup
        self.stage_keywords: Dict[str, Set[str]] = {}
        for stage in config.stages:
            self.stage_keywords[stage.name] = set(kw.lower() for kw in stage.keywords)

        # Build entity to stage lookup
        self.entity_to_stage: Dict[str, str] = {}
        for stage_name, entities in config.entities.items():
            for entity in entities:
                self.entity_to_stage[entity.lower()] = stage_name

        # Track findings
        self.links: Dict[Tuple[str, str, str, str], CrosswalkLink] = {}
        self.stage_counts: Dict[str, int] = defaultdict(int)
        self.stage_funding: Dict[str, float] = defaultdict(float)

    def classify_grant_stage(self, grant_id: str, title: str, abstract: str) -> Dict[str, Any]:
        """
        Classify which crosswalk stage(s) a grant belongs to.

        Returns dict with:
          - primary_stage: Main stage assignment
          - stages: All stages with scores
          - entities_found: Specific entities detected
          - spans_stages: Whether grant bridges multiple stages (valuable!)
        """
        text = f"{title} {abstract}".lower()

        # Score each stage
        stage_scores: Dict[str, float] = {}
        entities_found: Dict[str, List[str]] = defaultdict(list)

        for stage in self.config.stages:
            score = 0.0
            for kw in stage.keywords:
                if kw.lower() in text:
                    score += stage.weight

            # Also check entities
            for entity in self.config.entities.get(stage.name, []):
                if entity.lower() in text:
                    score += 2.0  # Entities are more specific
                    entities_found[stage.name].append(entity)

            stage_scores[stage.name] = score

        # Determine primary stage
        if not any(stage_scores.values()):
            primary_stage = None
        else:
            primary_stage = max(stage_scores.items(), key=lambda x: x[1])[0]

        # Check if grant bridges stages (especially valuable)
        active_stages = [s for s, score in stage_scores.items() if score > 0]
        spans_stages = len(active_stages) > 1

        return {
            'primary_stage': primary_stage,
            'stages': stage_scores,
            'entities_found': dict(entities_found),
            'spans_stages': spans_stages,
            'active_stages': active_stages,
        }

    def add_grant(self, grant_id: str, title: str, abstract: str, amount: float = 0.0):
        """
        Add a grant to the crosswalk analysis.

        Tracks:
        - Which stage it belongs to
        - Which entities it mentions
        - Links it creates between stages/entities
        """
        result = self.classify_grant_stage(grant_id, title, abstract)

        # Update stage counts
        if result['primary_stage']:
            self.stage_counts[result['primary_stage']] += 1
            self.stage_funding[result['primary_stage']] += amount

        # Track entity-to-entity links for grants that span stages
        if result['spans_stages']:
            # Find all entity pairs across different stages
            for stage1, entities1 in result['entities_found'].items():
                for stage2, entities2 in result['entities_found'].items():
                    if stage1 != stage2:
                        for e1 in entities1:
                            for e2 in entities2:
                                key = (stage1, stage2, e1, e2)
                                if key not in self.links:
                                    self.links[key] = CrosswalkLink(
                                        source_stage=stage1,
                                        target_stage=stage2,
                                        source_entity=e1,
                                        target_entity=e2,
                                    )
                                self.links[key].grant_count += 1
                                self.links[key].total_funding += amount
                                self.links[key].grant_ids.append(grant_id)

    def identify_gaps(self) -> List[Dict[str, Any]]:
        """
        Identify underfunded connections in the crosswalk.

        Returns list of gaps, each with:
          - source_stage, target_stage
          - source_entity, target_entity (if applicable)
          - gap_type: "missing", "underfunded", "unconnected"
          - severity: 1-10 score
          - rationale: Why this is a gap
        """
        gaps = []

        # 1. Find stage-to-stage gaps
        for i, stage1 in enumerate(self.stage_names[:-1]):
            stage2 = self.stage_names[i + 1]

            # Count grants bridging these stages
            bridging_grants = sum(
                link.grant_count
                for link in self.links.values()
                if link.source_stage == stage1 and link.target_stage == stage2
            )

            # Compare to individual stage counts
            stage1_count = self.stage_counts.get(stage1, 0)
            stage2_count = self.stage_counts.get(stage2, 0)

            if stage1_count > 0 and stage2_count > 0 and bridging_grants == 0:
                gaps.append({
                    'source_stage': stage1,
                    'target_stage': stage2,
                    'gap_type': 'missing',
                    'severity': 10,
                    'rationale': f"No grants bridge {stage1} ({stage1_count} grants) to {stage2} ({stage2_count} grants)",
                    'bridging_grants': 0,
                })
            elif bridging_grants < min(stage1_count, stage2_count) * 0.1:
                gaps.append({
                    'source_stage': stage1,
                    'target_stage': stage2,
                    'gap_type': 'underfunded',
                    'severity': 7,
                    'rationale': f"Only {bridging_grants} grants bridge {stage1} to {stage2}",
                    'bridging_grants': bridging_grants,
                })

        # 2. Find known links with zero funding
        for source_entity, target_entity in self.config.known_links:
            # Check if this link exists in our data
            found = False
            for link in self.links.values():
                if (link.source_entity.lower() == source_entity.lower() and
                    link.target_entity.lower() == target_entity.lower()):
                    found = True
                    break

            if not found:
                source_stage = self.entity_to_stage.get(source_entity.lower(), 'unknown')
                target_stage = self.entity_to_stage.get(target_entity.lower(), 'unknown')
                gaps.append({
                    'source_stage': source_stage,
                    'target_stage': target_stage,
                    'source_entity': source_entity,
                    'target_entity': target_entity,
                    'gap_type': 'unconnected',
                    'severity': 8,
                    'rationale': f"Known connection {source_entity} → {target_entity} has no funding",
                })

        return sorted(gaps, key=lambda x: -x['severity'])

    def generate_sankey_data(self) -> Dict[str, Any]:
        """
        Generate data for Sankey diagram visualization.

        Returns:
          - nodes: List of nodes with stage and entity info
          - links: List of connections with values
        """
        nodes = []
        node_index = {}

        # Add stage nodes
        for i, stage in enumerate(self.config.stages):
            node_index[f"stage_{stage.name}"] = len(nodes)
            nodes.append({
                'id': f"stage_{stage.name}",
                'name': stage.name,
                'type': 'stage',
                'count': self.stage_counts.get(stage.name, 0),
                'funding': self.stage_funding.get(stage.name, 0),
            })

        # Add entity nodes
        for stage_name, entities in self.config.entities.items():
            for entity in entities:
                key = f"entity_{entity}"
                if key not in node_index:
                    node_index[key] = len(nodes)
                    nodes.append({
                        'id': key,
                        'name': entity,
                        'type': 'entity',
                        'stage': stage_name,
                    })

        # Generate links
        links = []
        for link in self.links.values():
            source_key = f"entity_{link.source_entity}"
            target_key = f"entity_{link.target_entity}"

            if source_key in node_index and target_key in node_index:
                links.append({
                    'source': node_index[source_key],
                    'target': node_index[target_key],
                    'value': link.grant_count,
                    'funding': link.total_funding,
                })

        return {
            'nodes': nodes,
            'links': links,
        }

    def summary(self) -> Dict[str, Any]:
        """Generate summary statistics."""
        return {
            'stages': {
                name: {
                    'count': self.stage_counts.get(name, 0),
                    'funding': self.stage_funding.get(name, 0),
                }
                for name in self.stage_names
            },
            'total_links': len(self.links),
            'total_grants_analyzed': sum(self.stage_counts.values()),
            'gaps': self.identify_gaps(),
        }


# =============================================================================
# PRESET CROSSWALK CONFIGURATIONS
# =============================================================================

def get_environmental_health_crosswalk() -> CrosswalkConfig:
    """
    Environmental health crosswalk: Exposure → Mechanism → Intervention

    This is the original "gap analysis" pattern from the NIH work.
    """
    return CrosswalkConfig(
        name="Environmental Health",
        description="Exposure → Biological Mechanism → Therapeutic Intervention",
        stages=[
            CrosswalkStage(
                name="exposure",
                description="Research documenting chemical exposures and their presence",
                keywords=["exposure", "contamination", "biomonitoring", "pollutant", "toxicant",
                         "environmental monitoring", "detection", "measurement"],
            ),
            CrosswalkStage(
                name="mechanism",
                description="Research on how exposures cause biological harm",
                keywords=["mechanism", "pathway", "toxicity", "oxidative stress", "inflammation",
                         "epigenetic", "disruption", "damage", "dysfunction"],
            ),
            CrosswalkStage(
                name="intervention",
                description="Research on protective or therapeutic interventions",
                keywords=["protection", "prevention", "intervention", "treatment", "therapy",
                         "antioxidant", "supplement", "chelation", "reversal"],
            ),
        ],
        entities={
            "exposure": ["PFAS", "phthalates", "BPA", "lead", "mercury", "arsenic", "cadmium",
                        "PM2.5", "pesticides", "microplastics"],
            "mechanism": ["oxidative stress", "inflammation", "endocrine disruption",
                         "neurotoxicity", "hepatotoxicity", "reproductive toxicity",
                         "epigenetic modification", "DNA damage"],
            "intervention": ["NAC", "alpha-lipoic acid", "sulforaphane", "silymarin",
                            "chelation therapy", "antioxidant", "Nrf2 activation"],
        },
        known_links=[
            # Known exposure-mechanism links
            ("PFAS", "hepatotoxicity"),
            ("PFAS", "endocrine disruption"),
            ("phthalates", "reproductive toxicity"),
            ("lead", "neurotoxicity"),
            ("PM2.5", "oxidative stress"),
            ("PM2.5", "inflammation"),
            # Known mechanism-intervention links (often underfunded)
            ("oxidative stress", "NAC"),
            ("oxidative stress", "alpha-lipoic acid"),
            ("inflammation", "sulforaphane"),
        ],
    )


def get_drug_development_crosswalk() -> CrosswalkConfig:
    """
    Drug development crosswalk: Target → Pathway → Treatment
    """
    return CrosswalkConfig(
        name="Drug Development",
        description="Disease Target → Biological Pathway → Treatment Modality",
        stages=[
            CrosswalkStage(
                name="target",
                description="Research identifying disease targets",
                keywords=["target identification", "disease mechanism", "biomarker",
                         "genetic variant", "driver mutation"],
            ),
            CrosswalkStage(
                name="pathway",
                description="Research on targetable pathways",
                keywords=["signaling pathway", "druggable", "modulator", "inhibitor",
                         "activator", "receptor", "enzyme"],
            ),
            CrosswalkStage(
                name="treatment",
                description="Research developing treatments",
                keywords=["therapeutic", "drug candidate", "clinical trial", "efficacy",
                         "formulation", "delivery"],
            ),
        ],
        entities={
            "target": ["KRAS", "p53", "EGFR", "HER2", "PD-1", "BRCA"],
            "pathway": ["MAPK", "PI3K", "Wnt", "Notch", "JAK-STAT", "NF-kB"],
            "treatment": ["small molecule", "antibody", "CAR-T", "gene therapy", "vaccine"],
        },
        known_links=[],
    )


# Registry of preset crosswalks
CROSSWALK_PRESETS = {
    'environmental_health': get_environmental_health_crosswalk,
    'drug_development': get_drug_development_crosswalk,
}


def get_crosswalk(name: str) -> CrosswalkConfig:
    """Get a preset crosswalk configuration by name."""
    if name not in CROSSWALK_PRESETS:
        raise ValueError(f"Unknown crosswalk: {name}. Available: {list(CROSSWALK_PRESETS.keys())}")
    return CROSSWALK_PRESETS[name]()
