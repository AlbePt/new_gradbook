from sqlalchemy.orm import Session
from models.region import Region
from schemas.region import RegionCreate

class RegionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, region_id: int) -> Region:
        return self.db.query(Region).filter(Region.id == region_id).first()

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(Region).offset(skip).limit(limit).all()

    def create(self, region: RegionCreate) -> Region:
        db_region = Region(**region.dict())
        self.db.add(db_region)
        self.db.commit()
        self.db.refresh(db_region)
        return db_region

    def update(self, region_id: int, updates: dict) -> Region:
        db_region = self.get(region_id)
        for key, value in updates.items():
            setattr(db_region, key, value)
        self.db.commit()
        self.db.refresh(db_region)
        return db_region

    def delete(self, region_id: int) -> None:
        db_region = self.get(region_id)
        if db_region:
            self.db.delete(db_region)
            self.db.commit()
