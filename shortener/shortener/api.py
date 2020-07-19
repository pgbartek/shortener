from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

from . import repository
from .models import Redirect


router = APIRouter()


@router.post("/")
async def create_redirect(redirect: Redirect) -> Redirect:
    if not redirect.url_id:
        redirect.url_id = Redirect.generate_url_id()

    try:
        created_redirect = await repository.create_redirect(redirect)
    except repository.RedirectExistsException:
        raise HTTPException(409, "conflict")
    except repository.RedirectRepositoryException:
        raise HTTPException(503, "service unavailable")
    else:
        return created_redirect


@router.get("/{url_id}")
async def redirect(url_id: str) -> RedirectResponse:
    try:
        redirect = await repository.get_redirect(url_id)
    except repository.RedirectNotFoundException:
        raise HTTPException(404, "redirect not found")
    except repository.RedirectRepositoryUnavailableException:
        raise HTTPException(503, "service unavailable")
    else:
        return RedirectResponse(url=redirect.url)
