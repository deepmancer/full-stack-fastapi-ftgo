"""drop all tables

Revision ID: cfe302323b63
Revises: d027879506f1
Create Date: 2024-07-06 23:27:52.517615

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cfe302323b63'
down_revision: Union[str, None] = 'd027879506f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
