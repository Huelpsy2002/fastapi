"""add content column to posts table

Revision ID: 0ba3a0ad1122
Revises: 3c6a9d330b6c
Create Date: 2023-03-11 22:06:56.594418

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ba3a0ad1122'
down_revision = '3c6a9d330b6c'
branch_labels = None
depends_on = None


def upgrade() :
    op.add_column('posts' , sa.Column('content' ,sa.String() , nullable=False ))

    pass


def downgrade() -> None:
    pass
