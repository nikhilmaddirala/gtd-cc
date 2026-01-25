# Troubleshooting PPTX to Markdown Conversion

Common issues and solutions when using the conversion script.

## Required System Packages

The script requires two system-level tools:

- libreoffice (provides `soffice` command)
- poppler-utils (provides `pdftoppm` command)

Install via your package manager:

- Debian/Ubuntu: `sudo apt install libreoffice poppler-utils`
- macOS: `brew install libreoffice poppler`
- Fedora/RHEL: `sudo dnf install libreoffice poppler-utils`
- Arch: `sudo pacman -S libreoffice poppler`
- NixOS: Add to system packages or use `nix shell nixpkgs#libreoffice nixpkgs#poppler-utils nixpkgs#stdenv.cc.cc.lib`

For NixOS users: The stdenv.cc.cc.lib package provides the C++ standard library needed by markitdown's dependencies (numpy, pandas).

## LibreOffice Conversion Issues

### Problem: soffice command not found

**Error message:**
```
❌ Error: soffice not found. Install LibreOffice
```

**Solution:**
Install LibreOffice using your package manager. See the "Required System Packages" section above for installation commands for your operating system.

### Problem: LibreOffice fails to convert

**Symptoms:**
- Conversion completes but PDF is corrupted or missing
- Strange formatting in output
- Process hangs

**Solutions:**
1. Try opening and re-saving the PPTX file manually in LibreOffice first
2. Check for corrupted slides or unsupported PowerPoint features
3. Use `--infilter="impress8"` flag for specific formats:
   ```bash
   soffice --headless --infilter="impress8" --convert-to pdf "file.pptx" --outdir pdf/
   ```
4. Ensure file path has no special characters
5. Check LibreOffice version: `soffice --version` (recommend 7.0+)

## Image Export Issues

### Problem: No slide images generated

**Symptoms:**
- PDF conversion succeeds but no `.jpg` files in `slide-images/`
- Error about pdftoppm not found

**Solutions:**
1. Ensure poppler-utils is installed on your system (see Required System Packages section above)
2. Verify pdftoppm is available: `pdftoppm -h`
3. Manual image extraction:
   ```bash
   pdftoppm -jpeg -r 150 "presentation.pdf" slide-images/slide
   ```

### Problem: Images are too large or too small

**Issue:** Generated images have wrong dimensions or file size

**Solutions:**
Adjust DPI using the `--dpi` flag:

```bash
# Higher quality, larger files (300 DPI)
./convert_pptx_to_markdown.py input.pptx output/ --dpi 300

# Lower quality, smaller files (100 DPI)
./convert_pptx_to_markdown.py input.pptx output/ --dpi 100

# Recommended balance (150 DPI - default)
./convert_pptx_to_markdown.py input.pptx output/ --dpi 150
```

**File size comparison:**
- 100 DPI: ~50-100 KB per slide
- 150 DPI: ~100-200 KB per slide (recommended)
- 300 DPI: ~300-500 KB per slide

## Text Extraction Issues

### Problem: System library errors with markitdown

**Error messages:**
```
ImportError: libstdc++.so.6: cannot open shared object file
OSError: library not found
```

**Cause:** Markitdown has C extensions (numpy, pandas) requiring system libraries (libstdc++.so.6)

**Solutions:**

Most systems: The required libraries are installed by default. If you encounter this error:

1. Linux (Debian/Ubuntu): Install build-essential
   ```bash
   sudo apt install build-essential
   ```

2. NixOS: Run the script with C++ standard library available
   ```bash
   nix shell nixpkgs#stdenv.cc.cc.lib --command \
     ./scripts/convert_pptx_to_markdown.py input.pptx output/
   ```

3. Alternative: Use pure Python extraction (simpler but less formatted)
   ```python
   # Install: uv pip install python-pptx
   from pptx import Presentation
   prs = Presentation("file.pptx")
   for i, slide in enumerate(prs.slides, 1):
       print(f"<!-- Slide number: {i} -->")
       for shape in slide.shapes:
           if hasattr(shape, "text"):
               print(shape.text)
   ```

### Problem: No slide markers in extracted text

**Symptoms:**
```
✗ No slide markers found in extracted text
   Expected markers like: <!-- Slide number: 1 -->
```

**Cause:** markitdown didn't insert slide boundary comments

**Solutions:**
1. Check markitdown version: `python -m markitdown --version`
2. Inspect the extracted text file manually: `cat output/*-text.md`
3. If using alternative extraction tool, add markers manually or adjust script regex
4. Update the script's `split_into_slides()` function to match your marker format

## Markdown Assembly Issues

### Problem: Missing or broken image links

**Symptoms:**
- Markdown shows broken image icons
- Images don't display when viewing markdown

**Solutions:**
1. Verify images exist: `ls output/slide-images/slide-*.jpg`
2. Check image naming matches expected pattern: `slide-01.jpg`, `slide-02.jpg`, etc.
3. Verify relative paths are correct from markdown file location
4. If images are in different location, use `--images-dir` option (future enhancement)

### Problem: Slide content appears jumbled

**Symptoms:**
- Text from multiple slides merged
- Slide boundaries unclear

**Cause:** Slide splitting regex doesn't match the marker format

**Solutions:**
1. Examine text file for actual marker format: `grep -n "Slide" output/*-text.md`
2. Common patterns:
   - `<!-- Slide number: N -->` (markitdown default)
   - `Slide N:` (some parsers)
   - `---\nPage N\n---` (some converters)
3. Modify script if needed (edit `split_into_slides()` function)

## Permission and Path Issues

### Problem: Permission denied errors

**Error messages:**
```
Permission denied: '/path/to/output'
mkdir: cannot create directory
```

**Solutions:**
1. Check write permissions: `ls -la output_dir/`
2. Create output directory first: `mkdir -p output/`
3. Avoid protected paths (system directories, read-only mounts)
4. Check symlink targets have write access

### Problem: File path with spaces fails

**Symptoms:**
- Command fails with "file not found" even though file exists
- Error shows truncated path

**Solutions:**
1. Always quote paths with spaces:
   ```bash
   ./convert_pptx_to_markdown.py "My Presentation.pptx" "output dir/"
   ```
2. Or use paths without spaces:
   ```bash
   ./convert_pptx_to_markdown.py My_Presentation.pptx output_dir/
   ```

## NixOS-Specific Issues

This section is for NixOS users who want to use `nix shell` to provide dependencies.

### Using nix shell to provide dependencies

NixOS users can use nix shell instead of installing packages system-wide:

```bash
nix shell nixpkgs#libreoffice nixpkgs#poppler-utils nixpkgs#stdenv.cc.cc.lib --command \
  ./scripts/convert_pptx_to_markdown.py input.pptx output/
```

The stdenv.cc.cc.lib package provides the C++ standard library needed by markitdown.

### Problem: Nix evaluation fails

**Error message:**
```
error: getting status of '/nix/store/...': No such file or directory
```

**Solutions:**
1. Update nix channels:
   ```bash
   nix-channel --update
   ```
2. Try with explicit nixpkgs:
   ```bash
   nix shell github:NixOS/nixpkgs/nixos-unstable#poppler-utils --command ...
   ```
3. Clear nix cache if corrupted:
   ```bash
   nix-collect-garbage -d
   ```

## Performance Issues

### Problem: Conversion is very slow

**Symptoms:**
- Takes minutes to convert small presentations
- Process appears hung

**Solutions:**
1. LibreOffice startup overhead is normal (5-10 seconds)
2. For batch processing, keep soffice process running
3. Monitor progress: script shows step-by-step status
4. Large presentations (>50 slides, embedded videos) take longer
5. Check system resources: `top` or `htop`

### Problem: High memory usage

**Cause:** Large presentations or high DPI settings

**Solutions:**
1. Reduce image DPI: `--dpi 100` instead of default 150
2. Process presentations in batches rather than all at once
3. Clear `/tmp/` if full of LibreOffice temporary files
4. Close other applications during conversion

## Output Validation

### Checklist for successful conversion

Verify these after conversion:

- [ ] PDF exists in `output/pdf/`
- [ ] All slide images present in `output/slide-images/` (count matches slide count)
- [ ] Text file created: `output/*-text.md`
- [ ] Final markdown created: `output/*.md`
- [ ] Image references in markdown are valid (check one manually)
- [ ] Markdown renders properly when viewed
- [ ] No error messages in console output

### How to check slide count

```bash
# Count PDF pages
pdfinfo output/pdf/presentation.pdf | grep Pages

# Count generated images
ls output/slide-images/slide-*.jpg | wc -l

# Count slides in markdown
grep "^## Slide" output/presentation.md | wc -l
```

All three should match!

## Getting Help

If issues persist after trying these solutions:

1. Check script output for specific error messages
2. Run with verbose shell debugging:
   ```bash
   bash -x ./convert_pptx_to_markdown.py input.pptx output/
   ```
3. Test each step manually:
   - PPTX → PDF: `soffice --headless --convert-to pdf file.pptx`
   - PDF → Images: `pdftoppm -jpeg -r 150 file.pdf slide`
   - Text extraction: `python -m markitdown file.pptx`
4. Check for file corruption: Try with a different PPTX file
5. Verify all dependencies are working individually

## Common Workflow Tips

### Best practices for reliable conversion

1. **Test with simple presentation first** - Verify setup before processing complex files
2. **Keep originals safe** - Never modify source files in shared folders
3. **Use descriptive output directories** - `output/presentation-name/` not just `output/`
4. **Check results immediately** - Validate each conversion before moving to alt-text generation
5. **Document customizations** - Note any special handling needed for specific presentations

### Batch conversion pattern

For multiple presentations:

```bash
#!/bin/bash
for pptx in source/*.pptx; do
    name=$(basename "$pptx" .pptx)
    ./convert_pptx_to_markdown.py "$pptx" "output/$name/"
done
```

### Integration with version control

Recommended .gitignore for conversion projects:

```gitignore
# Intermediate files (optional to track)
output/*/pdf/
output/*/-text.md

# Always ignore uv cache
~/.cache/uv/

# Keep these in version control
!output/*/*.md
!output/*/slide-images/
```
