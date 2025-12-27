#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pandas>=2.0.0",
#   "openpyxl>=3.1.0",
# ]
# ///
"""
Parse XLSX (Excel) files using multiple Python methods.

This script extracts content from Microsoft Excel spreadsheets using four different methods,
each optimized for different use cases: basic extraction, structure analysis, detailed statistics,
or formula extraction.

Output structure for each file:
    output_dir/filename.xlsx/
    ├── parsing_results.json           # File-level metadata and method results
    ├── pandas_basic/                # Method 1 output
    │   ├── csv/                    # CSV files for each sheet
    │   │   ├── Sheet1.csv
    │   │   ├── Sheet2.csv
    │   │   └── ...
    │   └── metadata.json          # Workbook metadata (sheets, rows, columns)
    ├── openpyxl_structure/         # Method 2 output
    │   ├── Sheet1.json            # Sheet data as JSON
    │   ├── Sheet2.json
    │   ├── workbook_metadata.json # Workbook info (sheets, dimensions)
    ├── pandas_detailed/            # Method 3 output
    │   ├── statistics/            # Per-sheet analysis
    │   │   ├── Sheet1_analysis.json
    │   │   ├── Sheet2_analysis.json
    │   │   └── ...
    │   └── sheets_analysis.json   # Overall analysis (dtypes, missing values, statistics)
    └── openpyxl_formulas/         # Method 4 output
        └── formulas.json          # Extracted formulas with cell locations

Methods:

1. pandas (basic) - Extract all sheets as CSV files with metadata
   - Reads all sheets using pandas
   - Exports each sheet as CSV
   - Creates metadata with sheet, row, and column counts
   - Clean CSV format
   - Output: CSV files + metadata.json

   CLI alternative: in2csv (csvkit)
   - Command: nix run nixpkgs#csvkit -- in2csv "$SOURCE_FILE" --write-sheets
   - Advantages: Fast conversion, handles multiple sheets with --write-sheets option
   - Disadvantages: May simplify formatting, part of csvkit suite required

   CLI alternative: csvtk
   - Command: csvtk xlsx2csv "$SOURCE_FILE" -n "SheetName" > sheet1.csv
   - Advantages: Can filter by sheet name, supports piping to other csvtk tools
   - Disadvantages: More complex for multiple sheets

2. openpyxl (structure) - Extract sheets with formatting and structure info
   - Reads workbook structure using openpyxl
   - Extracts dimensions for each sheet
   - Saves sheet data as JSON arrays
   - Captures workbook-level metadata
   - Output: JSON files per sheet + workbook metadata

   CLI alternative: LibreOffice CLI
   - Command: nix shell nixpkgs#libreoffice --command bash -c "libreoffice --headless --convert-to csv '$SOURCE_FILE' && libreoffice --headless --convert-to pdf '$SOURCE_FILE'"
   - Advantages: Creates both CSV (data) and PDF (visuals), PDF preserves charts/formatting
   - Disadvantages: Requires LibreOffice via nix, heavy dependency
   - Best for: Dual artifact approach (semantic + visual fidelity)

3. pandas (detailed) - Extract with data types and statistics
   - Reads all sheets with pandas
   - Analyzes data types for each column
   - Calculates statistics for numeric columns
   - Counts missing values
   - Creates detailed JSON analysis per sheet
   - Output: Statistics JSON files + overall analysis

   CLI alternative: None (Python library is best option for detailed analysis)

4. openpyxl (formulas) - Extract formulas and calculated values
   - Loads workbook without evaluating formulas
   - Extracts formula strings from cells
   - Tracks cell coordinates for each formula
   - Captures formula expressions (not just calculated values)
   - Output: Formulas JSON with cell locations and expressions

   CLI alternative: jq + unzip
   - Command: unzip -p "$SOURCE_FILE" "DataModel/Model.json" | jq '.model.measures[] | {name: .Name, expression: .Expression}'
   - Advantages: Fast extraction of metadata, no Python runtime required
   - Disadvantages: Limited to JSON/XML extraction, no table data
   - Best for: Quick metadata inspection

Usage:
    ./parse_xlsx.py <file_path> <output_dir>

Arguments:
    file_path  - Path to XLSX file to parse
    output_dir  - Directory where parsed content will be created

Example:
    ./parse_xlsx.py /path/to/spreadsheet.xlsx /path/to/output

Dependencies:
    - pandas>=2.0.0 - Data analysis and CSV export
    - openpyxl>=3.1.0 - Excel file parsing

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

pandas (basic):
- Advantages: Fast, standard CSV format, includes metadata
- Disadvantages: Simplifies formatting, formulas evaluated as values (not preserved)
- Best for: Data export, analysis, machine-readable formats
- C library required: nixpkgs#stdenv.cc.cc.lib (on NixOS)
- Source: https://pandas.pydata.org/docs/user_guide/io.html

openpyxl (structure):
- Advantages: Preserves structure, dimensions info, JSON format
- Disadvantages: Slower than pandas, more complex output
- Best for: Structure analysis, understanding workbook layout
- Source: https://openpyxl.readthedocs.io/

pandas (detailed):
- Advantages: Comprehensive analysis, data types, statistics, missing values
- Disadvantages: Slower, requires more memory for large files
- Best for: Data quality analysis, understanding data characteristics
- C library required: nixpkgs#stdenv.cc.cc.lib (on NixOS)

openpyxl (formulas):
- Advantages: Preserves formulas (not just calculated values), captures cell locations
- Disadvantages: No data values, only formulas
- Best for: Formula analysis, understanding business logic, auditing
- Source: https://openpyxl.readthedocs.io/

CLI alternatives (via nix) detailed:

in2csv (csvkit):
- Command: nix run nixpkgs#csvkit -- in2csv "$SOURCE_FILE" --write-sheets
- Fast conversion from XLSX to CSV
- Handles multiple sheets with --write-sheets option
- Convert specific sheet: in2csv "$SOURCE_FILE" --sheet "SheetName" -o sheet1.csv
- List sheets first: in2csv "$SOURCE_FILE" --sheet - | head -20
- Advantages: Fast, handles multiple sheets, part of csvkit suite
- Disadvantages: May simplify formatting, preserves data values but not formulas
- Source: https://csvkit.readthedocs.io/en/latest/scripts/in2csv.html

csvtk:
- Command: csvtk xlsx2csv "$SOURCE_FILE" -n "SheetName" > sheet1.csv
- Convert all sheets: csvtk xlsx2csv "$SOURCE_FILE" --list-sheets
- Pipes with other csvtk tools: csvtk xlsx2csv "$SOURCE_FILE" | csvtk pretty
- Advantages: Can filter by sheet name, supports piping to other csvtk tools
- Disadvantages: More complex for multiple sheets, separate tool to install
- Source: https://github.com/shenwei356/csvtk

LibreOffice:
- Command: nix shell nixpkgs#libreoffice --command bash -c "libreoffice --headless --convert-to csv '$SOURCE_FILE' && libreoffice --headless --convert-to pdf '$SOURCE_FILE'"
- Creates both CSV (data) and PDF (visuals)
- PDF preserves charts, formatting, and layout
- Advantages: Best dual artifact approach (semantic + visual), PDF serves as visual reference for charts
- Disadvantages: Heavy dependency, requires LibreOffice via nix
- Best for: When you need both data and visual reference
- Source: https://help.libreoffice.org/latest/en-US/text/swriter/guide/convert.html

Dual Artifact Strategy for XLSX:
XLSX files often contain:
1. Semantic data (values, formulas) → CSV/JSON
2. Visual artifacts (charts, formatting) → PDF/snapshots

Using both ensures:
- Data is machine-readable (CSV/JSON)
- Visuals are preserved (PDF)
- Charts and formatting are referenceable
- Supports both analysis and reference use cases

Chart Extraction Limitation:
Most CLI tools cannot extract charts as images. Options:
- LibreOffice PDF preserves chart visuals
- Manual screenshotting for specific charts
- Use Python libraries (openpyxl + matplotlib) for custom extraction
"""

import sys
import json
from pathlib import Path
from datetime import datetime
import pandas as pd
from openpyxl import load_workbook


def parse_method1_pandas(source_file, output_dir):
    """
    Method 1: pandas for CSV export with metadata

    Extracts all sheets from XLSX file using pandas and exports each as CSV.
    Creates workbook metadata with sheet, row, and column information.

    Advantages:
    - Fast CSV export
    - Standard format for data analysis
    - Handles multiple sheets automatically
    - Includes metadata (rows, columns per sheet)

    Disadvantages:
    - Formulas evaluated as values (not preserved)
    - May simplify formatting
    - Requires C library on NixOS

    When to use:
    - Data export and analysis
    - Standard CSV format needed
    - Multiple sheets need processing
    - Machine-readable format required

    Output:
    - csv/: Directory with CSV files (Sheet1.csv, Sheet2.csv, etc.)
    - metadata.json: Workbook metadata including sheets, rows, columns

    Dependencies: pandas>=2.0.0, openpyxl>=3.1.0

    CLI alternatives:
    - in2csv: nix run nixpkgs#csvkit -- in2csv "$SOURCE_FILE" --write-sheets
    - csvtk: csvtk xlsx2csv "$SOURCE_FILE"

    C library required: nixpkgs#stdenv.cc.cc.lib (on NixOS or containerized environments)
    Command: nix shell nixpkgs#stdenv.cc.cc.lib --command bash -c "export LD_LIBRARY_PATH=$(nix eval --raw nixpkgs#stdenv.cc.cc.lib)/lib:$LD_LIBRARY_PATH && <command>"
    """
    print("    Method 1: pandas (basic)...")
    method_dir = output_dir / "pandas_basic"
    method_dir.mkdir(exist_ok=True)
    csv_dir = method_dir / "csv"
    csv_dir.mkdir(exist_ok=True)

    try:
        # Read all sheets
        excel_data = pd.read_excel(source_file, sheet_name=None, engine="openpyxl")

        # Export each sheet as CSV
        for sheet_name, df in excel_data.items():
            sheet_name_clean = (
                sheet_name.replace("/", "_").replace("\\", "_").replace(" ", "_")
            )
            csv_path = csv_dir / f"{sheet_name_clean}.csv"
            df.to_csv(csv_path, index=False)

        # Create metadata
        metadata = {
            "sheets": list(excel_data.keys()),
            "source": str(source_file),
            "rows": {name: len(df) for name, df in excel_data.items()},
            "columns": {name: list(df.columns) for name, df in excel_data.items()},
        }

        with open(method_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)

        print(f"      ✓ Extracted {len(excel_data)} sheets as CSV")
        return True
    except Exception as e:
        print(f"      ⚠ Failed: {str(e)[:100]}")
        return False


def parse_method2_openpyxl(source_file, output_dir):
    """
    Method 2: openpyxl for detailed sheet information

    Extracts workbook structure and sheet data using openpyxl library.
    Captures dimensions, saves data as JSON, and creates workbook metadata.

    Advantages:
    - Preserves workbook structure
    - Captures sheet dimensions
    - JSON format for programmatic access
    - No formula evaluation (reads raw values)

    Disadvantages:
    - Slower than pandas
    - More complex output structure
    - Data as JSON (less common than CSV)

    When to use:
    - Structure analysis needed
    - Understanding workbook layout
    - JSON format preferred
    - When raw values (not calculated) are needed

    Output:
    - Sheet1.json, Sheet2.json, ...: Sheet data as JSON arrays
    - workbook_metadata.json: Workbook info (sheets, sheet count, dimensions)

    Dependencies: openpyxl>=3.1.0

    CLI alternatives:
    - LibreOffice PDF: See Dual Artifact Strategy below
    - jq + unzip: unzip -p "$SOURCE_FILE" "DataModel/Model.json" | jq '...'
    """
    print("    Method 2: openpyxl (structure)...")
    method_dir = output_dir / "openpyxl_structure"
    method_dir.mkdir(exist_ok=True)

    try:
        wb = load_workbook(source_file, data_only=True)

        # Extract sheet info
        sheets_info = {}
        for sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
            sheets_info[sheet_name] = {
                "max_row": ws.max_row,
                "max_column": ws.max_column,
                "dimensions": ws.dimensions,
            }

        metadata = {
            "workbook": str(source_file),
            "sheets": wb.sheetnames,
            "sheet_count": len(wb.sheetnames),
            "sheet_details": sheets_info,
        }

        with open(method_dir / "workbook_metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)

        # Export data from each sheet
        for sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
            sheet_name_clean = (
                sheet_name.replace("/", "_").replace("\\", "_").replace(" ", "_")
            )

            # Extract values as list of lists
            data = []
            for row in ws.iter_rows(values_only=True):
                data.append([str(cell) if cell is not None else "" for cell in row])

            # Save as JSON
            with open(method_dir / f"{sheet_name_clean}.json", "w") as f:
                json.dump(data, f, indent=2)

        print(f"      ✓ Extracted {len(wb.sheetnames)} sheets with metadata")
        return True
    except Exception as e:
        print(f"      ⚠ Failed: {str(e)[:100]}")
        return False


def parse_method3_pandas_detailed(source_file, output_dir):
    """
    Method 3: pandas with data type analysis and statistics

    Extracts all sheets and performs detailed analysis using pandas.
    Captures data types, statistics for numeric columns, and missing value counts.

    Advantages:
    - Most comprehensive data analysis
    - Captures data types per column
    - Calculates statistics for numeric data
    - Counts missing values
    - Per-sheet and overall analysis

    Disadvantages:
    - Slower than basic methods
    - Requires more memory for large files
    - Formulas evaluated as values

    When to use:
    - Data quality analysis
    - Understanding data characteristics
    - When statistics are needed
    - Identifying data issues (missing values, types)

    Output:
    - statistics/: Directory with per-sheet analysis JSON
    - sheets_analysis.json: Overall analysis with dtypes, missing values, statistics

    Dependencies: pandas>=2.0.0, openpyxl>=3.1.0

    C library required: nixpkgs#stdenv.cc.cc.lib (on NixOS)
    """
    print("    Method 3: pandas (detailed)...")
    method_dir = output_dir / "pandas_detailed"
    method_dir.mkdir(exist_ok=True)
    stats_dir = method_dir / "statistics"
    stats_dir.mkdir(exist_ok=True)

    try:
        # Read all sheets
        excel_data = pd.read_excel(source_file, sheet_name=None, engine="openpyxl")

        sheets_analysis = {}

        for sheet_name, df in excel_data.items():
            sheet_name_clean = (
                sheet_name.replace("/", "_").replace("\\", "_").replace(" ", "_")
            )

            # Analyze data types
            dtypes_info = {col: str(dtype) for col, dtype in df.dtypes.items()}

            # Get basic statistics for numeric columns
            stats = {}
            try:
                numeric_stats = df.describe().to_dict()
                stats["numeric"] = numeric_stats
            except:
                pass

            # Count missing values
            missing = df.isnull().sum().to_dict()

            # Store analysis
            sheets_analysis[sheet_name] = {
                "shape": df.shape,
                "columns": list(df.columns),
                "dtypes": dtypes_info,
                "missing_values": {k: int(v) for k, v in missing.items()},
                "statistics": stats,
            }

            # Save statistics to file
            with open(stats_dir / f"{sheet_name_clean}_analysis.json", "w") as f:
                json.dump(sheets_analysis[sheet_name], f, indent=2)

        # Save overall analysis
        with open(method_dir / "sheets_analysis.json", "w") as f:
            json.dump(sheets_analysis, f, indent=2)

        print(f"      ✓ Analyzed {len(excel_data)} sheets with statistics")
        return True
    except Exception as e:
        print(f"      ⚠ Failed: {str(e)[:100]}")
        return False


def parse_method4_openpyxl_formulas(source_file, output_dir):
    """
    Method 4: openpyxl to extract formulas and calculated values

    Loads workbook without evaluating formulas to capture formula strings.
    Tracks cell coordinates for each formula and saves them as JSON.

    Advantages:
    - Preserves formulas (not just calculated values)
    - Captures cell coordinates
    - Can analyze business logic and dependencies
    - Useful for auditing and understanding calculations

    Disadvantages:
    - Does not provide data values (only formulas)
    - Limited to formula cells
    - May be incomplete for complex formulas

    When to use:
    - Formula analysis and auditing
    - Understanding business logic
    - When you need to see formulas, not just values
    - Dependency tracking

    Output:
    - formulas.json: Extracted formulas with cell locations and expressions
      Format: {"SheetName": [{"cell": "A1", "row": 1, "col": 1, "formula": "=SUM(B1:B10)"}, ...]}

    Dependencies: openpyxl>=3.1.0

    CLI alternative: jq + unzip
    - Command: unzip -p "$SOURCE_FILE" "DataModel/Model.json" | jq '.model.measures[] | {name: .Name, expression: .Expression}'
    - Advantages: Fast, no Python runtime required
    - Disadvantages: Limited to JSON/XML extraction, no table data
    - Best for: Quick metadata inspection
    """
    print("    Method 4: openpyxl (formulas)...")
    method_dir = output_dir / "openpyxl_formulas"
    method_dir.mkdir(exist_ok=True)

    try:
        # Load workbook without evaluating formulas to get formulas
        wb = load_workbook(source_file, data_only=False)

        formulas_data = {}

        for sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
            sheet_formulas = []

            # Find cells with formulas
            for row_idx, row in enumerate(ws.iter_rows(), 1):
                for col_idx, cell in enumerate(row, 1):
                    if (
                        cell.value
                        and isinstance(cell.value, str)
                        and cell.value.startswith("=")
                    ):
                        sheet_formulas.append(
                            {
                                "cell": cell.coordinate,
                                "row": row_idx,
                                "col": col_idx,
                                "formula": cell.value,
                            }
                        )

            if sheet_formulas:
                formulas_data[sheet_name] = sheet_formulas

        # Save formulas
        with open(method_dir / "formulas.json", "w") as f:
            json.dump(formulas_data, f, indent=2)

        total_formulas = sum(len(formulas) for formulas in formulas_data.values())
        print(
            f"      ✓ Extracted {total_formulas} formulas from {len(formulas_data)} sheets"
        )
        return True
    except Exception as e:
        print(f"      ⚠ Failed: {str(e)[:100]}")
        return False


def main():
    if len(sys.argv) != 3:
        print("Usage: ./parse_xlsx.py <file_path> <output_dir>")
        sys.exit(1)

    source_file = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])

    if not source_file.exists():
        print(f"Error: File not found: {source_file}")
        sys.exit(1)

    print(f"Parsing XLSX: {source_file.name}")
    print(f"Output directory: {output_dir}")
    print()

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Run all parsing methods
    methods_success = {
        "method1_pandas_basic": parse_method1_pandas(source_file, output_dir),
        "method2_openpyxl_structure": parse_method2_openpyxl(source_file, output_dir),
        "method3_pandas_detailed": parse_method3_pandas_detailed(
            source_file, output_dir
        ),
        "method4_openpyxl_formulas": parse_method4_openpyxl_formulas(
            source_file, output_dir
        ),
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
