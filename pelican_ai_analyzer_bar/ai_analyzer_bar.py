"""
AI Analyzer Bar Plugin for Pelican
Adds clickable buttons to analyze articles with AI services like ChatGPT, Perplexity, Claude, etc.
"""

import logging
from urllib.parse import quote_plus

from pelican import signals

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    'enabled': True,
    'services': ['chatgpt', 'perplexity', 'claude', 'gemini', 'grok'],
    'position': 'after_header',
    'text': 'Summarize and analyze this article with:',
    'exclude_categories': [],
    'exclude_paths': [],
}

AI_SERVICES = {
    'chatgpt': {
        'name': 'ChatGPT',
        'url': 'https://chat.openai.com/?q={url}',
        'icon': '''<svg viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="M22.2819 9.8211a5.9847 5.9847 0 0 0-.5157-4.9108 6.0462 6.0462 0 0 0-6.5098-2.9A6.0651 6.0651 0 0 0 4.9807 4.1818a5.9847 5.9847 0 0 0-3.9977 2.9 6.0462 6.0462 0 0 0 .7427 7.0966 5.98 5.98 0 0 0 .511 4.9107 6.051 6.051 0 0 0 6.5146 2.9001A5.9847 5.9847 0 0 0 13.2599 24a6.0557 6.0557 0 0 0 5.7718-4.2058 5.9894 5.9894 0 0 0 3.9977-2.9001 6.0557 6.0557 0 0 0-.7475-7.0729zm-9.022 12.6081a4.4755 4.4755 0 0 1-2.8764-1.0408l.1419-.0804 4.7783-2.7582a.7948.7948 0 0 0 .3927-.6813v-6.7369l2.02 1.1686a.071.071 0 0 1 .038.052v5.5826a4.504 4.504 0 0 1-4.4945 4.4944zm-9.6607-4.1254a4.4708 4.4708 0 0 1-.5346-3.0137l.142.0852 4.783 2.7582a.7712.7712 0 0 0 .7806 0l5.8428-3.3685v2.3324a.0804.0804 0 0 1-.0332.0615L9.74 19.9502a4.4992 4.4992 0 0 1-6.1408-1.6464zM2.3408 7.8956a4.485 4.485 0 0 1 2.3655-1.9728V11.6a.7664.7664 0 0 0 .3879.6765l5.8144 3.3543-2.0201 1.1685a.0757.0757 0 0 1-.071 0l-4.8303-2.7865A4.504 4.504 0 0 1 2.3408 7.872zm16.5963 3.8558L13.1038 8.364l2.0201-1.1685a.0757.0757 0 0 1 .071 0l4.8303 2.7913a4.4944 4.4944 0 0 1-.6765 8.1042v-5.6772a.79.79 0 0 0-.407-.667zm2.0107-3.0231l-.142-.0852-4.7735-2.7818a.7759.7759 0 0 0-.7854 0L9.409 9.2297V6.8974a.0662.0662 0 0 1 .0284-.0615l4.8303-2.7866a4.4992 4.4992 0 0 1 6.6802 4.66zM8.3065 12.863l-2.02-1.1638a.0804.0804 0 0 1-.038-.0567V6.0742a4.4992 4.4992 0 0 1 7.3757-3.4537l-.142.0805L8.704 5.459a.7948.7948 0 0 0-.3927.6813zm1.0976-2.3654l2.602-1.4998 2.6069 1.4998v2.9994l-2.5974 1.4997-2.6067-1.4997Z"/></svg>''',
    },
    'perplexity': {
        'name': 'Perplexity',
        'url': 'https://www.perplexity.ai/search/new?q={url}',
        'icon': '''<svg viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="M12 0L8 4h3v6.5L5.5 5 4 6.5 9.5 12H4v3h5.5L4 20.5 5.5 22l5.5-5.5V23h2v-6.5l5.5 5.5 1.5-1.5-5.5-5.5H20v-3h-5.5L20 6.5 18.5 5 13 10.5V4h3l-4-4z"/></svg>''',
    },
    'claude': {
        'name': 'Claude',
        'url': 'https://claude.ai/new?q={url}',
        'icon': '''<svg viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="M4.709 15.955l4.72-2.647.08-.23-.08-.128H2.91l-.08.128.079.23zm8.204-.063l-1.263-3.576-.165-.126-.165.126-1.263 3.576.063.252h2.73zm3.799-5.283L12.12 8.39l-.12-.031-.12.031-4.592 2.22.008.253 4.584 2.573.12.032.12-.032 4.584-2.573zm.798 5.346l4.72 2.647.08-.23-.08-.128h-6.518l-.08.128.079.23zM12 3.59L6.632 6.47l.012.248L12 9.592l5.356-2.874.012-.248zm9.291 12.238L12.12 20.41l-.12.032-.12-.032-9.171-4.582-.08.23.08.127 9.17 4.932.121.031.12-.031 9.172-4.932.079-.128z"/></svg>''',
    },
    'gemini': {
        'name': 'Gemini',
        'url': 'https://gemini.google.com/app?query={url}',
        'icon': '''<svg viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="M12 24A14.304 14.304 0 0 0 0 12 14.304 14.304 0 0 0 12 0a14.305 14.305 0 0 0 12 12 14.305 14.305 0 0 0-12 12"/></svg>''',
    },
    'grok': {
        'name': 'Grok',
        'url': 'https://x.com/i/grok?text={url}',
        'icon': '''<svg viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>''',
    },
}


def get_config(pelican_settings):
    """Get plugin configuration merged with defaults."""
    config = DEFAULT_CONFIG.copy()
    user_config = pelican_settings.get('AI_ANALYZER_BAR', {})
    config.update(user_config)
    return config


def should_show_bar(article, config):
    """Determine if the AI analyzer bar should be shown for this article."""
    if not config.get('enabled', True):
        return False

    if hasattr(article, 'ai_analyzer_bar') and article.ai_analyzer_bar is False:
        return False

    if hasattr(article, 'metadata'):
        meta_value = article.metadata.get('ai_analyzer_bar', '').lower()
        if meta_value in ('false', 'no', '0', 'disable', 'disabled'):
            return False

    if hasattr(article, 'category'):
        category_name = str(article.category).lower()
        exclude_categories = [c.lower() for c in config.get('exclude_categories', [])]
        if category_name in exclude_categories:
            return False

    if hasattr(article, 'url'):
        exclude_paths = config.get('exclude_paths', [])
        for path in exclude_paths:
            if path in article.url:
                return False

    return True


def generate_bar_html(article, config, siteurl):
    """Generate the HTML for the AI analyzer bar."""
    services = config.get('services', [])
    text = config.get('text', DEFAULT_CONFIG['text'])

    article_url = f"{siteurl}/{article.url}"
    encoded_url = quote_plus(article_url)

    buttons_html = []
    for service_key in services:
        service = AI_SERVICES.get(service_key)
        if not service:
            logger.warning(f"Unknown AI service: {service_key}")
            continue

        service_url = service['url'].format(url=encoded_url)
        button_html = f'''<a href="{service_url}" target="_blank" rel="noopener noreferrer" class="ai-analyzer-btn ai-analyzer-{service_key}" title="Analyze with {service['name']}">
            <span class="ai-analyzer-icon">{service['icon']}</span>
            <span class="ai-analyzer-name">{service['name']}</span>
        </a>'''
        buttons_html.append(button_html)

    if not buttons_html:
        return ''

    html = f'''<div class="ai-analyzer-bar-inner">
    <span class="ai-analyzer-text">{text}</span>
    <div class="ai-analyzer-buttons">
        {''.join(buttons_html)}
    </div>
</div>'''

    return html


def add_ai_analyzer_bar(article_generator, content):
    """Signal handler to add AI analyzer bar to articles."""
    if content._content is None:
        return

    config = get_config(article_generator.settings)

    if not should_show_bar(content, config):
        content.ai_analyzer_bar_html = ''
        content.ai_analyzer_bar_position = None
        return

    siteurl = article_generator.settings.get('SITEURL', '')
    bar_html = generate_bar_html(content, config, siteurl)

    content.ai_analyzer_bar_html = bar_html
    content.ai_analyzer_bar_position = config.get('position', 'after_header')


def register():
    """Register the plugin with Pelican."""
    signals.article_generator_write_article.connect(add_ai_analyzer_bar)
