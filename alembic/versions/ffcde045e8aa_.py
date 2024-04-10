"""empty message

Revision ID: ffcde045e8aa
Revises:
Create Date: 2024-04-10 04:19:37.889317

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ffcde045e8aa"
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
        sa.Column("value", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("tool", sa.String(), nullable=False),
        sa.Column(
            "type",
            sa.Enum(
                "DOMAIN",
                "IP_ADDRESS",
                "EMAIL",
                "URL",
                "ASN",
                "OPEN_PORT",
                "TECHNOLOGY",
                "SOCIAL",
                name="type",
            ),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["scan_id"], ["scan.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("scan_id", "tool", "type", "value", name="unique_result"),
    )


def downgrade() -> None:
    op.drop_table("result")
    op.drop_table("scan")
