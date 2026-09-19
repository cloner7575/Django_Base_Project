---
name: django-rest-framework
description: Django REST Framework patterns for serializers, ViewSets, permissions, pagination, and queryset optimization. Use when building APIs, serializers, viewsets, or DRF permissions. Triggers on DRF, REST API, serializer, ViewSet, APIView.
---

# Django REST Framework

DRF is not installed yet. When adding it:

```bash
.venv/bin/pip install djangorestframework
```

Add `"rest_framework"` to `INSTALLED_APPS` and include API urls from `core/urls.py`. Do not add DRF unless the task needs an API.

## Layout

```
<app>/
├── models.py
├── serializers.py
├── views.py          # or viewsets.py
├── permissions.py
└── urls.py
```

## Serializers

- One serializer per use case when inputs differ (create vs list vs nested write)
- Validate in the serializer (`validate_<field>`, `validate`), not in the view
- Use `SerializerMethodField` sparingly — it often causes N+1
- Prefer `PrimaryKeyRelatedField` / nested read serializers over fat write nests
- Never pass `request.data` straight into a model constructor

```python
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "title", "author", "created_at")
        read_only_fields = ("id", "author", "created_at")

    def create(self, validated_data: dict) -> Post:
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)
```

## Views and ViewSets

- `ModelViewSet` when CRUD maps cleanly; `APIView` / `GenericAPIView` when it does not
- **Always** override `get_queryset()` and apply `select_related` / `prefetch_related`
- Scope queryset to the user; do not rely on the serializer to hide other users' rows
- Use `perform_create` to stamp `request.user`

```python
class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet[Post]:
        return (
            Post.objects.filter(author=self.request.user)
            .select_related("author")
            .order_by("-created_at")
        )
```

## Permissions and Auth

- Default to authenticated write, explicit allow-list for public read
- Custom permissions implement `has_permission` and `has_object_permission`
- Pair with `django-auth` for JWT / session choices

```python
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}
```

## Pagination, Errors, Versioning

- Always paginate list endpoints
- Return DRF `ValidationError` / `APIException`; do not leak stack traces
- Version via URL (`api/v1/`) unless the project already chose another scheme

## Anti-Patterns

- `queryset = Model.objects.all()` on a ViewSet that then filters in `list()`
- Serializers that walk relations without prefetch
- Business logic in `create()` views instead of serializer/model
- `permission_classes = [AllowAny]` on write endpoints

## Integration

- `django-models`, `django-auth`, `django-caching`, `pytest-django-patterns`
