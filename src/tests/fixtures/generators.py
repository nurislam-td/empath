import random
import string

import pytest
from mimesis import Generic, Locale
from mimesis.providers import BaseProvider


class PasswordProvider(BaseProvider):
    class Meta:  # type: ignore  # noqa: PGH003
        name = "password"

    def secure(self, length: int = 8) -> str:
        categories = [
            string.ascii_uppercase,
            string.ascii_lowercase,
            string.digits,
            "!@#$%^&*",
        ]
        password_chars = [random.choice(cat) for cat in categories]  # noqa: S311

        all_chars = string.ascii_letters + string.digits + "!@#$%^&*"
        remaining = length - len(password_chars)
        password_chars += [random.choice(all_chars) for _ in range(remaining)]  # noqa: S311

        random.shuffle(password_chars)
        return "".join(password_chars)


@pytest.fixture
def generic_generator() -> Generic:
    generic = Generic(Locale.RU)
    generic.add_provider(PasswordProvider)
    return generic
