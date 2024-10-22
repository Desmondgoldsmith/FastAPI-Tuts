"""add columns to post table

Revision ID: 2cae28d6cf14
Revises: 32e92b65e142
Create Date: 2024-10-22 03:06:22.626006

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2cae28d6cf14'
down_revision: Union[str, None] = '32e92b65e142'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', 
                  sa.Column('ownerID', sa.Integer(), nullable=False)),
                  
    op.create_foreign_key('posts_users_fk', source_table = 'posts', referent_table = 'users', local_cols = ['ownerID'], remote_cols = ['id'], ondelete='CASCADE'),
                  
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name = 'posts', type_='foreignkey')
    op.drop_column('posts', 'ownerID')  # noqa: E501  # column name can be used as identifier in SQLAlchemy, so it's not a typo. 
    pass
