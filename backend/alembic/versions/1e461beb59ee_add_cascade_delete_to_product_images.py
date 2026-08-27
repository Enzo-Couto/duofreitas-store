"""add cascade delete to product images

Revision ID: 1e461beb59ee
Revises: 74043ebcfae5
Create Date: 2026-08-26 19:17:27.978454

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e461beb59ee'
down_revision: Union[str, Sequence[str], None] = '74043ebcfae5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_constraint(
        'product_images_product_id_fkey',
        'product_images',
        type_='foreignkey'
    )

    op.create_foreign_key(
        'product_images_product_id_fkey',
        'product_images',
        'products',
        ['product_id'],
        ['id'],
        ondelete='CASCADE'
    )


def downgrade():
    op.drop_constraint(
        'product_images_product_id_fkey',
        'product_images',
        type_='foreignkey'
    )

    op.create_foreign_key(
        'product_images_product_id_fkey',
        'product_images',
        'products',
        ['product_id'],
        ['id']
    )
