from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import OTPSession, User

def get_current_user(x_session_token: str = Header(None), db: Session = Depends(get_db)):
    if not x_session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    session = db.query(OTPSession).filter(
        OTPSession.session_token == x_session_token
    ).first()

    if not session:
        raise HTTPException(status_code=401, detail="Invalid session")

    user = db.query(User).filter(User.phone == session.phone).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
