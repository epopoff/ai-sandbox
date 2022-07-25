Для запуска:

docker build -t ai_sandbox .
docker run -p 5000:5000 -t ai_sandbox


Для отправки изображения:
python demo.py

или

curl -X POST -d '{"url": "<ссылка на картинку>"}' -H 'Content-Type: application/json' http://127.0.0.1:5000/predict