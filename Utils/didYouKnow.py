import random
from main.models import EnvironmentalTipModel

def didYouKnowMessage():
    tip = EnvironmentalTipModel.objects.order_by('?').first()

    data = {
        'category':tip.category,
        'content':tip.content
    }

    if data:
        return data

    return none
