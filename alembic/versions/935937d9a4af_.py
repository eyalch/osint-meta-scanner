"""empty message

Revision ID: 935937d9a4af
Revises:
Create Date: 2024-04-08 18:43:50.364505

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "935937d9a4af"
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
            sa.Enum("FQDN", "IP_ADDRESS", "EMAIL", "URL", "ASN", name="type"),
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
