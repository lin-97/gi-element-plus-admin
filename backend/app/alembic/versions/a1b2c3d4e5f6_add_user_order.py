"""add user order column

Revision ID: a1b2c3d4e5f6
Revises: 442b5b3fe948
Create Date: 2026-05-28 16:40:00.000000
"""
import sqlalchemy as sa
from alembic import op

revision = "a1b2c3d4e5f6"
down_revision = "442b5b3fe948"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "sys_user",
        sa.Column("order", sa.Integer(), nullable=False, server_default="0"),
    )
    op.alter_column("sys_user", "order", server_default=None)


def downgrade() -> None:
    op.drop_column("sys_user", "order")
