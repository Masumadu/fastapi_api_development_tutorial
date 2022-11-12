"""create post table

Revision ID: bdd3882ebf65
Revises: 
Create Date: 2022-11-12 13:14:31.687943

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bdd3882ebf65'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False)
    )


def downgrade():
    op.drop_table("posts")
