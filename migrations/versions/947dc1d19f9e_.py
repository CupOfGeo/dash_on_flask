"""empty message

Revision ID: 947dc1d19f9e
Revises: b695c2235fac
Create Date: 2021-11-09 11:55:12.746065

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '947dc1d19f9e'
down_revision = 'b695c2235fac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('gpt_model', sa.Column('dataset_id', sa.String(length=64), nullable=True))
    op.drop_column('gpt_model', 'dataset_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('gpt_model', sa.Column('dataset_name', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    op.drop_column('gpt_model', 'dataset_id')
    # ### end Alembic commands ###
