"""comment

Revision ID: f3eeb2e43a65
Revises: 
Create Date: 2023-05-26 22:27:55.448037

"""
from alembic import op
import sqlalchemy as sa
from app.database.models.buisiness_entities import rars_t 

# revision identifiers, used by Alembic.
revision = 'f3eeb2e43a65'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('CREATE SCHEMA IF NOT EXISTS buisiness_entities')
    op.create_table('category',
    sa.Column('title', sa.String(length=100), nullable=False, comment='Title of the category'),
    sa.Column('rars', rars_t, nullable=False, comment='Title of the category'),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('edited_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='buisiness_entities'
    )
    op.create_index(op.f('ix_buisiness_entities_category_title'), 'category', ['title'], unique=False, schema='buisiness_entities')
    op.create_table('product',
    sa.Column('title', sa.String(length=100), nullable=False, comment='Title of the product'),
    sa.Column('flammable', sa.Boolean(), nullable=False, comment='flammable product or not'),
    sa.Column('price', sa.Integer(), nullable=False, comment='price displayed on the platform'),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('edited_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='buisiness_entities'
    )
    op.create_index(op.f('ix_buisiness_entities_product_price'), 'product', ['price'], unique=False, schema='buisiness_entities')
    op.create_index(op.f('ix_buisiness_entities_product_title'), 'product', ['title'], unique=False, schema='buisiness_entities')
    op.create_table('product_to_category',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('product_id', sa.UUID(), nullable=False),
    sa.Column('category_id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('edited_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['buisiness_entities.category.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['buisiness_entities.product.id'], ),
    sa.PrimaryKeyConstraint('product_id', 'category_id'),
    schema='buisiness_entities'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product_to_category', schema='buisiness_entities')
    op.drop_index(op.f('ix_buisiness_entities_product_title'), table_name='product', schema='buisiness_entities')
    op.drop_index(op.f('ix_buisiness_entities_product_price'), table_name='product', schema='buisiness_entities')
    op.drop_table('product', schema='buisiness_entities')
    op.drop_index(op.f('ix_buisiness_entities_category_title'), table_name='category', schema='buisiness_entities')
    op.drop_table('category', schema='buisiness_entities')
    
    rars_t.drop(op.get_bind())
    op.execute('DROP SCHEMA IF EXISTS buisiness_entities RESTRICT')
    # ### end Alembic commands ###
