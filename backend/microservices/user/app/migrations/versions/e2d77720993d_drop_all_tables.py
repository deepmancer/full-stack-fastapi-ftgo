"""drop all tables

Revision ID: e2d77720993d
Revises: 2fdb1ce376f5
Create Date: 2024-07-06 23:42:53.558943

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e2d77720993d'
down_revision: Union[str, None] = '2fdb1ce376f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
