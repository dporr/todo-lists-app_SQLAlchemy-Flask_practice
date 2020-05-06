"""empty message

Revision ID: e19490e8ef71
Revises: 531c19a73f7c
Create Date: 2020-05-06 00:37:22.310275

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e19490e8ef71'
down_revision = '531c19a73f7c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todos', sa.Column('list_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'todos', 'todo_lists', ['list_id'], ['id'])
    op.execute("INSERT INTO todo_lists VALUES(1, 'Uncategorized');")
    op.execute("UPDATE todos SET list_id=1 WHERE list_id IS NULL;")
    op.alter_column('todos', 'list_id', nullable= False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'todos', type_='foreignkey')
    op.drop_column('todos', 'list_id')
    # ### end Alembic commands ###