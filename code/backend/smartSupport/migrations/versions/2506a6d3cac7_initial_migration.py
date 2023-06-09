"""Initial migration.

Revision ID: 2506a6d3cac7
Revises: 
Create Date: 2023-03-11 18:40:48.191023

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2506a6d3cac7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('faqs',
    sa.Column('faq_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('query', sa.Text(), nullable=False),
    sa.Column('answer', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('faq_id')
    )
    op.create_table('role',
    sa.Column('role_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('role_id')
    )
    op.create_table('tag',
    sa.Column('tag_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('tag_id')
    )
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=False),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('fs_uniquifier', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('roles_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.role_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.UniqueConstraint('user_id', 'role_id', name='user_role')
    )
    op.create_table('ticket',
    sa.Column('ticket_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('body', sa.Text(), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['student_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('ticket_id')
    )
    op.create_table('user_tags',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.tag_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('tag_id', 'user_id'),
    sa.UniqueConstraint('user_id', 'tag_id', name='user_tag')
    )
    op.create_table('comment',
    sa.Column('comment_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('ticket_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('body', sa.Text(), nullable=False),
    sa.Column('solution', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['ticket_id'], ['ticket.ticket_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('comment_id')
    )
    op.create_table('ticket_tags',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('ticket_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.tag_id'], ),
    sa.ForeignKeyConstraint(['ticket_id'], ['ticket.ticket_id'], ),
    sa.PrimaryKeyConstraint('tag_id', 'ticket_id'),
    sa.UniqueConstraint('ticket_id', 'tag_id', name='ticket_tag')
    )
    op.create_table('vote',
    sa.Column('vote_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('ticket_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['ticket_id'], ['ticket.ticket_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('vote_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vote')
    op.drop_table('ticket_tags')
    op.drop_table('comment')
    op.drop_table('user_tags')
    op.drop_table('ticket')
    op.drop_table('roles_users')
    op.drop_table('user')
    op.drop_table('tag')
    op.drop_table('role')
    op.drop_table('faqs')
    # ### end Alembic commands ###
