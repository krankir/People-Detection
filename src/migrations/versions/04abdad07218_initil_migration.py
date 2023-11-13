"""initil migration

Revision ID: 04abdad07218
Revises: 
Create Date: 2023-11-09 11:35:57.584611

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '04abdad07218'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task_status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('doc_url', sa.Text(), nullable=True),
    sa.Column('task_status_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['task_status_id'], ['task_status.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_task_status_id'), 'task', ['task_status_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_task_task_status_id'), table_name='task')
    op.drop_table('task')
    op.drop_table('task_status')
    # ### end Alembic commands ###
