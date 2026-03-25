"""add created_at

Revision ID: 9840e83f5778
Revises:
Create Date: 2026-03-25 15:11:46.794646

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '9840e83f5778'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'transactions',
        sa.Column(
            'created_at',
            sa.DateTime(),
            server_default=sa.func.now(),
            nullable=False
        )
    )


def downgrade() -> None:
    op.drop_column('transactions', 'created_at')
