"""empty message

Revision ID: a63d9d1e1d50
Revises:
Create Date: 2022-02-13 19:57:03.304817

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid


# revision identifiers, used by Alembic.
revision = 'a63d9d1e1d50'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'secrets',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('password_hash', sa.String(5000), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=func.now())
    )

def downgrade():
    op.drop_table('secrets')
