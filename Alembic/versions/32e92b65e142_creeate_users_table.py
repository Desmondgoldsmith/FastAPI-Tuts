"""creeate users table

Revision ID: 32e92b65e142
Revises: 197ebb69cdb5
Create Date: 2024-10-22 03:00:03.913289

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '32e92b65e142'
down_revision: Union[str, None] = '197ebb69cdb5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', 
                           sa.Column('id', sa.Integer(), nullable=False),
                           sa.Column('username', sa.String(length=50), nullable=False),
                           sa.Column('email', sa.String(length=100), nullable=False),
                           sa.Column('password', sa.String(length=128), nullable=False),
                           sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                           
                           sa.PrimaryKeyConstraint('id'),
                           sa.UniqueConstraint('email')  # noqa: E501  # unique constraint can be used as identifier in SQLAlchemy, so it's not a typo.
                   )
    pass


def downgrade() -> None:
    op.drop_table('users')  # noqa: E501  # table name can be used as identifier in SQLAlchemy, so it's not a typo.  # noqa: E
    pass
