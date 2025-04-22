from sqlalchemy.orm import Session
from models import User, QuestionnaireResponse, UserPoops
from auth import verify_password, get_password_hash
from sqlalchemy.sql.expression import func
from datetime import date
from sqlalchemy import desc

def create_user(db: Session, username: str, password: str):
    hashed_password = get_password_hash(password)
    db_user = User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if user and verify_password(password, user.hashed_password):
        return user
    return None


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def save_questionnaire_response(db: Session, user_id: int, question: str, answer: str):
    entry = QuestionnaireResponse(user_id=user_id, question=question, answer=answer)
    db.add(entry)
    db.commit()

def save_daily_input(db: Session, user_id: int, poop_date: date, poop_count: int, poop_type: str, poop_color: str, poop_size: str):
    entry = UserPoops(
        user_id=user_id,
        poop_date=poop_date,
        poop_count=poop_count,
        poop_type=poop_type,
        poop_color=poop_color,
        poop_size=poop_size
    )
    db.add(entry)
    db.commit()

def get_user_inputs(db: Session, user_id: int):
    return db.query(UserPoops).filter(UserPoops.user_id == user_id).order_by(UserPoops.poop_date).all()

def get_user_stats(db: Session, user_id: int):
    # Get all entries ordered by date
    entries = db.query(UserPoops).filter(UserPoops.user_id == user_id).order_by(UserPoops.poop_date).all()
    
    # Calculate total poops
    total_poops = sum(entry.poop_count for entry in entries)
    
    # Get daily counts for the chart
    daily_counts = []
    for entry in entries:
        daily_counts.append({
            "date": entry.poop_date.isoformat(),
            "count": entry.poop_count,
            "type": entry.poop_type,
            "color": entry.poop_color,
            "size": entry.poop_size
        })
    
    # Get most common type and color
    type_counts = {}
    color_counts = {}
    for entry in entries:
        type_counts[entry.poop_type] = type_counts.get(entry.poop_type, 0) + entry.poop_count
        color_counts[entry.poop_color] = color_counts.get(entry.poop_color, 0) + entry.poop_count
    
    most_common_type = max(type_counts.items(), key=lambda x: x[1])[0] if type_counts else None
    most_common_color = max(color_counts.items(), key=lambda x: x[1])[0] if color_counts else None
    
    # Convert distributions to lists with consistent structure
    type_distribution = []
    for poop_type, count in type_counts.items():
        type_distribution.append({
            "type": poop_type,
            "count": count,
            "percentage": (count / total_poops * 100) if total_poops > 0 else 0
        })
    
    color_distribution = []
    for poop_color, count in color_counts.items():
        color_distribution.append({
            "color": poop_color,
            "count": count,
            "percentage": (count / total_poops * 100) if total_poops > 0 else 0
        })
    
    return {
        "total_poops": total_poops,
        "daily_counts": daily_counts,
        "most_common_type": most_common_type,
        "most_common_color": most_common_color,
        "type_distribution": type_distribution,
        "color_distribution": color_distribution
    }


