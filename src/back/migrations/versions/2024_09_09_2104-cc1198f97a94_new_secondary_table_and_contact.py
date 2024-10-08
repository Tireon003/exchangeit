"""new secondary table and-contact

Revision ID: cc1198f97a94
Revises: 729a5ff50258
Create Date: 2024-09-09 21:04:54.823739

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc1198f97a94'
down_revision: Union[str, None] = '729a5ff50258'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ads_contact',
    sa.Column('ad_id', sa.Integer(), nullable=False),
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['ad_id'], ['ads.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['contact_id'], ['contacts.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('ad_id', 'contact_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ads_contact')
    # ### end Alembic commands ###
