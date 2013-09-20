from django.template import Library

from product.models import Category, Product


register = Library()


@register.inclusion_tag('satchmo_tools/category_navigation.html', takes_context=True)
def category_navigation(context):
    return {
        'nodes': Category.objects.root_categories()
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

@register.assignment_tag
def random_featured(n):
    return Product.objects.filter(active=True, featured=True).order_by('?')[:n]
