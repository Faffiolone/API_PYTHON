import requests

url= "http://127.0.0.1:8000/cities" 
# Mi metto nell'end point di app.post definito in app_post.py (punto all'end point in gergo)

data = {
    "city": "Strong" ,
    "country": "Indonesia"
}

# Chiamiamo il metodo post all'URL=end point dove abbiamo definito @app.post("/cities")
# E gli passiamo la nuova città da aggiungere in json
# La funzione requests.post ritorna codice di errore o di buon fine che possiamo usare per vedere
# se è stata aggiunta con successo
""" 
request.post simula un client che passa una nuova città in pratica
json= serve per trasformare una lista python in file json
"""
response = requests.post(url,json=data)

if response.status_code==200: # Operazione andata a buon fine
    print(response.json())
else:
    print(f"Errore: {response.status_code} - {response.json}")
    # response.status_code == Codice di errore
    # response.json == tipo di errore
