from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Item, Tender, Party
from app.schemas import ItemCreate, ItemResponse
from app.chilecompra import import_data

app = FastAPI(title="API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4321", "http://frontend:4321"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health():
    return {"status": "ok"}


# Graph endpoints
@app.get("/api/import")
def run_import(db: Session = Depends(get_db)):
    """Import data from JSONL file into database."""
    return import_data(db)


@app.get("/api/tenders")
def get_tenders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of tenders."""
    total = db.query(Tender).count()
    tenders = db.query(Tender).offset(skip).limit(limit).all()
    return {"total": total, "tenders": tenders}


@app.get("/api/tenders/{tender_id}")
def get_tender(tender_id: int, db: Session = Depends(get_db)):
    """Get a specific tender with its parties."""
    tender = db.query(Tender).filter(Tender.id == tender_id).first()
    if not tender:
        return {"error": "Tender not found"}
    parties = db.query(Party).filter(Party.tender_id == tender_id).all()
    return {"tender": tender, "parties": parties}


@app.get("/api/parties")
def get_parties(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of parties."""
    parties = db.query(Party).offset(skip).limit(limit).all()
    return parties


