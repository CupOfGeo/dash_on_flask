"""empty message

Revision ID: c4e07372a7e5
Revises: 947dc1d19f9e
Create Date: 2021-11-09 15:45:58.019862

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4e07372a7e5'
down_revision = '947dc1d19f9e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('gpt_model', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.drop_column('gpt_model', 'owner')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('gpt_model', sa.Column('owner', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('gpt_model', 'owner_id')
    # ### end Alembic commands ###