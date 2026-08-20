from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal
from textual.widgets import Button, Header, Input, Label

from password_generator import generate_password
from widgets import PasswordCheckbox, PasswordInput

try:
    import pyperclip

    HAS_PYPERCLIP = True
except ImportError:
    HAS_PYPERCLIP = False


class PasswordGeneratorApp(App):
    CSS_PATH = "styles.tcss"

    BINDINGS = [
        Binding("ctrl+g", "generate", "Generate"),
        Binding("ctrl+y", "copy", "Copy"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()

        with Container():
            yield Label("PASSWORD GENERATOR", id="title")

            yield Label("LÄNGE:", id="length-label")

            yield Input(
                value="12",
                id="length",
                restrict=r"[0-9]*",
            )

            yield PasswordCheckbox("Kleinbuchstaben", value=True, id="lowercase")
            yield PasswordCheckbox("Großbuchstaben", value=True, id="uppercase")
            yield PasswordCheckbox("Zahlen", value=True, id="numbers")
            yield PasswordCheckbox("Sonderzeichen", value=True, id="symbols")

            yield Button("GENERATE PASSWORD", id="btnRefresh")

            with Horizontal(id="password-box"):
                yield PasswordInput(placeholder="PASSWORD", id="sPassword")
                yield Button("COPY PASSWORD", id="btnCopy")

    def on_mount(self) -> None:
        # Cache widget references once instead of running a new DOM
        # query every time a password is generated or copied.
        self.length_input = self.query_one("#length", Input)
        self.lowercase_checkbox = self.query_one("#lowercase", PasswordCheckbox)
        self.uppercase_checkbox = self.query_one("#uppercase", PasswordCheckbox)
        self.numbers_checkbox = self.query_one("#numbers", PasswordCheckbox)
        self.symbols_checkbox = self.query_one("#symbols", PasswordCheckbox)
        self.password_output = self.query_one("#sPassword", PasswordInput)

        self.length_input.focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btnRefresh":
            self.generate_password()
        elif event.button.id == "btnCopy":
            self.copy_password()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "length":
            self.generate_password()

    def action_generate(self) -> None:
        self.generate_password()

    def action_copy(self) -> None:
        self.copy_password()

    def _warn(self, message: str) -> None:
        self.notify(message, severity="warning")

    def generate_password(self) -> None:
        raw_length = self.length_input.value.strip()

        if not raw_length or not raw_length.isdigit():
            self._warn("Please enter a valid password length.")
            return

        length = int(raw_length)

        if length <= 0:
            self._warn("Password length must be at least 1.")
            return

        include_lowercase = self.lowercase_checkbox.value
        include_uppercase = self.uppercase_checkbox.value
        include_numbers = self.numbers_checkbox.value
        include_symbols = self.symbols_checkbox.value

        if not any(
            (include_lowercase, include_uppercase, include_numbers, include_symbols)
        ):
            self._warn("At least one character set must be selected.")
            return

        password = generate_password(
            length,
            include_lowercase,
            include_uppercase,
            include_numbers,
            include_symbols,
        )

        if password:
            self.password_output.value = password

    def copy_password(self) -> None:
        password = self.password_output.value

        if not password:
            self._warn("No password available to copy.")
            return

        if not HAS_PYPERCLIP:
            self.notify("pyperclip is not installed.", severity="error")
            return

        try:
            pyperclip.copy(password)
            self.notify("Password copied to clipboard.", title="Success")
        except Exception:
            self.notify(
                "Failed to copy password to clipboard.",
                severity="error",
            )


if __name__ == "__main__":
    PasswordGeneratorApp().run()