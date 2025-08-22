"""create users table


Revision ID: 20250822_0001
Revises: None
Create Date: 2025-08-22 00:01:00
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '20250822_0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:


    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('user', sa.String(length=80), nullable=False, index=True),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('dosha', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.UniqueConstraint('user', name='uq_users_user')
    )


def downgrade() -> None:


    op.drop_table('users')
