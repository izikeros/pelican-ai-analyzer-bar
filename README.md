# Pelican AI Analyzer Bar

A Pelican plugin that adds clickable AI service buttons to your articles, allowing readers to analyze and summarize content with one click using ChatGPT, Perplexity, Claude, Gemini, or Grok.

## Installation

```bash
pip install pelican-ai-analyzer-bar
```

Or install from source:

```bash
pip install -e /path/to/pelican-ai-analyzer-bar
```

## Configuration

Add to your `pelicanconf.py`:

```python
PLUGINS = [
    # ... other plugins
    'pelican_ai_analyzer_bar',
]

AI_ANALYZER_BAR = {
    'enabled': True,
    'services': ['chatgpt', 'perplexity', 'claude', 'gemini', 'grok'],
    'position': 'after_header',  # 'after_header', 'after_summary', or 'both'
    'text': 'Summarize and analyze this article with:',
    'exclude_categories': ['note', 'til'],
    'exclude_paths': [],
}
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enabled` | bool | `True` | Enable/disable the plugin globally |
| `services` | list | All 5 services | Which AI services to show |
| `position` | str | `'after_header'` | Where to display the bar |
| `text` | str | `'Summarize and analyze this article with:'` | Text shown before buttons |
| `exclude_categories` | list | `[]` | Categories to exclude |
| `exclude_paths` | list | `[]` | URL paths to exclude |

### Available Services

- `chatgpt` - OpenAI ChatGPT
- `perplexity` - Perplexity AI
- `claude` - Anthropic Claude
- `gemini` - Google Gemini
- `grok` - xAI Grok

## Per-Article Control

Disable the bar for a specific article using frontmatter:

```markdown
Title: My Article
ai_analyzer_bar: false

Content here...
```

## Theme Integration

Your theme needs to include the bar HTML. For Flex theme, add to `article.html`:

```jinja2
{% if article.ai_analyzer_bar_html %}
    {% set position = article.ai_analyzer_bar_position or 'after_header' %}
    {% if position in ['after_header', 'both'] %}
        <div class="ai-analyzer-bar">
            {{ article.ai_analyzer_bar_html|safe }}
        </div>
    {% endif %}
{% endif %}
```

See the CSS styling section in the Flex theme for required styles.

## License

MIT License
