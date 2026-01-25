#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pbixray>=0.1.0",
# ]
# ///
"""
Parse Power BI files using 2 extraction methods: model metadata/tables via pbixray,
and raw ZIP extraction for internal structure.

Usage: ./parse_pbix.py <file_path> <output_dir>
"""

import sys
import json
import zipfile
from pathlib import Path
from datetime import datetime
from pbixray import PBIXRay


def parse_method1_pbixray(source_file, output_dir):
    """Extract model metadata, tables, measures, and relationships using pbixray."""
    print("    Method 1: pbixray...")
    method_dir = output_dir / "pbixray"
    method_dir.mkdir(exist_ok=True)
    tables_dir = method_dir / "tables"
    tables_dir.mkdir(exist_ok=True)

    try:
        model = PBIXRay(str(source_file))

        statistics = {
            "statistics": model.statistics,
            "table_count": len(model.tables),
            "measure_count": len(model.measures),
            "relationship_count": len(model.relationships),
        }

        with open(method_dir / "statistics.json", "w") as f:
            json.dump(statistics, f, indent=2)

        tables_metadata = {}
        for name, table in model.tables.items():
            tables_metadata[name] = {
                "rows": table.n_rows,
                "columns": [
                    {"name": col.name, "type": str(col.data_type)}
                    for col in table.columns
                ],
            }

            table_name_clean = (
                name.replace("/", "_").replace("\\", "_").replace(" ", "_")
            )
            try:
                df = table.to_pandas()
                df.to_csv(tables_dir / f"{table_name_clean}.csv", index=False)
            except Exception as e:
                print(f"        ⚠ Could not export table {name}: {str(e)[:50]}")

        with open(method_dir / "tables_metadata.json", "w") as f:
            json.dump(tables_metadata, f, indent=2)

        measures_data = {}
        for name, measure in model.measures.items():
            measures_data[name] = {
                "expression": measure.expression,
                "format_string": measure.format_string,
                "data_type": str(measure.data_type),
            }

        with open(method_dir / "measures.json", "w") as f:
            json.dump(measures_data, f, indent=2)

        relationships_data = []
        for rel in model.relationships:
            relationships_data.append(
                {
                    "from_table": rel.from_table,
                    "to_table": rel.to_table,
                    "from_columns": rel.from_columns,
                    "to_columns": rel.to_columns,
                }
            )

        with open(method_dir / "relationships.json", "w") as f:
            json.dump(relationships_data, f, indent=2)

        print(
            f"      ✓ Extracted {len(model.tables)} tables, {len(model.measures)} measures, {len(model.relationships)} relationships"
        )
        return True
    except Exception as e:
        print(f"      ⚠ Failed: {str(e)[:100]}")
        return False


def parse_method2_zipfile(source_file, output_dir):
    """Extract raw PBIX ZIP contents for internal structure inspection."""
    print("    Method 2: zipfile extraction...")
    method_dir = output_dir / "zipfile"
    method_dir.mkdir(exist_ok=True)
    extracted_dir = method_dir / "extracted"
    extracted_dir.mkdir(exist_ok=True)

    try:
        with zipfile.ZipFile(source_file, "r") as zip_ref:
            file_list = zip_ref.namelist()

            zip_ref.extractall(extracted_dir)

            manifest = {
                "total_files": len(file_list),
                "files": file_list,
            }

            with open(method_dir / "manifest.json", "w") as f:
                json.dump(manifest, f, indent=2)

            if "DataModelSchema" in file_list:
                try:
                    schema_data = zip_ref.read("DataModelSchema")
                    schema_json = json.loads(schema_data)
                    with open(method_dir / "datamodel_schema.json", "w") as f:
                        json.dump(schema_json, f, indent=2)
                except:
                    pass

        print(f"      ✓ Extracted {len(file_list)} files from PBIX archive")
        return True
    except Exception as e:
        print(f"      ⚠ Failed: {str(e)[:100]}")
        return False


def main():
    if len(sys.argv) != 3:
        print("Usage: ./parse_pbix.py <file_path> <output_dir>")
        sys.exit(1)

    source_file = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])

    if not source_file.exists():
        print(f"Error: File not found: {source_file}")
        sys.exit(1)

    print(f"Parsing PBIX: {source_file.name}")
    print(f"Output directory: {output_dir}")
    print()

    output_dir.mkdir(parents=True, exist_ok=True)

    methods_success = {
        "method1_pbixray": parse_method1_pbixray(source_file, output_dir),
        "method2_zipfile": parse_method2_zipfile(source_file, output_dir),
    }

    success_count = sum(methods_success.values())
    print(f"\n  ✓ Completed: {success_count}/{len(methods_success)} methods successful")

    results = {
        "timestamp": datetime.now().isoformat(),
        "source_file": str(source_file),
        "output_dir": str(output_dir),
        "methods": methods_success,
        "success_count": success_count,
    }

    with open(output_dir / "parsing_summary.json", "w") as f:
        json.dump(results, f, indent=2)

    return 0 if success_count > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
