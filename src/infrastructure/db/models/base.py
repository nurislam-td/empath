import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, registry

convention = {
    "ix": "ix_%(column_0_label)s",  # INDEX
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",  # UNIQUE
    "ck": "ck_%(table_name)s_%(constraint_name)s",  # CHECK
    "fk": "fk_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s",  # FOREIGN KEY
    "pk": "pk_%(table_name)s",  # PRIMARY KEY
}

mapper_registry = registry(metadata=sa.MetaData(naming_convention=convention))


class BaseModel(DeclarativeBase):
    registry = mapper_registry
    metadata = mapper_registry.metadata

    __abstract__ = True
    id = sa.Column(  # type: ignore
        sa.types.Uuid,
        primary_key=True,
        server_default=sa.text("gen_random_uuid()"),
        index=True,
    )


class TimedBaseModel(BaseModel):
    """An abstract base model that adds created_at and updated_at timestamp fields to the model."""

    __abstract__ = True

    created_at = sa.Column(sa.String(), nullable=False, server_default=sa.func.now())
    updated_at = sa.Column(
        sa.types.DateTime,
        nullable=False,
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
    )
