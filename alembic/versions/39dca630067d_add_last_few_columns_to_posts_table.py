"""add last few columns to  posts table

Revision ID: 39dca630067d
Revises: 7257387e1c84
Create Date: 2024-05-08 14:35:37.602381

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '39dca630067d'
down_revision: Union[str, None] = '7257387e1c84'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column(
        "published",sa.Boolean(), nullable=False, server_default="TRUE"
    ),)
    op.add_column("posts",sa.Column(
        "Created_at", sa.TIMESTAMP(timezone=True),nullable=False, server_default=sa.text("NOW()")
    ),)
    pass


def downgrade() -> None:
    op.drop_column("posts",'published')
    op.drop_column("posts","Created_at")
    pass
