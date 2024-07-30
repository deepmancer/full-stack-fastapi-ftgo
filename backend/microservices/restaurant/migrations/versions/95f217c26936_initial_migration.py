"""Initial migration

Revision ID: 95f217c26936
Revises: 
Create Date: 2024-07-28 17:50:53.718557

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95f217c26936'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('supplier',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('owner_user_id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('postal_code', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('address_lat', sa.Float(), nullable=False),
    sa.Column('address_lng', sa.Float(), nullable=False),
    sa.Column('restaurant_licence_id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('menu_item',
    sa.Column('item_id', sa.String(), nullable=False),
    sa.Column('restaurant_id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['restaurant_id'], ['supplier.id'], ),
    sa.PrimaryKeyConstraint('item_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('menu_item')
    op.drop_table('supplier')
    # ### end Alembic commands ###