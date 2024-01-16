"""init contact model

Revision ID: 8f35070ab375
Revises: 50dcd302bae3
Create Date: 2024-01-09 16:53:31.429906

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8f35070ab375'
down_revision: Union[str, None] = '50dcd302bae3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('label',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('label_name', sa.String(length=100), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_label_id'), 'label', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_label_id'), table_name='label')
    op.drop_table('label')
    # ### end Alembic commands ###
