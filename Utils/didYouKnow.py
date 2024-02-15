import random
from main.models import DidYouKnow

def didYouKnowMessage():
    random_fact = DidYoKnow.objects.order_by('?').first()
    if random_fact:
        return random_fact.message
    
    return None
