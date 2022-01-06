

class EagerLoadingMixin:
    @classmethod
    def setup_eager_loading(cls, queryset):
        """
        This function allow dynamic addition of the related objects to
        the provided query.
        @parameter param1: queryset
        """
        if hasattr(cls, "select_related_fields"):
            queryset = queryset.select_related(*cls.select_related_fields)
        if hasattr(cls, "prefetch_related_fields"):
            queryset = queryset.prefetch_related(*cls.prefetch_related_fields)
        return queryset
