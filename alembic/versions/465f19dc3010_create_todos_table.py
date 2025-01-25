"""create todos table

Revision ID: 465f19dc3010
Revises: 
Create Date: 2025-01-25 17:04:21.447121

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '465f19dc3010'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
    create table todos(
        id bigserial primary key,
        name text,
        completed boolean not null default false
    )
    """)

def downgrade():
    op.execute("drop table todos;")
