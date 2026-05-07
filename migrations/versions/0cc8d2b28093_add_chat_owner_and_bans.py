"""add chat owner and bans

Revision ID: 0cc8d2b28093
Revises: 722440cc8790
Create Date: 2026-05-07 22:10:42.308352
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0cc8d2b28093'
down_revision = '722440cc8790'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Добавляем owner_id как nullable
    with op.batch_alter_table('chats', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('owner_id', sa.Integer(), nullable=True)
        )

    # 2. Для старых чатов ставим владельцем первого участника
    op.execute("""
        UPDATE chats
        SET owner_id = sub.user_id
        FROM (
            SELECT DISTINCT ON (chat_id)
                chat_id,
                user_id
            FROM memberships
            ORDER BY chat_id, id ASC
        ) AS sub
        WHERE chats.id = sub.chat_id
          AND chats.owner_id IS NULL
    """)

    # 3. Если вдруг чат без участников — ставим первого пользователя
    op.execute("""
        UPDATE chats
        SET owner_id = (
            SELECT id
            FROM users
            ORDER BY id ASC
            LIMIT 1
        )
        WHERE owner_id IS NULL
    """)

    # 4. Делаем owner_id обязательным + FK
    with op.batch_alter_table('chats', schema=None) as batch_op:
        batch_op.alter_column(
            'owner_id',
            existing_type=sa.Integer(),
            nullable=False
        )

        batch_op.create_foreign_key(
            'fk_chats_owner_id_users',
            'users',
            ['owner_id'],
            ['id']
        )

    # 5. Добавляем бан
    with op.batch_alter_table('memberships', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                'is_banned',
                sa.Boolean(),
                nullable=False,
                server_default=sa.false()
            )
        )

        batch_op.alter_column(
            'is_banned',
            server_default=None
        )


def downgrade():
    with op.batch_alter_table('memberships', schema=None) as batch_op:
        batch_op.drop_column('is_banned')

    with op.batch_alter_table('chats', schema=None) as batch_op:
        batch_op.drop_constraint(
            'fk_chats_owner_id_users',
            type_='foreignkey'
        )

        batch_op.drop_column('owner_id')