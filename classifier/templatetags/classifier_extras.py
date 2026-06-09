from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiply the value by the argument."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def sum_weight(farmer_data):
    """Calculate total weight from farmer data."""
    return sum(float(record['weight'] or 0) for record in farmer_data)

@register.filter
def sum_value(farmer_data):
    """Calculate total value from farmer data."""
    return sum(float(record['weight'] or 0) * float(record['result__price'] or 0) for record in farmer_data) 