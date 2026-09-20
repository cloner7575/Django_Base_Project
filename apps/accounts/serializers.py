from rest_framework import serializers

from apps.accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    """Profile representation of the authenticated user."""

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "date_joined",
        )
        read_only_fields = ("id", "username", "date_joined")

    def validate_email(self, value: str) -> str:
        normalized = value.strip().lower()
        if not normalized:
            return ""

        taken = User.objects.filter(email__iexact=normalized)
        if self.instance is not None:
            taken = taken.exclude(pk=self.instance.pk)
        if taken.exists():
            raise serializers.ValidationError("This email is already in use.")
        return normalized
