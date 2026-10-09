from sqlalchemy import text

from app.infrastructure.database.connection import engine


def add_user_id_column():
    with engine.begin() as connection:
        connection.execute(
            text(
                """
                ALTER TABLE recommendations
                ADD COLUMN IF NOT EXISTS user_id INTEGER
                """
            )
        )

        connection.execute(
            text(
                """
                UPDATE recommendations
                SET user_id = 1
                WHERE user_id IS NULL
                """
            )
        )

        connection.execute(
            text(
                """
                ALTER TABLE recommendations
                ALTER COLUMN user_id SET NOT NULL
                """
            )
        )

        connection.execute(
            text(
                """
                CREATE INDEX IF NOT EXISTS ix_recommendations_user_id
                ON recommendations (user_id)
                """
            )
        )

        connection.execute(
            text(
                """
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1
                        FROM pg_constraint
                        WHERE conname = 'fk_recommendations_user_id'
                    ) THEN
                        ALTER TABLE recommendations
                        ADD CONSTRAINT fk_recommendations_user_id
                        FOREIGN KEY (user_id)
                        REFERENCES users(id);
                    END IF;
                END
                $$;
                """
            )
        )


if __name__ == "__main__":
    add_user_id_column()
    print("user_id column added successfully.")