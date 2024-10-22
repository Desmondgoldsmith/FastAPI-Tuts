"""creating Post table

Revision ID: 5cf2f988417b
Revises: 
Create Date: 2024-10-22 02:09:02.067776

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5cf2f988417b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('Posts', 
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(length=100), nullable=False),
                    sa.Column('content', sa.Text(), nullable=False),
                    sa.Column('published', sa.Boolean(), server_default='True', nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    # sa.Column('ownerID', sa.Integer(), nullable=False),
                    
                    sa.PrimaryKeyConstraint('id'),
                    # sa.ForeignKeyConstraint(['ownerID'], ['users.id'], ondelete='CASCADE')
                    )
    pass


def downgrade() -> None:
    op.drop_table('Posts')  # noqa: E501  # table name can be used as identifier in SQLAlchemy, so it's not a typo.
    pass
