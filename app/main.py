from fastapi import Request, Depends
from sqlalchemy.orm import Session
from app.deps import templates, get_db
from app import models
from app.routes import start, session, end
from fastapi import FastAPI

app = FastAPI()

# Register routers
app.include_router(start.router)
app.include_router(session.router)
app.include_router(end.router)

@app.get("/")
def dashboard(request: Request, db: Session = Depends(get_db)):
    """
    Show recent sessions and their reflections.
    """
    sessions = (
        db.query(models.FocusSession)
        .order_by(models.FocusSession.start_time.desc())
        .limit(10)
        .all()
    )
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "sessions": sessions},
    )
