"""Initial migration

Revision ID: 3c1110cd6b9a
Revises: 
Create Date: 2024-09-02 22:12:06.841859

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c1110cd6b9a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category_name', sa.String(length=40), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('signup_timestamp', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('last_activity', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('ads',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('by_user', sa.Integer(), nullable=False),
    sa.Column('category', sa.Integer(), nullable=False),
    sa.Column('item_give', sa.String(length=40), nullable=False),
    sa.Column('item_get', sa.String(length=40), nullable=False),
    sa.Column('description', sa.String(length=300), nullable=False),
    sa.Column('location', sa.String(length=80), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.ForeignKeyConstraint(['by_user'], ['users.id'], ),
    sa.ForeignKeyConstraint(['category'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ads')
    op.drop_table('users')
    op.drop_table('categories')
    # ### end Alembic commands ###
