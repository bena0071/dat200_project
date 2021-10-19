"""empty message

Revision ID: 60186e5647b5
Revises: 4a9db05ce51d
Create Date: 2021-10-18 15:34:16.752769

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60186e5647b5'
down_revision = '4a9db05ce51d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'comment', 'user', ['user_id'], ['id'])
    op.drop_column('user', 'last_seen')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('last_seen', sa.DATETIME(), nullable=True))
    op.drop_constraint(None, 'comment', type_='foreignkey')
    op.drop_column('comment', 'user_id')
    # ### end Alembic commands ###