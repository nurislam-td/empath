"""change work format

Revision ID: 7840a916e484
Revises: 90c6732549c2
Create Date: 2025-04-05 08:25:53.158353

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "7840a916e484"
down_revision: Union[str, None] = "90c6732549c2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "work_format",
        sa.Column(
            "name",
            postgresql.ENUM("REMOTE", "ONSITE", "HYBRID", name="workformatenum", create_type=False),
            nullable=False,
        ),  # type: ignore  # noqa: PGH003
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_work_format")),
        schema="job",
    )
    op.create_index(op.f("ix_job_work_format_id"), "work_format", ["id"], unique=False, schema="job")
    op.create_table(
        "rel_vacancy_work_format",
        sa.Column("work_format_id", sa.Uuid(), nullable=False),
        sa.Column("vacancy_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(
            ["vacancy_id"],
            ["job.vacancy.id"],
            name=op.f("fk_rel_vacancy_work_format_vacancy_id_vacancy"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["work_format_id"],
            ["job.work_format.id"],
            name=op.f("fk_rel_vacancy_work_format_work_format_id_work_format"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("work_format_id", "vacancy_id", name=op.f("pk_rel_vacancy_work_format")),
        schema="job",
    )
    op.drop_column("vacancy", "work_format", schema="job")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "vacancy",
        sa.Column(
            "work_format",
            postgresql.ENUM("REMOTE", "ONSITE", "HYBRID", name="workformatenum"),
            autoincrement=False,
            nullable=False,
        ),
        schema="job",
    )
    op.drop_table("rel_vacancy_work_format", schema="job")
    op.drop_index(op.f("ix_job_work_format_id"), table_name="work_format", schema="job")
    op.drop_table("work_format", schema="job")
    # ### end Alembic commands ###
