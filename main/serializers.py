from rest_framework import serializers
from main.models import WasteCategory

# Serializer for WasteCategory model.


class WasteCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteCategory
        fields = ('category', 'description',)

    # Custom validation for the category field.
    def validate_category(self, category):
        # Get the defined waste categories from the model choices.
        defined_categories = [choice[0]
                              for choice in WasteCategory.CATEGORY_CHOICES]

        # Check if the provided category is one of the defined categories.
        if category not in defined_categories:
            raise serializers.ValidationError('Invalid waste category name.')

        return category
