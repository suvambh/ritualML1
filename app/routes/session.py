from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.deps import templates, get_db
from app import models

router = APIRouter(tags=["session"])


@router.get("/session", name="focus_session")
def session_page(
    request: Request,
    session_id: str,
    duration: int = 25,
    db: Session = Depends(get_db)
):
    """
    Renders the countdown timer page for a specific session.
    - `session_id`: the database UUID of the FocusSession
    - `duration`: minutes (default = 25)
    """

    # Optional: fetch session from DB to verify it exists
    focus_session = db.query(models.FocusSession).filter_by(id=session_id).first()

    if not focus_session:
        return templates.TemplateResponse(
            "error.html", {"request": request, "message": "Session not found"}
        )

    return templates.TemplateResponse(
        "session.html",
        {
            "request": request,
            "duration": duration,
            "session_id": session_id,
        },
    )
