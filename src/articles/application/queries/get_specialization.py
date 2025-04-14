from dataclasses import dataclass

from articles.application.dto.article import SpecializationDTO
from articles.application.ports.repo import ArticleReader
from common.application.dto import PaginatedDTO
from common.application.query import PaginationParams, Query, QueryHandler


@dataclass(frozen=True, slots=True)
class GetSpecializations(Query[PaginatedDTO[SpecializationDTO]]):
    pagination: PaginationParams
    name: str | None = None


@dataclass(frozen=True, slots=True)
class GetSpecializationsHandler(QueryHandler[GetSpecializations, PaginatedDTO[SpecializationDTO]]):
    _reader: ArticleReader

    async def __call__(self, query: GetSpecializations) -> PaginatedDTO[SpecializationDTO]:
        return await self._reader.get_specialization(query)
