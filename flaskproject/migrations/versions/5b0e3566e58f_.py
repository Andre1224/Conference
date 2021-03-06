"""empty message

Revision ID: 5b0e3566e58f
Revises: 3e353d4b4ac1
Create Date: 2020-09-05 16:40:24.528994

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b0e3566e58f'
down_revision = '3e353d4b4ac1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('question',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('content', sa.TEXT(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('question')
    # ### end Alembic commands ###
