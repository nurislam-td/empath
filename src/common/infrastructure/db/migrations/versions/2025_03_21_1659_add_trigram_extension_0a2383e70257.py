"""add trigram extension

Revision ID: 0a2383e70257
Revises: a0f1f9c8a3ef
Create Date: 2025-03-21 16:59:51.320285

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0a2383e70257"
down_revision: Union[str, None] = "a0f1f9c8a3ef"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")


def downgrade() -> None:
    op.execute("DROP EXTENSION IF EXISTS pg_trgm;")
