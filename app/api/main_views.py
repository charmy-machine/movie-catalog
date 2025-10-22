from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/")
def read_root(request: Request, name: str = "Anonymous") -> dict[str, str]:
    docs_url = request.url.replace(path="/docs")
    return {
        "message": f"Hello, {name}!",
        "docs": str(docs_url),
    }
