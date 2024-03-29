"""edit name is_active

Revision ID: 2f730f04fcb1
Revises: dd2ec8b82c7c
Create Date: 2023-04-26 18:39:29.602046

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f730f04fcb1'
down_revision = 'dd2ec8b82c7c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('admin_user', 'active')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('admin_user', sa.Column('active', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
