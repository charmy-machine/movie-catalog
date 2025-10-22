from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/")
def read_root(request: Request) -> dict[str, str]:
    docs_url = request.url.replace(path="/docs")
    return {"docs": str(docs_url)}
