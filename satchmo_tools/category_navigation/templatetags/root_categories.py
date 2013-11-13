from django import template
from product.models import Category


register = template.Library()

@register.assignment_tag
def root_categories():
    return Category.objects.root_categories()
