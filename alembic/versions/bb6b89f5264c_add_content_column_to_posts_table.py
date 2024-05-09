"""add content  column to posts table

Revision ID: bb6b89f5264c
Revises: 59089f1cbb9c
Create Date: 2024-05-08 14:07:44.100947

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb6b89f5264c'
down_revision: Union[str, None] = '59089f1cbb9c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
