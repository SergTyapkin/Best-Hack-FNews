from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ....external.postgres.models.user import User


def get_user_by_username(*, username: str, db: Session) -> User:
    user_record = db.query(User).filter(User.username == username).first()

    if not user_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No such user"
        )

    return user_record
