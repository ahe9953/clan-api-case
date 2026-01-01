from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, crud, database

# Veritabanı tablolarını oluştur (İlk çalıştırmada)
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Vertigo Games Clan API",
    description="Klan yönetimi için REST API case study",
    version="1.0.0"
)

# Dependency (Her istekte veritabanı oturumu açıp kapatır)
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Create a clan
@app.post("/clans/", response_model=schemas.Clan, status_code=201)
def create_clan(clan: schemas.ClanCreate, db: Session = Depends(get_db)):
    # 1. Kontrol: İsim daha önce alınmış mı?
    db_clan = crud.get_clan_by_exact_name(db, name=clan.name)
    if db_clan:
        raise HTTPException(status_code=400, detail="Bu klan adı zaten kullanımda.")
    
    # Sorun yoksa oluştur
    return crud.create_clan(db=db, clan=clan)

# 2. List clans (Tümünü getir)
@app.get("/clans/", response_model=List[schemas.Clan])
def read_clans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_clans(db, skip=skip, limit=limit)

# 3. Find clan with name (Arama)
@app.get("/clans/search/", response_model=List[schemas.Clan])
def search_clans(
    name: str = Query(..., min_length=3, description="Aranacak klan adı (en az 3 harf)"),
    db: Session = Depends(get_db)
):
    results = crud.get_clans_by_name(db, name_query=name)
    if not results:
        # Boş liste dönebiliriz veya 404 verebiliriz, arama için boş liste daha uygundur
        return []
    return results

# 4. Delete a specific clan with id
@app.delete("/clans/{clan_id}", status_code=200)
def delete_clan(clan_id: str, db: Session = Depends(get_db)):
    # 1. Önce silinecek klan veritabanında var mı bakalım
    clan = crud.get_clan_by_id(db, clan_id=clan_id)
    
    if not clan:
        raise HTTPException(status_code=404, detail="Silinecek klan bulunamadı.")
    
    # 2. Silme işlemini yap
    crud.delete_clan(db, clan_id=clan_id)
    
    # 3. Geriye bilgilendirici bir JSON dön
    return {
        "detail": "Klan başarıyla silindi.",
        "deleted_id": clan_id,
        "clan_name": clan.name,  # Hangi klanın silindiğini de göstermek şık olur
        "region": clan.region
    }