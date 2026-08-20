# logic

import secrets
import string

LOWERCASE_CHARS = string.ascii_lowercase
UPPERCASE_CHARS = string.ascii_uppercase
NUMBER_CHARS = string.digits
SYMBOL_CHARS = "~`!@#$%^&*()_-+={[}]|\\:;'<,>.?/"


def generate_password(
    length: int,
    include_lowercase: bool,
    include_uppercase: bool,
    include_numbers: bool,
    include_symbols: bool,
) -> str | None:
    """Generate a cryptographically secure random password.

    Every selected character class is guaranteed to appear at least
    once (as long as `length` allows it), so a long password can't
    randomly end up missing a class the user explicitly asked for.
    """
    selected_pools = [
        pool
        for pool, include in (
            (LOWERCASE_CHARS, include_lowercase),
            (UPPERCASE_CHARS, include_uppercase),
            (NUMBER_CHARS, include_numbers),
            (SYMBOL_CHARS, include_symbols),
        )
        if include
    ]

    if length <= 0 or not selected_pools:
        return None

    allowed_chars = "".join(selected_pools)

    # Guarantee at least one character from each selected pool
    # (capped at `length` in case length < number of selected pools).
    password_chars = [
        secrets.choice(pool) for pool in selected_pools[:length]
    ]

    remaining = length - len(password_chars)
    password_chars.extend(
        secrets.choice(allowed_chars) for _ in range(remaining)
    )

    # Shuffle so the guaranteed characters aren't predictably placed
    # at the start of the password.
    secrets.SystemRandom().shuffle(password_chars)

    return "".join(password_chars)