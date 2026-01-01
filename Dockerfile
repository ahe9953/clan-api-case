# 1. Base Image: Python 3.9'un hafif sürümünü kullanıyoruz
FROM python:3.9-slim

# 2. Çalışma dizinini ayarla
WORKDIR /code

# 3. Bağımlılıkları yükle
# Önce requirements.txt kopyalanır ki kod değişse bile kütüphaneler tekrar indirilmesin (Layer Caching)
COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 4. Uygulama kodunu kopyala
COPY ./app /code/app

# 5. Seed scriptini ve CSV verisini kopyala
COPY ./seed.py /code/
COPY ./clan_sample_data.csv /code/

# 6. Port tanımla (Cloud Run varsayılan olarak 8080 bekler)
EXPOSE 8080

# 7. Uygulamayı başlat
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]