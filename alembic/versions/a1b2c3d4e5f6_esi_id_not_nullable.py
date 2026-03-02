"""esi_id not nullable

Revision ID: a1b2c3d4e5f6
Revises: 0e757782815e
Create Date: 2026-03-02 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = '0e757782815e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('esi_users', 'esi_id', nullable=False)


def downgrade() -> None:
    op.alter_column('esi_users', 'esi_id', nullable=True)
