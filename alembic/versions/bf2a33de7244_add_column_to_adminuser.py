"""Add column to adminuser

Revision ID: bf2a33de7244
Revises: 9260b79b4eae
Create Date: 2023-04-05 11:58:39.371912

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf2a33de7244'
down_revision = '9260b79b4eae'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('admin_user', sa.Column('role', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('admin_user', 'role')
    # ### end Alembic commands ###
