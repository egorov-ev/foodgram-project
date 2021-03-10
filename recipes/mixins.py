from django.shortcuts import redirect, reverse


class IsAuthorMixin:

    def dispatch(self, request, *args, **kwargs):
        """
        Проверяем, что только автор рецепта может его изменить.
        """
        obj = self.get_object()
        if obj.author != self.request.user:
            return redirect(reverse(
                'slug_recipe_view',
                kwargs={'slug': obj.slug, 'recipe_id': obj.id})
            )
        response = super().dispatch(request, *args, **kwargs)
        return response
