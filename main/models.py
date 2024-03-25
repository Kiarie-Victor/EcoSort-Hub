from django.db import models

# Create your models here.

class EnvironmentalTipModel(models.Model):
    category = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category
    
class WasteCategory(models.Model):
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

    category = models.CharField(max_length = 100, choices = CATEGORY_CHOICES)
    description = models.TextField()

    def __str__(self):
        return self.category
    