# generated by fastapi-codegen:
#   filename:  zkp.yml
#   timestamp: 2024-05-13T07:43:28+00:00

from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(
    title='RP Flask REST API',
    description='An API about zkp key',
    version='1.0.0',
    servers=[{'url': '/zkp'}],
)


@app.get('/puzs', response_model=None, tags=['key'])
def zkp_initial_get__pzs() -> None:
    pass


@app.get('/pzs', response_model=None, tags=['key'])
def zkp_initial_get_pzs() -> None:
    pass