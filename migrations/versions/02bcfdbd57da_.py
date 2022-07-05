"""empty message

Revision ID: 02bcfdbd57da
Revises: 
Create Date: 2022-07-05 14:34:05.971873

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02bcfdbd57da'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('guideline')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('guideline',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.Column('content', sa.TEXT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='guideline_pkey'),
    sa.UniqueConstraint('title', name='guideline_title_key')
    )
    # ### end Alembic commands ###
