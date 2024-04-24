from django.db import models

# EnvironmentalTipModel represents environmental tips provided in the application.


class EnvironmentalTipModel(models.Model):  
    category = models.CharField(max_length=30)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category

# WasteCategory represents different categories of waste.


class WasteCategory(models.Model):
    # Define choices for waste categories.
    PLASTIC = 'Plastic'
    GLASS = 'Glass'
    PAPER = 'Paper'
    METAL = 'Metal'
    ORGANIC = 'Organic'
    E_WASTE = 'Electronic Waste'
    HAZARDOUS = 'Hazardous Waste'
    TEXTILES = 'Textiles'
    RUBBER = 'Rubber'
    WOOD = 'Wood'

    # Define choices as tuples.
    CATEGORY_CHOICES = [
        (PLASTIC, 'Plastic'),
        (GLASS, 'Glass'),
        (PAPER, 'Paper'),
        (METAL, 'Metal'),
        (ORGANIC, 'Organic'),
        (E_WASTE, 'Electronic Waste'),
        (HAZARDOUS, 'Hazardous Waste'),
        (TEXTILES, 'Textiles'),
        (RUBBER, 'Rubber'),
        (WOOD, 'Wood')
    ]

    # Define the category field with choices.
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    description = models.TextField()

    def __str__(self):
        return self.category