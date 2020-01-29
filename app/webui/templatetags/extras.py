from django import template

register = template.Library()


@register.inclusion_tag("webui/pagination_nav.html", takes_context=True)
def pagination_nav(context):
    """
    Inclusion tag for rendering pagination_nav panel
    """
    return context


@register.inclusion_tag("webui/statistics.html")
def statistics(stats: dict) -> dict:
    """
    Inclusion tag for rendering statistics block
    """
    return stats
