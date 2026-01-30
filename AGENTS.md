# AI Agent Instructions

## Project Overview

Pelican plugin that adds AI service buttons (ChatGPT, Perplexity, Claude, Gemini, Grok) to articles, allowing readers to analyze and summarize content with one click.

## Development Commands

```bash
pip install -e .           # Install in development mode
pip install -e ".[dev]"    # Install with dev dependencies (if available)
python -c "from pelican_ai_analyzer_bar import register; print('OK')"  # Verify import
```

## Code Style

- Follow existing patterns in codebase
- Use type hints for all public functions
- Docstrings: Google style
- Line length: 88 (Black default)
- Imports: sorted alphabetically

## Commit Convention

Use [Conventional Commits](https://www.conventionalcommits.org/):

| Type | Description |
|------|-------------|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `docs:` | Documentation changes |
| `refactor:` | Code refactoring |
| `test:` | Adding/updating tests |
| `chore:` | Maintenance tasks |

**IMPORTANT: Never add `Co-authored-by` lines to commit messages.**

## Project Structure

```
pelican-ai-analyzer-bar/
├── pelican_ai_analyzer_bar/
│   ├── __init__.py          # Plugin entry point
│   └── ai_analyzer_bar.py   # Core logic
├── pyproject.toml           # Project configuration
├── README.md                # Documentation
├── LICENSE                  # MIT License
└── AGENTS.md                # This file
```

## Adding New AI Services

To add a new AI service, update `AI_SERVICES` dict in `ai_analyzer_bar.py`:

```python
'service_key': {
    'name': 'Display Name',
    'url': 'https://service.com/?q={url}',
    'icon': '<svg>...</svg>',
}
```

Then add corresponding CSS hover color in the theme's stylesheet.

## Testing

Test the plugin by:
1. Installing in a Pelican project: `pip install -e /path/to/pelican-ai-analyzer-bar`
2. Adding to `PLUGINS` in `pelicanconf.py`
3. Running `pelican content` and verifying output

## Security

- Never commit secrets/keys
- URL encoding is handled via `urllib.parse.quote_plus`
- All external links use `rel="noopener noreferrer"`
