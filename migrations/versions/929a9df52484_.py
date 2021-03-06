"""empty message

Revision ID: 929a9df52484
Revises: 6c2c45057040
Create Date: 2017-08-18 19:47:43.137745

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '929a9df52484'
down_revision = '6c2c45057040'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'admin')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('admin', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
