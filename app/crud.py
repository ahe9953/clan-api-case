from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy import func

# Klan oluşturma
def create_clan(db: Session, clan: schemas.ClanCreate):
    db_clan = models.Clan(name=clan.name, region=clan.region)
    db.add(db_clan)
    db.commit()
    db.refresh(db_clan)
    return db_clan

# Tüm klanları listeleme
def get_clans(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Clan).offset(skip).limit(limit).all()

# İsme göre klan arama (İçeren kelime, büyük/küçük harf duyarsız)
def get_clans_by_name(db: Session, name_query: str):
    # 'ilike' case-insensitive (büyük/küçük harf duyarsız) arama yapar
    return db.query(models.Clan).filter(models.Clan.name.ilike(f"%{name_query}%")).all()

# YENİ: Tam eşleşme kontrolü (Kayıt oluştururken kullanacağız)
def get_clan_by_exact_name(db: Session, name: str):
    # Büyük/küçük harf duyarsız tam eşleşme (Case-insensitive match)
    return db.query(models.Clan).filter(models.Clan.name.ilike(name)).first()

# ID'ye göre klan silme
def delete_clan(db: Session, clan_id: str):
    clan = db.query(models.Clan).filter(models.Clan.id == clan_id).first()
    if clan:
        db.delete(clan)
        db.commit()
        return True
    return False

# ID kontrolü (Silme işlemi öncesi var mı diye bakmak için)
def get_clan_by_id(db: Session, clan_id: str):
    return db.query(models.Clan).filter(models.Clan.id == clan_id).first()