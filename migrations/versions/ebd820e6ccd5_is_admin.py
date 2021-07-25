"""'is_admin'

Revision ID: ebd820e6ccd5
Revises: a519c21bdf8b
Create Date: 2021-06-21 12:24:46.155364

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ebd820e6ccd5'
down_revision = 'a519c21bdf8b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_admin', sa.Boolean(), nullable=True))
    op.add_column('user', sa.Column('verified', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'verified')
    op.drop_column('user', 'is_admin')
    # ### end Alembic commands ###
