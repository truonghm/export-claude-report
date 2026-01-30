# export-claude-report

A simple tool to export Deep Research reports from your Claude conversations. To use this tool, you'll need to export your conversations by going to **Settings > Privacy > Export Data** to download conversations (we recommend filtering by date to only include necessary conversations).

## Installation

This package is only available on GitHub. Install it directly from the repository:

```bash
# Install as a tool (recommended)
uv tool install git+https://github.com/truonghm/export-claude-report.git

# Or install as a package
uv pip install git+https://github.com/truonghm/export-claude-report.git
```

## Usage

If you installed with `uv tool install`, run the command directly:

```bash
export-claude-report --path /path/to/conversations.json --output docs
```

If you installed with `uv pip install`, use:

```bash
uv run export-claude-report --path /path/to/conversations.json --output docs
```

## Arguments

- `--path` / `-p` (required): Path to the `conversations.json` file exported from Claude
- `--output` / `-o` (optional): Directory where the exported markdown reports will be saved. Defaults to `docs`

## Examples

Export reports to the default `docs` directory:

```bash
export-claude-report --path conversations.json
```

Export reports to a custom directory:

```bash
export-claude-report --path ~/Downloads/conversations.json --output reports
```

Using short flags:

```bash
export-claude-report -p conversations.json -o my_reports
```
