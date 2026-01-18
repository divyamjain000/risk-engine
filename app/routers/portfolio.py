from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models import Position

router = APIRouter(prefix="/portfolio")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_portfolio(db: Session = Depends(get_db)):
    positions = db.query(Position).all()
    return {
        "positions": [
            {
                "symbol": p.symbol,
                "quantity": p.quantity,
                "avg_price": p.avg_price
            } for p in positions
        ]
    }

@router.post("/position")
def add_position(
    symbol: str,
    quantity: float,
    avg_price: float,
    db: Session = Depends(get_db)
):
    position = Position(
        symbol=symbol,
        quantity=quantity,
        avg_price=avg_price
    )
    db.add(position)
    db.commit()
    db.refresh(position)
    return {"status": "ok", "id": position.id}
