"""Add role column to user_profile

Revision ID: 1cebbb92e812
Revises: e2d77720993d
Create Date: 2024-07-06 23:44:05.573387

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1cebbb92e812'
down_revision: Union[str, None] = 'e2d77720993d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

op.drop_table('user_profile')
op.drop_table('user_address')
def upgrade():
    op.drop_table('user_profile')
    op.drop_table('user_address')
    # Add the new column with a default value temporarily
    op.add_column('user_profile', sa.Column('role', sa.String(), nullable=True))

    # Update the column for existing rows to have a default value
    op.execute('UPDATE user_profile SET role = \'CUSTOMER\' WHERE role IS NULL')

    # Alter the column to be non-nullable
    op.alter_column('user_profile', 'role', nullable=False, existing_type=sa.String())

def downgrade():
    # Revert the changes
    op.alter_column('user_profile', 'role', nullable=True, existing_type=sa.String())
    op.drop_column('user_profile', 'role')
