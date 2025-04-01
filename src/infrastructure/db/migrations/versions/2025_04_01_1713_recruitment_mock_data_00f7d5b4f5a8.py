"""Recruitment mock data

Revision ID: 00f7d5b4f5a8
Revises: c76ad69b7bcf
Create Date: 2025-04-01 17:13:13.315836

"""

import uuid
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "00f7d5b4f5a8"
down_revision: Union[str, None] = "c76ad69b7bcf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    employment_type_full_time = uuid.uuid4()
    employment_type_part_time = uuid.uuid4()

    op.execute(
        sa.text(
            """
            INSERT INTO job.employment_type (id, name)
            VALUES (:full_time_id, 'Full-time'),
                   (:part_time_id, 'Part-time')
            """
        ).bindparams(full_time_id=(employment_type_full_time), part_time_id=(employment_type_part_time)),
    )

    # Вставляем данные в таблицу work_schedule
    ws_5_2 = uuid.uuid4()
    ws_free = uuid.uuid4()  # Свободный
    ws_weekends = uuid.uuid4()  # По выходным
    ws_other = uuid.uuid4()  # Другое
    ws_6_1 = uuid.uuid4()
    ws_4_3 = uuid.uuid4()
    ws_3_2 = uuid.uuid4()
    ws_2_2 = uuid.uuid4()
    ws_2_1 = uuid.uuid4()
    ws_1_3 = uuid.uuid4()
    ws_1_2 = uuid.uuid4()
    ws_4_4 = uuid.uuid4()

    op.execute(
        sa.text(
            """
            INSERT INTO job.work_schedule (id, name)
            VALUES
                (:ws_5_2, '5/2'),
                (:ws_free, 'Free'),
                (:ws_weekends, 'On weekends'),
                (:ws_other, 'Other'),
                (:ws_6_1, '6/1'),
                (:ws_4_3, '4/3'),
                (:ws_3_2, '3/2'),
                (:ws_2_2, '2/2'),
                (:ws_2_1, '2/1'),
                (:ws_1_3, '1/3'),
                (:ws_1_2, '1/2'),
                (:ws_4_4, '4/4')
            """
        ).bindparams(
            ws_5_2=(ws_5_2),
            ws_free=(ws_free),
            ws_weekends=(ws_weekends),
            ws_other=(ws_other),
            ws_6_1=(ws_6_1),
            ws_4_3=(ws_4_3),
            ws_3_2=(ws_3_2),
            ws_2_2=(ws_2_2),
            ws_2_1=(ws_2_1),
            ws_1_3=(ws_1_3),
            ws_1_2=(ws_1_2),
            ws_4_4=(ws_4_4),
        ),
    )


def downgrade() -> None:
    op.execute("DELETE FROM job.work_schedule")
    op.execute("DELETE FROM job.employment_type")
