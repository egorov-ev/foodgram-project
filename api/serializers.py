from rest_framework import serializers

from recipes.models import Ingredient

from .models import Favorite, Purchase, Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('author',)

    def validate(self, attrs):
        if (self.context['request'].user == attrs
                and self.context['request'].method == 'POST'):
            raise serializers.ValidationError('Невозможно подписаться на себя')
        return attrs


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('recipe',)


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ('recipe',)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('title', 'unit_measure',)
