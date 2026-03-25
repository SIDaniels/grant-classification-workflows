#!/usr/bin/env python3
"""
Grant Classifier CLI

Usage:
    python -m grant_classifier.cli fetch --source nsf --config config.yaml --output grants.json
    python -m grant_classifier.cli classify --input grants.json --config config.yaml --output results.json
    python -m grant_classifier.cli crosswalk --input grants.json --preset environmental_health --output gaps.json
    python -m grant_classifier.cli pipeline --config workflow.yaml
"""

import argparse
import json
import yaml
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional


def load_config(path: str) -> Dict[str, Any]:
    """Load YAML or JSON config file."""
    with open(path) as f:
        if path.endswith('.yaml') or path.endswith('.yml'):
            return yaml.safe_load(f)
        return json.load(f)


def save_json(data: Any, path: str):
    """Save data to JSON file."""
    with open(path, 'w') as f:
        json.dump(data, f, indent=2, default=str)
    print(f"Saved to {path}")


def cmd_fetch(args):
    """Fetch grants from a data source."""
    from .sources import get_source

    config = load_config(args.config) if args.config else {}

    print(f"Fetching from {args.source}...")
    source = get_source(args.source, config)

    grants = []
    for i, grant in enumerate(source.fetch()):
        grants.append({
            'id': grant.id,
            'title': grant.title,
            'abstract': grant.abstract,
            'amount': grant.amount,
            'start_date': str(grant.start_date) if grant.start_date else None,
            'end_date': str(grant.end_date) if grant.end_date else None,
            'institution': grant.institution,
            'state': grant.state,
            'pi_name': grant.pi_name,
            'program': grant.program,
            'source_type': grant.source_type,
            'metadata': grant.metadata,
        })

        if (i + 1) % 100 == 0:
            print(f"  Fetched {i + 1} grants...")

    print(f"Total: {len(grants)} grants")

    if args.output:
        save_json(grants, args.output)

    return grants


def cmd_classify(args):
    """Classify grants using specified classifier."""
    from .classifiers import get_classifier

    # Load grants
    with open(args.input) as f:
        grants = json.load(f)

    print(f"Loaded {len(grants)} grants")

    # Load config
    config = load_config(args.config) if args.config else {}

    # Get classifier type
    classifier_type = args.classifier or config.get('classifier', 'keyword')

    print(f"Using {classifier_type} classifier...")
    classifier = get_classifier(classifier_type, config)

    # Classify
    if hasattr(classifier, 'classify_batch'):
        results = classifier.classify_batch(
            grants,
            id_field='id',
            title_field='title',
            abstract_field='abstract'
        )
    else:
        results = []
        for grant in grants:
            result = classifier.classify(
                grant_id=grant['id'],
                title=grant['title'],
                abstract=grant['abstract']
            )
            results.append(result)

    # Convert to dicts for JSON output
    output_results = []
    for r in results:
        result_dict = {
            'grant_id': r.grant_id,
            'primary_category': r.primary_category,
            'confidence': r.confidence,
        }
        # Add optional fields if present
        if hasattr(r, 'matched_keywords'):
            result_dict['matched_keywords'] = r.matched_keywords
        if hasattr(r, 'needs_review'):
            result_dict['needs_review'] = r.needs_review
        if hasattr(r, 'review_reason'):
            result_dict['review_reason'] = r.review_reason
        if hasattr(r, 'method_used'):
            result_dict['method_used'] = r.method_used

        output_results.append(result_dict)

    # Print summary
    if hasattr(classifier, 'summary'):
        summary = classifier.summary(results)
        print("\nClassification Summary:")
        print(f"  Total: {summary['total']}")
        print("  By category:")
        for cat, count in summary.get('by_category', {}).items():
            print(f"    {cat}: {count}")
        if 'needs_review' in summary:
            print(f"  Needs review: {summary['needs_review']} ({summary.get('needs_review_pct', 0):.1f}%)")
        if 'avg_confidence' in summary:
            print(f"  Avg confidence: {summary['avg_confidence']:.2f}")

    if args.output:
        save_json(output_results, args.output)

    return output_results


def cmd_crosswalk(args):
    """Run crosswalk analysis on grants."""
    from .classifiers.crosswalk import CrosswalkAnalyzer, get_crosswalk

    # Load grants
    with open(args.input) as f:
        grants = json.load(f)

    print(f"Loaded {len(grants)} grants")

    # Get crosswalk config
    if args.preset:
        config = get_crosswalk(args.preset)
        print(f"Using preset: {args.preset}")
    elif args.config:
        config_data = load_config(args.config)
        from .classifiers.crosswalk import CrosswalkConfig, CrosswalkStage
        stages = [CrosswalkStage(**s) for s in config_data.get('stages', [])]
        config = CrosswalkConfig(
            name=config_data.get('name', 'Custom'),
            description=config_data.get('description', ''),
            stages=stages,
            entities=config_data.get('entities', {}),
            known_links=config_data.get('known_links', []),
        )
    else:
        print("Error: Must specify --preset or --config")
        sys.exit(1)

    # Run analysis
    analyzer = CrosswalkAnalyzer(config)

    print("Analyzing grants...")
    for grant in grants:
        analyzer.add_grant(
            grant_id=grant['id'],
            title=grant['title'],
            abstract=grant.get('abstract', ''),
            amount=grant.get('amount', 0),
        )

    # Get results
    summary = analyzer.summary()
    gaps = analyzer.identify_gaps()
    sankey_data = analyzer.generate_sankey_data()

    print("\nCrosswalk Analysis Summary:")
    print(f"  Total grants analyzed: {summary['total_grants_analyzed']}")
    print("  By stage:")
    for stage, data in summary['stages'].items():
        print(f"    {stage}: {data['count']} grants, ${data['funding']:,.0f}")
    print(f"  Total links found: {summary['total_links']}")
    print(f"  Gaps identified: {len(gaps)}")

    if gaps:
        print("\nTop Gaps:")
        for gap in gaps[:5]:
            print(f"  [{gap['severity']}/10] {gap['gap_type']}: {gap['rationale']}")

    # Output
    output = {
        'summary': summary,
        'gaps': gaps,
        'sankey_data': sankey_data,
    }

    if args.output:
        save_json(output, args.output)

    return output


def cmd_pipeline(args):
    """Run full pipeline from config file."""
    config = load_config(args.config)

    print(f"Running pipeline: {config.get('name', 'unnamed')}")

    # Step 1: Fetch
    if 'source' in config:
        print("\n=== FETCH ===")
        from .sources import get_source

        source_type = config['source']['type']
        source = get_source(source_type, config)

        grants = []
        for grant in source.fetch():
            grants.append({
                'id': grant.id,
                'title': grant.title,
                'abstract': grant.abstract,
                'amount': grant.amount,
                'start_date': str(grant.start_date) if grant.start_date else None,
                'end_date': str(grant.end_date) if grant.end_date else None,
                'institution': grant.institution,
                'program': grant.program,
                'source_type': grant.source_type,
                'metadata': grant.metadata,
            })

        print(f"Fetched {len(grants)} grants")

        # Save intermediate
        if config.get('save_intermediate'):
            save_json(grants, f"{config['output_dir']}/grants_raw.json")
    else:
        # Load from file
        input_file = config.get('input_file')
        if input_file:
            with open(input_file) as f:
                grants = json.load(f)
            print(f"Loaded {len(grants)} grants from {input_file}")
        else:
            print("Error: No source or input_file specified")
            sys.exit(1)

    # Step 2: Classify
    if 'classifier' in config:
        print("\n=== CLASSIFY ===")
        from .classifiers import get_classifier

        classifier_config = config['classifier']
        classifier_type = classifier_config.get('type', 'hybrid')

        # Merge categories into classifier config
        if 'categories' in config:
            classifier_config['categories'] = config['categories']

        classifier = get_classifier(classifier_type, classifier_config)

        if hasattr(classifier, 'classify_batch'):
            results = classifier.classify_batch(grants)
        else:
            results = [
                classifier.classify(g['id'], g['title'], g.get('abstract', ''))
                for g in grants
            ]

        # Print summary
        if hasattr(classifier, 'summary'):
            summary = classifier.summary(results)
            print(f"Classified: {summary['total']} grants")
            print(f"  By category: {summary.get('by_category', {})}")
            if 'needs_human_review' in summary:
                print(f"  Needs review: {summary['needs_human_review']}")

        # Export review items
        if hasattr(classifier, 'export_for_review'):
            review_items = classifier.export_for_review(results)
            if review_items:
                review_path = f"{config.get('output_dir', '.')}/review_queue.json"
                save_json(review_items, review_path)
                print(f"  Exported {len(review_items)} items for review")

        # Merge results back into grants
        result_map = {r.grant_id: r for r in results}
        for grant in grants:
            r = result_map.get(grant['id'])
            if r:
                grant['category'] = r.primary_category
                grant['classification_confidence'] = r.confidence
                if hasattr(r, 'method_used'):
                    grant['classification_method'] = r.method_used

        # Save classified
        if config.get('save_intermediate') or config.get('output_dir'):
            out_dir = config.get('output_dir', '.')
            save_json(grants, f"{out_dir}/grants_classified.json")

    # Step 3: Crosswalk analysis (if configured)
    if 'crosswalk' in config:
        print("\n=== CROSSWALK ===")
        from .classifiers.crosswalk import CrosswalkAnalyzer, get_crosswalk

        cw_config = config['crosswalk']
        if 'preset' in cw_config:
            crosswalk = get_crosswalk(cw_config['preset'])
        else:
            from .classifiers.crosswalk import CrosswalkConfig, CrosswalkStage
            stages = [CrosswalkStage(**s) for s in cw_config.get('stages', [])]
            crosswalk = CrosswalkConfig(
                name=cw_config.get('name', 'Custom'),
                description=cw_config.get('description', ''),
                stages=stages,
                entities=cw_config.get('entities', {}),
                known_links=cw_config.get('known_links', []),
            )

        analyzer = CrosswalkAnalyzer(crosswalk)
        for grant in grants:
            analyzer.add_grant(
                grant['id'],
                grant['title'],
                grant.get('abstract', ''),
                grant.get('amount', 0)
            )

        gaps = analyzer.identify_gaps()
        sankey = analyzer.generate_sankey_data()

        print(f"  Found {len(gaps)} funding gaps")

        out_dir = config.get('output_dir', '.')
        save_json({'gaps': gaps, 'sankey': sankey}, f"{out_dir}/crosswalk_analysis.json")

    print("\n=== DONE ===")
    return grants


def cmd_list_sources(args):
    """List available data sources."""
    from .sources import list_sources

    sources = list_sources()

    print("Available data sources:")
    print()

    for name, info in sorted(sources.items()):
        status = "✓" if info['available'] else "✗"
        type_label = f"({info['type']})"
        print(f"  {status} {name:20} {type_label}")

    print()
    print("Core sources are always available.")
    print("Optional sources may require additional dependencies.")


def cmd_list_presets(args):
    """List available classification presets."""
    from .classifiers.keyword import CLASSIFICATION_PRESETS
    from .classifiers.crosswalk import CROSSWALK_PRESETS

    print("Classification presets:")
    for name in CLASSIFICATION_PRESETS:
        print(f"  - {name}")

    print()
    print("Crosswalk presets:")
    for name in CROSSWALK_PRESETS:
        print(f"  - {name}")


def main():
    parser = argparse.ArgumentParser(
        description="Grant Classifier - Categorize research grants from any source",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fetch NSF grants
  python -m grant_classifier.cli fetch --source nsf --config nsf_config.yaml -o grants.json

  # Classify grants
  python -m grant_classifier.cli classify -i grants.json --config classify.yaml -o results.json

  # Run crosswalk analysis
  python -m grant_classifier.cli crosswalk -i grants.json --preset environmental_health -o gaps.json

  # Run full pipeline
  python -m grant_classifier.cli pipeline --config workflow.yaml

  # List available sources
  python -m grant_classifier.cli list-sources
        """
    )

    subparsers = parser.add_subparsers(dest='command', required=True)

    # Fetch command
    fetch_parser = subparsers.add_parser('fetch', help='Fetch grants from a data source')
    fetch_parser.add_argument('--source', '-s', required=True, help='Data source type (nsf, nih_reporter, etc.)')
    fetch_parser.add_argument('--config', '-c', help='Config file (YAML or JSON)')
    fetch_parser.add_argument('--output', '-o', help='Output file')
    fetch_parser.set_defaults(func=cmd_fetch)

    # Classify command
    classify_parser = subparsers.add_parser('classify', help='Classify grants')
    classify_parser.add_argument('--input', '-i', required=True, help='Input grants file (JSON)')
    classify_parser.add_argument('--config', '-c', help='Config file')
    classify_parser.add_argument('--classifier', help='Classifier type (keyword, llm, hybrid)')
    classify_parser.add_argument('--output', '-o', help='Output file')
    classify_parser.set_defaults(func=cmd_classify)

    # Crosswalk command
    crosswalk_parser = subparsers.add_parser('crosswalk', help='Run crosswalk gap analysis')
    crosswalk_parser.add_argument('--input', '-i', required=True, help='Input grants file (JSON)')
    crosswalk_parser.add_argument('--preset', '-p', help='Crosswalk preset (environmental_health, etc.)')
    crosswalk_parser.add_argument('--config', '-c', help='Custom crosswalk config')
    crosswalk_parser.add_argument('--output', '-o', help='Output file')
    crosswalk_parser.set_defaults(func=cmd_crosswalk)

    # Pipeline command
    pipeline_parser = subparsers.add_parser('pipeline', help='Run full pipeline from config')
    pipeline_parser.add_argument('--config', '-c', required=True, help='Pipeline config file')
    pipeline_parser.set_defaults(func=cmd_pipeline)

    # List sources command
    list_sources_parser = subparsers.add_parser('list-sources', help='List available data sources')
    list_sources_parser.set_defaults(func=cmd_list_sources)

    # List presets command
    list_presets_parser = subparsers.add_parser('list-presets', help='List available presets')
    list_presets_parser.set_defaults(func=cmd_list_presets)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
