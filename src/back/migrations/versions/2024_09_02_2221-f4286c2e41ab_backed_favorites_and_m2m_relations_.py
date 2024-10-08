"""Backed Favorites and m2m relations between users and ads

Revision ID: f4286c2e41ab
Revises: 3c1110cd6b9a
Create Date: 2024-09-02 22:21:51.368155

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4286c2e41ab'
down_revision: Union[str, None] = '3c1110cd6b9a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorites',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('ad_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['ad_id'], ['ads.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'ad_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favorites')
    # ### end Alembic commands ###
