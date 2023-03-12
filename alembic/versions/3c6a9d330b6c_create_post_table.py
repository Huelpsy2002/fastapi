"""create post table

Revision ID: 3c6a9d330b6c
Revises: 
Create Date: 2023-03-11 01:36:14.431417

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c6a9d330b6c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None :
    op.create_table('posts', sa.Column('id' , sa.Integer()  ,primary_key=True,  nullable=False) , 
    sa.Column('title' , sa.String() ,nullable = False ))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
