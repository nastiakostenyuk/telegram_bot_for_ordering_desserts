"""add table to sequrity

Revision ID: 81528d98be56
Revises: bf2a33de7244
Create Date: 2023-04-06 14:13:17.903196

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '81528d98be56'
down_revision = 'bf2a33de7244'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('roles_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['admin_user.id'], )
    )
    op.add_column('admin_user', sa.Column('last_name', sa.String(), nullable=True))
    op.alter_column('admin_user', 'password',
               existing_type=postgresql.BYTEA(),
               type_=sa.String(length=255),
               existing_nullable=True)
    op.drop_constraint('admin_user_first_name_key', 'admin_user', type_='unique')
    op.drop_constraint('admin_user_password_key', 'admin_user', type_='unique')
    op.drop_constraint('admin_user_second_name_key', 'admin_user', type_='unique')
    op.drop_column('admin_user', 'second_name')
    op.drop_column('admin_user', 'role')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('admin_user', sa.Column('role', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('admin_user', sa.Column('second_name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.create_unique_constraint('admin_user_second_name_key', 'admin_user', ['second_name'])
    op.create_unique_constraint('admin_user_password_key', 'admin_user', ['password'])
    op.create_unique_constraint('admin_user_first_name_key', 'admin_user', ['first_name'])
    op.alter_column('admin_user', 'password',
               existing_type=sa.String(length=255),
               type_=postgresql.BYTEA(),
               existing_nullable=True,
               postgresql_using='password::bytea')
    op.drop_column('admin_user', 'last_name')
    op.drop_table('roles_users')
    op.drop_table('role')
    # ### end Alembic commands ###
