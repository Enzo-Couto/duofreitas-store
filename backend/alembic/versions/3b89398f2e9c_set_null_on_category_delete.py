"""set null on category delete

Revision ID: 3b89398f2e9c
Revises: 4c976c7ed418
Create Date: 2026-08-25 15:49:32.653641

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b89398f2e9c'
down_revision: Union[str, Sequence[str], None] = '4c976c7ed418'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_constraint(
        "products_category_id_fkey",
        "products",
        type_="foreignkey"
    )

    op.create_foreign_key(
        "products_category_id_fkey",
        "products",
        "categories",
        ["category_id"],
        ["id"],
        ondelete="SET NULL"
    )


def downgrade():
    op.drop_constraint(
        "products_category_id_fkey",
        "products",
        type_="foreignkey"
    )

    op.create_foreign_key(
        "products_category_id_fkey",
        "products",
        "categories",
        ["category_id"],
        ["id"]
    )
