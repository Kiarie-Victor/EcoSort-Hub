import random
from main.models import EnvironmentalTipModel


def didYouKnowMessage():
    # Retrieve a random environmental tip from the database
    tip = EnvironmentalTipModel.objects.order_by('?').first()

    # Create a dictionary containing the category and content of the tip
    data = {
        'category': tip.category,
        'content': tip.content
    }

    # Check if a tip was found
    if data:
        # Return the tip data
        return data
    else:
        # Return None if no tip was found
        return None
