"""empty message

Revision ID: e9057c241482
Revises: 2639cb5f74a4
Create Date: 2026-03-15 13:52:32.199143

"""

from alembic import op
import sqlalchemy as sa


revision = "e9057c241482"
down_revision = "2639cb5f74a4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "questions",
        "question",
        existing_type=sa.VARCHAR(length=255),
        type_=sa.Text(),
        existing_nullable=False,
    )
    op.alter_column(
        "questions",
        "answer",
        existing_type=sa.VARCHAR(length=255),
        type_=sa.Text(),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "questions",
        "question",
        existing_type=sa.Text(),
        type_=sa.VARCHAR(length=255),
        existing_nullable=False,
    )
    op.alter_column(
        "questions",
        "answer",
        existing_type=sa.Text(),
        type_=sa.VARCHAR(length=255),
        existing_nullable=False,
    )
