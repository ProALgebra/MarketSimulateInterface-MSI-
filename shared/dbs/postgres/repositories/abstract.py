import abc

from typing import Generic, List, Type, TypeVar, Union

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.dbs.postgres.models.base_model import Base

AbstractModel = TypeVar("AbstractModel")


class Repository(Generic[AbstractModel]):
    type_model: Type[Base]
    session: AsyncSession

    def __init__(self, type_model: Type[Base], session: AsyncSession):
        """
        Initialize abstract repository class
        :param type_model: Which model will be used for operations
        :param session: Session in which repository will work
        """
        self.type_model = type_model
        self.session = session

    async def get(self, ident: Union[int, str]) -> AbstractModel:
        """
        Get an ONE model from the database with PK
        :param ident: Key which need to find entry in database
        :return:
        """
        return await self.session.get(entity=self.type_model, ident=ident)

    async def exists(self, ident: Union[int, str]) -> bool:
        """
        Checking the presence of the indexer in the database
        :param ident: Primary key of the model
        :return: True if the model exists, False otherwise
        """
        return (await self.get(ident)) is not None

    async def get_by_where(self, whereclause) -> Union[AbstractModel, None]:
        """
        Get an ONE model from the database with whereclause
        :param whereclause: Clause by which entry will be found
        :return: Model if only one model was found, else None
        """
        statement = select(self.type_model).where(whereclause)
        return (await self.session.execute(statement)).scalar_one_or_none()

    async def get_many(self, whereclause, limit: int = 100, order_by=None) -> List[AbstractModel]:
        """
        Get many models from the database with whereclause
        :param whereclause: Where clause for finding models
        :param limit: (Optional) Limit count of results
        :param order_by: (Optional) Order by clause

        :return: List of founded models
        """
        statement = select(self.type_model).where(whereclause).limit(limit)
        if order_by:
            statement = statement.order_by(order_by)

        return (await self.session.scalars(statement)).all()

    async def delete(self, whereclause) -> None:
        """
        Delete model from the database

        :param whereclause: (Optional) Which statement
        :return: Nothing
        """
        statement = delete(self.type_model).where(whereclause)
        await self.session.execute(statement)

    @abc.abstractmethod
    async def new(self, *args, **kwargs) -> None:
        """
        This method is need to be implemented in child classes,
        it is responsible for adding a new model to the database
        :return: Nothing
        """
        ...
