import csv
import os
from datetime import datetime
from app.database import SessionLocal, engine
from app import models
from app.schemas import RegionEnum

# Veritabanı tablolarının oluştuğundan emin olalım
models.Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    filename = "clan_sample_data.csv"
    
    if not os.path.exists(filename):
        print(f"Hata: {filename} bulunamadı!")
        return

    print("Veri aktarımı başlıyor...")
    success_count = 0
    skipped_count = 0

    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            name = row['name'].strip() if row['name'] else None
            region_str = row['region'].strip() if row['region'] else None
            created_at_str = row['created_at'].strip() if row['created_at'] else None

            # 1. Validasyon: Boş veri kontrolü
            if not name or not region_str or not created_at_str:
                print(f"Atlandı (Eksik Veri): {row}")
                skipped_count += 1
                continue
            
            # 2. Validasyon: Region kontrolü (Enum kullanarak)
            try:
                valid_region = RegionEnum(region_str)
            except ValueError:
                print(f"Atlandı (Geçersiz Region): {name} - Region: {region_str}")
                skipped_count += 1
                continue

            try:
                # Tarih formatını parse et
                created_at = datetime.strptime(created_at_str, "%Y-%m-%d %H:%M:%S")
                
                # Veritabanı nesnesini oluştur
                clan = models.Clan(
                    name=name,
                    region=valid_region.value,
                    created_at=created_at
                )
                db.add(clan)
                success_count += 1
                
            except ValueError as e:
                print(f"Atlandı (Tarih Hatası): {name} - {created_at_str}")
                skipped_count += 1
                continue

    db.commit()
    db.close()
    
    # Hata veren kısım burası olabilir, sadeleştirdim:
    print("-" * 30)
    print("İşlem Tamamlandı.")
    print(f"Başarılı Kayıt: {success_count}")
    print(f"Atlanan Kayıt: {skipped_count}")

if __name__ == "__main__":
    seed_data()