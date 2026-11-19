from typing import Annotated

from fastapi import Depends, HTTPException, Request, status

from app.schemas import User, UserCreate
from app.services.users import UserService, DuplicateUser


def get_service(request: Request) -> UserService:
    return request.app.state.users


Service = Annotated[UserService, Depends(get_service)]


def create_user(data: UserCreate, service: Service) -> User:
    try:
        return service.create(data)
    except DuplicateUser as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=str(exc)) from exc


def list_users(service: Service) -> list[User]:
    return service.list_users()
