"""mock work format

Revision ID: 2bd7b266dc3c
Revises: ec98ddc59c92
Create Date: 2025-04-05 08:53:09.119910

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2bd7b266dc3c"
down_revision: Union[str, None] = "ec98ddc59c92"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        sa.text(
            """
            INSERT INTO job.work_format (name)
            VALUES ('remote'), ('onsite'), ('hybrid')
            """
        )
    )


def downgrade() -> None:
    op.execute("DELETE FROM job.work_format WHERE name IN ('remote', 'onsite', 'hybrid')")
