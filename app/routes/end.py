from fastapi import APIRouter, Request, Depends, Form, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.deps import templates, get_db
from app import models
from datetime import datetime, timezone

router = APIRouter(tags=["end"])


@router.get("/end", name="end_session")
def end_questions(request: Request, session_id: str = Query(...)):
    """
    Show the post-session reflection form.
    """
    return templates.TemplateResponse(
        "end_questions.html",
        {"request": request, "session_id": session_id},
    )


@router.post("/end", name="save_end_session")
def save_end_questions(
    request: Request,
    session_id: str = Form(...),
    db: Session = Depends(get_db),
    progress: str = Form(...),
    levers_used: str = Form(...),  # comma-separated
    state_score: int = Form(...),
    state_text: str = Form(...),
):
    """
    Save the reflection AFTER the session.
    """
    reflection = models.Reflection(
        session_id=session_id,
        phase="after",
        goal=None,  # we don’t ask goal again here
        levers=levers_used.split(","),
        state={"score": state_score, "text": state_text},
        model=None,
        created_at=datetime.now(timezone.utc),
    )
    db.add(reflection)
    db.commit()

    # After saving, redirect to dashboard
    return RedirectResponse(url="/", status_code=303)
