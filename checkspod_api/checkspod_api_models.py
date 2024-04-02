from pydantic import BaseModel
from typing import List


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
    audio: APINestedResource
    duration: float
    cover: APINestedResource
    status: str
    _id: str
    isStarter: bool


class APIEpisodeResponse(BaseModel):
    results: List[APIEpisode]
