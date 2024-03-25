from rest_framework import serializers
from main.models import WasteCategory

class WasteCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteCategory
        fields = ('category', 'description',)

    def validate_category(self, category):
        defined_categories = [choice[0] for choice in WasteCategory.CATEGORY_CHOICES]

        if category not in defined_categories:
            raise serializers.ValidationError('Invalid waste category name.')

        return category