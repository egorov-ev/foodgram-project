from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from recipes.models import Ingredient

from .models import Favorite, Subscription
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          PurchaseSerializer, SubscriptionSerializer)


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class IngredientViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^title',)


class SubscriptionViewSet(CreateListDestroyViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'author'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, )


class FavoriteViewSet(CreateListDestroyViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'recipe'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, )


class PurchaseViewSet(CreateListDestroyViewSet):
    serializer_class = PurchaseSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'recipe'

    def get_queryset(self):
        return self.request.user.purchases.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, )
