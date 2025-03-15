"""remove name field

Revision ID: 8a985714a733
Revises: 5ff202acb55d
Create Date: 2025-03-15 03:13:13.134936

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '8a985714a733'
down_revision: Union[str, None] = '5ff202acb55d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
