from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models import Position
from app.services.datalake import write_portfolio_snapshot

router = APIRouter(prefix="/portfolio")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def serialize_portfolio(positions):
    return {
        "positions": [
            {
                "symbol": p.symbol,
                "quantity": p.quantity,
                "avg_price": p.avg_price
            }
            for p in positions
        ]
    }

@router.get("/")
def get_portfolio(db: Session = Depends(get_db)):
    positions = db.query(Position).all()
    return serialize_portfolio(positions)

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

    # 🔹 snapshot AFTER state change
    positions = db.query(Position).all()
    snapshot = serialize_portfolio(positions)
    write_portfolio_snapshot(portfolio_id=1, snapshot=snapshot)

    return {"status": "ok", "id": position.id}
