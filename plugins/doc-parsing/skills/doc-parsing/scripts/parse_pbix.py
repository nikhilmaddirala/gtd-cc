#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pbixray>=0.1.0",
# ]
# ///
"""
Parse PBIX (Power BI) files using multiple Python methods.

This script extracts content from Microsoft Power BI files using two different methods,
optimized for different use cases: metadata/data extraction or raw content access.

**Note:** PBIX extraction on Linux is limited. Most professional tools require Windows or
Power BI Desktop. These methods focus on Linux-compatible approaches.

Output structure for each file:
    output_dir/filename.pbix/
    ├── parsing_results.json           # File-level metadata and method results
    ├── pbixray/                    # Method 1 output
    │   ├── tables/                # Extracted tables as CSV
    │   │   ├── Table1.csv
    │   │   ├── Table2.csv
    │   │   └── ...
    │   ├── statistics.json        # Model statistics
    │   ├── tables_metadata.json  # Table metadata (rows, columns, types)
    │   ├── measures.json         # DAX measures
    │   └── relationships.json    # Table relationships
    └── zipfile/                     # Method 2 output
        ├── extracted/             # Raw PBIX contents
        │   ├── Report/
        │   ├── DataModel/
        │   ├── DataMashup/
        │   └── Metadata/
        ├── manifest.json         # File manifest
        └── datamodel_schema.json  # DataModel schema (if available)

Methods:

1. pbixray - Extract model metadata, tables, measures, and relationships
   - Python library for parsing Power BI PBIX files
   - Extracts VertiPaq table data
   - Provides model metadata, tables, measures, relationships
   - Exports tables to pandas DataFrames → CSV
   - Output: Tables as CSV, JSON for metadata/measures/relationships

   CLI alternative: None (Python library is best Linux-compatible option)

2. zipfile - Extract raw PBIX contents using zipfile
   - Direct extraction since PBIX files are ZIP archives
   - Access to XML/JSON contents
   - Exposes raw model definition (Model.json)
   - Exposes Power Query M code (MashupDocument.m)
   - Output: Extracted directory structure with all internal files

   CLI alternative: jq + unzip
   - Command: unzip -p "$SOURCE_FILE" "DataModel/Model.json" | jq '.model.tables | keys'
   - Advantages: Fast extraction of metadata, jq allows complex queries on model structure
   - Disadvantages: No table data (only metadata), limited to JSON/XML extraction
   - Best for: Quick metadata inspection, understanding model structure
   - Command to extract query definitions: unzip -p "$SOURCE_FILE" "DataMashup/*/MashupDocument.m" > powerquery.xml

Usage:
    ./parse_pbix.py <file_path> <output_dir>

Arguments:
    file_path  - Path to PBIX file to parse
    output_dir  - Directory where parsed content will be created

Example:
    ./parse_pbix.py /path/to/report.pbix /path/to/output

Dependencies:
    - pbixray>=0.1.0 - Power BI PBIX parsing and data extraction

All dependencies are specified in inline metadata above. Use `uv` to install automatically.

Output Metadata:
    Creates parsing_results.json in output directory with:
    - timestamp: ISO timestamp of parsing
    - source_file: Absolute path to source file
    - output_dir: Output directory path
    - methods: Dict of method_name -> success (bool)
    - success_count: Number of successful methods

Notes:

Method comparison:

pbixray:
- Advantages: Best Linux-compatible option, extracts tables/measures/metadata, exports tables to CSV
- Disadvantages: May not work with all PBIX versions, limited table data extraction for large models
- Best for: Data model analysis and documentation on Linux
- May require: Python 3.8+
- Source: https://github.com/Hugoberry/pbixray

zipfile:
- Advantages: Direct access to XML/JSON contents, exposes raw model definition, exposes Power Query M code
- Disadvantages: No table data (VertiPaq compressed tables not accessible), may need additional tools for parsing extracted XML
- Best for: Debugging and understanding PBIX structure, Power Query analysis
- Sources: https://github.com/microsoft/PowerBI-PbixFileFormat

Linux Limitations:
- pbi-tools (Windows-only): Best PBIX extraction tool but requires Windows
- Power BI Desktop required for full report rendering
- Screenshots of visuals require manual intervention
- Some advanced features may need Windows environment

Recommended Approach for Linux:
1. Use pbixray (Method 1) for data extraction and metadata
2. Use zipfile (Method 2) for quick inspection
3. Manual visual documentation: Take screenshots for key visuals if needed
4. Optional: Windows VM/remote machine for pbi-tools if critical

What Gets Extracted:
- Model metadata: Tables, columns, data types, relationships
- Measures: DAX expressions, format strings
- Table data: VertiPaq compressed tables (via pbixray)
- Power Query: M code and data transformation steps
- Report layout: Visual definitions and positioning

What's Challenging on Linux:
- Embedded visual screenshots (requires Power BI Desktop)
- Interactive report rendering (requires Power BI service/Report Server)
- Some data source connections (may require Windows auth)
- Complex visual configurations

Dual Artifact Strategy for PBIX:
Consider creating two outputs:
1. Semantic artifact: Extracted tables, measures, metadata (CSV/JSON)
2. Visual reference: Screenshots or PDF exports from Windows environment

This ensures:
- Data model is machine-readable and versionable
- Report visuals are documented
- Supports both data analysis and reference use cases

Additional CLI tools (via nix):

jq + unzip combination:
- Command: unzip -p "$SOURCE_FILE" "DataModel/Model.json" | jq '{tables: [.model.tables[] | {name: .Name, columns: [.Columns[] | {name: .Name, type: .DataType}]}, measures: [.model.measures[] | {name: .Name, expression: .Expression}], relationships: [.model.relationships[] | {from: .FromTable, to: .ToTable}]}'
- Extract model structure with jq JSON processing
- Query specific tables: unzip -p "$SOURCE_FILE" "DataModel/Model.json" | jq '.model.tables[].Name'
- Find measures for specific table: unzip -p "$SOURCE_FILE" "DataModel/Model.json" | jq '.model.measures[] | select(.Table == "TableName")'
- Advantages: Fast extraction of metadata, jq allows complex queries on model structure, no Python runtime required
- Disadvantages: Limited to JSON/XML extraction (no table data), requires learning jq syntax
- Best for: Quick metadata inspection, understanding PBIX structure

Windows-only tools (not available on Linux):
- pbi-tools: Best PBIX extraction tool with full feature support
  - Command: pbi-tools extract "$SOURCE_FILE" -o output_dir
  - Extracts all tables, measures, relationships, visuals
  - Source: https://pbi.tools/cli/
- Power BI Desktop: Interactive report rendering and visual screenshots
  - Manual: Open PBIX in Power BI Desktop, export as PDF or take screenshots
"""

import sys
import json
import zipfile
from pathlib import Path
from datetime import datetime
from pbixray import Pbixray


def parse_method1_pbixray(source_file, output_dir):
    """
    Method 1: pbixray for Power BI metadata and data

    Extracts model metadata, tables, measures, and relationships from PBIX file
    using the pbixray Python library. Exports tables to CSV format.

    Advantages:
    - Best Linux-compatible option for PBIX parsing
    - Extracts VertiPaq table data
    - Provides model metadata, tables, measures, relationships
    - Exports tables to pandas DataFrames → CSV

    Disadvantages:
    - May not work with all PBIX versions
    - Limited table data extraction for large models
    - May require Python 3.8+

    When to use:
    - Data model analysis and documentation on Linux
    - When you need table data and metadata
    - When measures and relationships are important
    - For comprehensive PBIX analysis on Linux

    Output:
    - tables/: Directory with CSV files (Table1.csv, Table2.csv, etc.)
    - statistics.json: Model statistics (table count, measure count, relationship count)
    - tables_metadata.json: Table metadata (rows, columns, data types)
    - measures.json: DAX measures with expressions and format strings
    - relationships.json: Table relationships with from/to tables and columns

    Dependencies: pbixray>=0.1.0
    """
    print("    Method 1: pbixray...")
    method_dir = output_dir / "pbixray"
    method_dir.mkdir(exist_ok=True)
    tables_dir = method_dir / "tables"
    tables_dir.mkdir(exist_ok=True)

    try:
        model = Pbixray(str(source_file))

        # Export model statistics
        statistics = {
            "statistics": model.statistics,
            "table_count": len(model.tables),
            "measure_count": len(model.measures),
            "relationship_count": len(model.relationships),
        }

        with open(method_dir / "statistics.json", "w") as f:
            json.dump(statistics, f, indent=2)

        # Export tables metadata
        tables_metadata = {}
        for name, table in model.tables.items():
            tables_metadata[name] = {
                "rows": table.n_rows,
                "columns": [
                    {"name": col.name, "type": str(col.data_type)}
                    for col in table.columns
                ],
            }

            # Export table data as CSV
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

        # Export measures
        measures_data = {}
        for name, measure in model.measures.items():
            measures_data[name] = {
                "expression": measure.expression,
                "format_string": measure.format_string,
                "data_type": str(measure.data_type),
            }

        with open(method_dir / "measures.json", "w") as f:
            json.dump(measures_data, f, indent=2)

        # Export relationships
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
    """
    Method 2: Extract raw PBIX contents using zipfile

    Extracts PBIX contents directly since PBIX files are ZIP archives.
    Provides access to internal structure, XML, and JSON files.

    Advantages:
    - Direct access to XML/JSON contents
    - Exposes raw model definition (Model.json)
    - Exposes Power Query M code (MashupDocument.m)
    - Simple and reliable
    - No special PBIX parsing required

    Disadvantages:
    - No table data (VertiPaq compressed tables not accessible)
    - May need additional tools for parsing extracted XML
    - Limited to what's in the ZIP structure

    When to use:
    - Debugging and understanding PBIX structure
    - Power Query M code analysis
    - When you need raw internal files
    - For manual inspection of model definition

    Output:
    - extracted/: Directory with raw PBIX contents
      Includes Report/, DataModel/, DataMashup/, Metadata/ subdirectories
    - manifest.json: File manifest listing all internal files
    - datamodel_schema.json: DataModel schema (if available)

    CLI alternative: jq + unzip
    - Command: unzip -p "$SOURCE_FILE" "DataModel/Model.json" | jq '.model.tables | keys'
    - Advantages: Fast, jq allows complex queries, no Python runtime
    - Disadvantages: No table data, requires jq syntax knowledge
    """
    print("    Method 2: zipfile extraction...")
    method_dir = output_dir / "zipfile"
    method_dir.mkdir(exist_ok=True)
    extracted_dir = method_dir / "extracted"
    extracted_dir.mkdir(exist_ok=True)

    try:
        with zipfile.ZipFile(source_file, "r") as zip_ref:
            # List all files
            file_list = zip_ref.namelist()

            # Extract all files
            zip_ref.extractall(extracted_dir)

            # Create manifest
            manifest = {
                "total_files": len(file_list),
                "files": file_list,
            }

            with open(method_dir / "manifest.json", "w") as f:
                json.dump(manifest, f, indent=2)

            # Try to extract and format DataModelSchema if it exists
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

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Run all parsing methods
    methods_success = {
        "method1_pbixray": parse_method1_pbixray(source_file, output_dir),
        "method2_zipfile": parse_method2_zipfile(source_file, output_dir),
    }

    success_count = sum(methods_success.values())
    print(f"\n  ✓ Completed: {success_count}/{len(methods_success)} methods successful")

    # Save results
    results = {
        "timestamp": datetime.now().isoformat(),
        "source_file": str(source_file),
        "output_dir": str(output_dir),
        "methods": methods_success,
        "success_count": success_count,
    }

    with open(output_dir / "parsing_results.json", "w") as f:
        json.dump(results, f, indent=2)

    return 0 if success_count > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
