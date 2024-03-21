from sqlalchemy.orm import DeclarativeBase, declared_attr

__all__ = ["Base"]


class Base(DeclarativeBase):

    @declared_attr.directive
    def __tablename__(self) -> str:
        return self.__name__.lower()
