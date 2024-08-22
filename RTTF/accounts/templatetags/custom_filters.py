from django import template
from datetime import timedelta

register = template.Library()

@register.filter
def sum_times(quests):
    total_duration = timedelta()
    for _, duration in quests:
        if duration:
            total_duration += duration
    return total_duration
