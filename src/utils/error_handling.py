from dataclasses import dataclass
from fastapi import HTTPException
from typing import Protocol
from pydantic import BaseModel


class ResponseProtocol(Protocol):
    status_code: int
    reason_phrase: str


class ServiceResponse(BaseModel):
    def handle_response(self, response: ResponseProtocol):
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.reason_phrase,
            )
