"""related tasks to users

Revision ID: d04256a81c81
Revises:
Create Date: 2025-03-17 16:33:38.655864

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "d04256a81c81"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("tasks", sa.Column("user_uuid", sa.Uuid(), nullable=True))
    op.create_foreign_key(None, "tasks", "users", ["user_uuid"], ["uuid"])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "tasks", type_="foreignkey")
    op.drop_column("tasks", "user_uuid")
    # ### end Alembic commands ###
