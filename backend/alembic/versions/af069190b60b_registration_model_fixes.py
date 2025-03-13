"""Registration Model Fixes

Revision ID: af069190b60b
Revises: 599bd613c9dd
Create Date: 2025-03-13 17:50:28.341686

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'af069190b60b'
down_revision: Union[str, None] = '599bd613c9dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('refresh_tokens')
    op.drop_index('ix_revoked_tokens_token', table_name='revoked_tokens')
    op.drop_table('revoked_tokens')
    op.drop_constraint('users_username_key', 'users', type_='unique')
    op.drop_column('users', 'username')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    op.create_unique_constraint('users_username_key', 'users', ['username'])
    op.create_table('revoked_tokens',
    sa.Column('token', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('expires_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('token', name='revoked_tokens_pkey')
    )
    op.create_index('ix_revoked_tokens_token', 'revoked_tokens', ['token'], unique=False)
    op.create_table('refresh_tokens',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('token', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name='refresh_tokens_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='refresh_tokens_pkey')
    )
    # ### end Alembic commands ###
