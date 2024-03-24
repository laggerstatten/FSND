"""myMigration

Revision ID: 15d3505700b5
Revises: 
Create Date: 2023-08-09 23:02:51.610858

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15d3505700b5'
down_revision = None
branch_labels = None
depends_on = None

# TODO: change schema

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Institution',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Animal',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('genus', sa.String(length=120), nullable=True),
    sa.Column('species', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Specimen',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('animal_id', sa.Integer(), nullable=False),
    sa.Column('institution_id', sa.Integer(), nullable=False),
    sa.Column('sightingdate', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['institution_id'], ['Institution.id'], ),
    sa.ForeignKeyConstraint(['animal_id'], ['Animal.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Specimen')
    op.drop_table('Animal')
    op.drop_table('Institution')
    # ### end Alembic commands ###