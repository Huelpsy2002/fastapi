"""add user table

Revision ID: 9af9b87319d8
Revises: 0ba3a0ad1122
Create Date: 2023-03-12 13:30:50.114201

"""
from pickle import FALSE
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9af9b87319d8'
down_revision = '0ba3a0ad1122'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users' , sa.Column('id' , sa.Integer(),nullable=False ) , 
    sa.Column('email' , sa.String() , nullable=False) , sa.Column('password' , sa.String() , nullable=False),
    sa.Column('created_at' , sa.TIMESTAMP(timezone=True) , server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id') , sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    pass
