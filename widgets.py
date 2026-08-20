from textual.widgets import Checkbox, Input


class PasswordCheckbox(Checkbox):
    """Checkbox with custom retro-style square glyphs instead of the
    default Textual checkbox symbol."""

    def render(self):
        symbol = "■" if self.value else "□"
        return f"{symbol}  {self.label}"


class PasswordInput(Input):
    """Input pre-configured to mask its content as a password field."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("password", True)
        super().__init__(*args, **kwargs)