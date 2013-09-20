from django.template import Library

from product.models import Category, Product


register = Library()


@register.inclusion_tag('category_navigation/_category_navigation.html', takes_context=True)
def category_navigation(context):
    category = None
    if 'category' in context:
        category = context['category']
    return {
        'nodes': Category.objects.root_categories(),
        'root': True,
        'category': category
    }

@register.assignment_tag
def category_is_active(node, category):
    if not category:
        return False
    active = category.id == node.id
    if not active:
        ids = [c.id for c in category.parents()]
        active = node.id in ids
    return active
