"""empty message

Revision ID: 55f91f24d89f
Revises:
Create Date: 2024-04-10 01:39:35.154930

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "55f91f24d89f"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "scan",
        sa.Column(
            "id",
            sa.Uuid(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("domain", sa.String(), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "result",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("scan_id", sa.Uuid(), nullable=False),
        sa.Column("tool", sa.String(), nullable=False),
        sa.Column(
            "type",
            sa.Enum("DOMAIN", "IP_ADDRESS", "EMAIL", "URL", "ASN", name="type"),
            nullable=False,
        ),
        sa.Column("value", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["scan_id"], ["scan.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("scan_id", "tool", "type", "value", name="unique_result"),
    )


def downgrade() -> None:
    op.drop_table("result")
    op.drop_table("scan")
