import requests

resp = requests.post("http://localhost:5000/predict",
                     files={"file": open('images/cat2.jpg','rb')})
print(resp.json())
