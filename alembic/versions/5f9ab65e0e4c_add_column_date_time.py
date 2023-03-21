"""add column date time

Revision ID: 5f9ab65e0e4c
Revises: 58941bad64c0
Create Date: 2023-03-21 23:04:14.184037

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5f9ab65e0e4c'
down_revision = '58941bad64c0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('date_time', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comments', 'date_time')
    # ### end Alembic commands ###
