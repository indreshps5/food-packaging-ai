from sqlalchemy.orm import Session

from app.infrastructure.database.models.user_model import UserModel


class UserRepositoryImpl:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        username: str,
        email: str,
        password_hash: str,
    ) -> UserModel:

        user = UserModel(
            username=username,
            email=email,
            password_hash=password_hash,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def get_by_id(
        self,
        user_id: int,
    ) -> UserModel | None:

        return (
            self.db.query(UserModel)
            .filter(UserModel.id == user_id)
            .first()
        )

    def get_by_username(
        self,
        username: str,
    ) -> UserModel | None:

        return (
            self.db.query(UserModel)
            .filter(UserModel.username == username)
            .first()
        )

    def get_by_email(
        self,
        email: str,
    ) -> UserModel | None:

        return (
            self.db.query(UserModel)
            .filter(UserModel.email == email)
            .first()
        )