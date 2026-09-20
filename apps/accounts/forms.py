from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    """Login form with autofocus and password-manager friendly attributes."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"autofocus": True, "autocomplete": "username"}
        )
        self.fields["password"].widget.attrs.update(
            {"autocomplete": "current-password"}
        )
