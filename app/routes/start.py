from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.deps import templates, get_db
from app import models
from app.deps import get_current_user
import uuid
from datetime import datetime, timezone

router = APIRouter(tags=["start"])


@router.get("/start", name="start")
def start_questions(request: Request):
    return templates.TemplateResponse(
        "start_questions.html", {"request": request}
    )


@router.post("/begin", name="begin")
def begin(
    request: Request,
    current_user: models.User = Depends(get_current_user),   # 👈
    db: Session = Depends(get_db),
    time: str = Form(...),   # session length (minutes, string from form input)
    goal: str = Form(...),
    levers: str = Form(...),  # comma-separated values
    state_score: int = Form(...),
    state_text: str = Form(...),
    model: str = Form(...)
):
    # 1. Create a new focus session
    new_session = models.FocusSession(
        user_id=current_user.id,          # TODO: later tie to real logged-in user
        duration_minutes=int(time),    # ensure we store it as integer
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    # 2. Save the "before" reflection entry
    reflection = models.Reflection(
        session_id=new_session.id,
        phase="before",                # marker: before-session answers
        goal=goal,
        levers=[l.strip() for l in levers.split(",")],  # clean whitespace
        state={"score": state_score, "text": state_text},  # JSON field
        model=model,
        created_at=datetime.now(timezone.utc),
    )
    db.add(reflection)
    db.commit()

    # 3. Redirect to the live session page (session.py will handle countdown)
    url = request.url_for("focus_session").include_query_params(
        session_id=new_session.id,
        duration=time
        )
    return RedirectResponse(url=url, status_code=303)

