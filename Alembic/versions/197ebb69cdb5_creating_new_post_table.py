"""creating new  Post table

Revision ID: 197ebb69cdb5
Revises: 5cf2f988417b
Create Date: 2024-10-22 02:57:14.574309

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '197ebb69cdb5'
down_revision: Union[str, None] = '5cf2f988417b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
     op.create_table('posts', 
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(length=100), nullable=False),
                    sa.Column('content', sa.Text(), nullable=False),
                    sa.Column('published', sa.Boolean(), server_default='True', nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    # sa.Column('ownerID', sa.Integer(), nullable=False),
                    
                    sa.PrimaryKeyConstraint('id'),
                    # sa.ForeignKeyConstraint(['ownerID'], ['users.id'], ondelete='CASCADE')
                    )
    


def downgrade() -> None:
    op.drop_table('posts')  # noqa: E501  # table name can be used as identifier in SQLAlchemy, so it's not a typo.
    pass
