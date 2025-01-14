from datetime import datetime
from typing import Any
from uuid import UUID

from langchain_core.documents import Document
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.pydantic_v1 import BaseModel as BaseModelV1
from langchain_core.pydantic_v1 import Field as FieldV1
from pydantic import BaseModel
from typing_extensions import TypedDict


class cited_answer(BaseModelV1):
    """Answer the user question based only on the given sources, and cite the sources used."""

    answer: str = FieldV1(
        ...,
        description="The answer to the user question, which is based only on the given sources.",
    )
    thoughts: str = FieldV1(
        ...,
        description="""Description of the thought process, based only on the given sources.
        Cite the text as much as possible and give the document name it appears in. In the format : 'Doc_name states : cited_text'. Be the most
        procedural as possible. Write all the steps needed to find the answer until you find it.""",
    )
    citations: list[int] = FieldV1(
        ...,
        description="The integer IDs of the SPECIFIC sources which justify the answer.",
    )

    followup_questions: list[str] = FieldV1(
        ...,
        description="Generate up to 3 follow-up questions that could be asked based on the answer given or context provided.",
    )


class ChatMessage(BaseModelV1):
    chat_id: UUID
    message_id: UUID
    brain_id: UUID
    msg: AIMessage | HumanMessage
    message_time: datetime
    metadata: dict[str, Any]


class Source(BaseModel):
    name: str
    source_url: str
    type: str
    original_file_name: str
    citation: str


class RawRAGChunkResponse(TypedDict):
    answer: dict[str, Any]
    docs: dict[str, Any]


class RawRAGResponse(TypedDict):
    answer: dict[str, Any]
    docs: dict[str, Any]


class RAGResponseMetadata(BaseModel):
    citations: list[int] | None = None
    thoughts: str | list[str] | None = None
    followup_questions: list[str] | None = None
    sources: list[Any] | None = None


class ParsedRAGResponse(BaseModel):
    answer: str
    metadata: RAGResponseMetadata | None = None


class ParsedRAGChunkResponse(BaseModel):
    answer: str
    metadata: RAGResponseMetadata
    last_chunk: bool = False


class QuivrKnowledge(BaseModel):
    id: UUID
    brain_id: UUID
    file_name: str | None = None
    url: str | None = None
    extension: str = "txt"
    status: str = "PROCESSING"


# NOTE: for compatibility issues with langchain <-> PydanticV1
class SearchResult(BaseModelV1):
    chunk: Document
    distance: float
