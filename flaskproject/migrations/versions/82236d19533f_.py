"""empty message

Revision ID: 82236d19533f
Revises: 806c31439862
Create Date: 2020-09-06 10:21:46.207087

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82236d19533f'
down_revision = '806c31439862'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('create_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comment', 'create_time')
    # ### end Alembic commands ###
