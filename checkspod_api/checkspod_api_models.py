from pydantic import BaseModel
from typing import List, Union


class APINestedResource(BaseModel):
    filename: str
    filetype: str
    originalname: str
    size: int
    url: str


class APIEpisode(BaseModel):
    title: str
    alias: str
    show: str
    owner: str
    creationDate: str
    publishDate: str
    summary: str
    type: str
    explicit: bool
    duration: float
    status: str
    cover: Union[APINestedResource, None]
    audio: APINestedResource
    _id: str
    isStarter: bool


class APIEpisodeResponse(BaseModel):
    results: List[APIEpisode]
