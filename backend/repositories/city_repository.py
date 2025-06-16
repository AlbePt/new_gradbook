from sqlalchemy.orm import Session
from models.city import City
from schemas.city import CityCreate

class CityRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, city_id: int) -> City:
        return self.db.query(City).filter(City.id == city_id).first()

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(City).offset(skip).limit(limit).all()

    def create(self, city: CityCreate) -> City:
        db_city = City(**city.dict())
        self.db.add(db_city)
        self.db.commit()
        self.db.refresh(db_city)
        return db_city

    def update(self, city_id: int, updates: dict) -> City:
        db_city = self.get(city_id)
        for key, value in updates.items():
            setattr(db_city, key, value)
        self.db.commit()
        self.db.refresh(db_city)
        return db_city

    def delete(self, city_id: int) -> None:
        db_city = self.get(city_id)
        if db_city:
            self.db.delete(db_city)
            self.db.commit()
