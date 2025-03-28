"""init db

Revision ID: 372360d9cf8a
Revises:
Create Date: 2025-03-08 21:32:18.251673

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "372360d9cf8a"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("CREATE SCHEMA IF NOT EXISTS auth")
    op.execute("CREATE SCHEMA IF NOT EXISTS article")
    op.execute("DROP TYPE IF EXISTS gender")
    op.create_table(
        "tag",
        sa.Column("name", sa.String(length=50), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tag")),
        schema="article",
    )
    op.create_index(
        op.f("ix_article_tag_id"), "tag", ["id"], unique=False, schema="article"
    )
    op.create_table(
        "user",
        sa.Column("password", sa.LargeBinary(), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("nickname", sa.String(length=20), nullable=True),
        sa.Column(
            "gender", sa.Enum("male", "female", "other", name="gender"), nullable=True
        ),
        sa.Column("name", sa.String(length=255), nullable=True),
        sa.Column("lastname", sa.String(length=255), nullable=True),
        sa.Column("patronymic", sa.String(length=255), nullable=True),
        sa.Column("date_birth", sa.Date(), nullable=True),
        sa.Column("image", sa.String(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user")),
        schema="auth",
    )
    op.create_index(
        op.f("ix_auth_user_email"), "user", ["email"], unique=True, schema="auth"
    )
    op.create_index(
        op.f("ix_auth_user_id"), "user", ["id"], unique=False, schema="auth"
    )
    op.create_table(
        "article",
        sa.Column("title", sa.String(length=50), nullable=True),
        sa.Column("text", sa.Text(), nullable=True),
        sa.Column("is_visible", sa.Boolean(), nullable=True),
        sa.Column("author_id", sa.Uuid(), nullable=True),
        sa.Column("views_cnt", sa.BigInteger(), nullable=True),
        sa.Column("likes_cnt", sa.BigInteger(), nullable=True),
        sa.Column("dislikes_cnt", sa.BigInteger(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["auth.user.id"],
            name=op.f("fk_article_author_id_user"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_article")),
        schema="article",
    )
    op.create_index(
        op.f("ix_article_article_id"), "article", ["id"], unique=False, schema="article"
    )
    op.create_table(
        "refresh_token",
        sa.Column("user_id", sa.Uuid(), nullable=True),
        sa.Column("refresh_token", sa.String(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["auth.user.id"],
            name=op.f("fk_refresh_token_user_id_user"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_refresh_token")),
        schema="auth",
    )
    op.create_index(
        op.f("ix_auth_refresh_token_id"),
        "refresh_token",
        ["id"],
        unique=False,
        schema="auth",
    )
    op.create_table(
        "article_img",
        sa.Column("url", sa.Text(), nullable=True),
        sa.Column("article_id", sa.Uuid(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["article_id"],
            ["article.article.id"],
            name=op.f("fk_article_img_article_id_article"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_article_img")),
        schema="article",
    )
    op.create_index(
        op.f("ix_article_article_img_id"),
        "article_img",
        ["id"],
        unique=False,
        schema="article",
    )
    op.create_table(
        "rel_article_tag",
        sa.Column("article_id", sa.Uuid(), nullable=False),
        sa.Column("tag_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["article_id"],
            ["article.article.id"],
            name=op.f("fk_rel_article_tag_article_id_article"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["tag_id"],
            ["article.tag.id"],
            name=op.f("fk_rel_article_tag_tag_id_tag"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "article_id", "tag_id", name=op.f("pk_rel_article_tag")
        ),
        schema="article",
    )
    op.create_table(
        "sub_article",
        sa.Column("article_id", sa.Uuid(), nullable=True),
        sa.Column("title", sa.String(length=50), nullable=True),
        sa.Column("text", sa.Text(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["article_id"],
            ["article.article.id"],
            name=op.f("fk_sub_article_article_id_article"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_sub_article")),
        schema="article",
    )
    op.create_index(
        op.f("ix_article_sub_article_id"),
        "sub_article",
        ["id"],
        unique=False,
        schema="article",
    )
    op.create_table(
        "sub_article_img",
        sa.Column("url", sa.Text(), nullable=True),
        sa.Column("sub_article_id", sa.Uuid(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["sub_article_id"],
            ["article.sub_article.id"],
            name=op.f("fk_sub_article_img_sub_article_id_sub_article"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_sub_article_img")),
        schema="article",
    )
    op.create_index(
        op.f("ix_article_sub_article_img_id"),
        "sub_article_img",
        ["id"],
        unique=False,
        schema="article",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_article_sub_article_img_id"),
        table_name="sub_article_img",
        schema="article",
    )
    op.drop_table("sub_article_img", schema="article")
    op.drop_index(
        op.f("ix_article_sub_article_id"), table_name="sub_article", schema="article"
    )
    op.drop_table("sub_article", schema="article")
    op.drop_table("rel_article_tag", schema="article")
    op.drop_index(
        op.f("ix_article_article_img_id"), table_name="article_img", schema="article"
    )
    op.drop_table("article_img", schema="article")
    op.drop_index(
        op.f("ix_auth_refresh_token_id"), table_name="refresh_token", schema="auth"
    )
    op.drop_table("refresh_token", schema="auth")
    op.drop_index(op.f("ix_article_article_id"), table_name="article", schema="article")
    op.drop_table("article", schema="article")
    op.drop_index(op.f("ix_auth_user_id"), table_name="user", schema="auth")
    op.drop_index(op.f("ix_auth_user_email"), table_name="user", schema="auth")
    op.drop_table("user", schema="auth")
    op.drop_index(op.f("ix_article_tag_id"), table_name="tag", schema="article")
    op.drop_table("tag", schema="article")
    op.execute("DROP SCHEMA IF EXISTS article")
    op.execute("DROP SCHEMA IF EXISTS auth")
    op.execute("DROP TYPE IF EXISTS gender")
    # ### end Alembic commands ###
