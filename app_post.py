from fastapi import FastAPI, Query, HTTPException
from typing import Optional
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

"""
Allora, prima di tutto in fondo andiamo a scrivere
L'indirizzo dove verrà utilizzata l'API con uvicorn appena entra nel file
"""
app = FastAPI()

"""
Creiamo la classe dove mettere i dati

A Che serve Pydantic?? City eredita da BaseModel, prendendo quindi gli stessi metodi
Pydantic fa da controllore che i dati siano esattamente come ci aspettiamo,
quindi BaseModel ha dei metodi di controllo che noi ereditiamo che ci aiutano e
ritornano errore se qualcosa è sbagliato
"""
class City(BaseModel):
    city: str
    country: str

# Inseriamo i primi dati, quindi simuliamo un database
data = [
    City(city="Napoli", country="Italy"),
    City(city="Pisa", country="Italy"),
    City(city="Reykjavik", country="Iceland"),
    City(city="Bali", country="Indonesia"),
]


"""
Defininiamo il primo end point, in pratica mettendo 
"/": definiamo le funzioni attivate all'apertura della pagina
In questo caso deve solo restituire codice HTML per la pagina
response_class=HTMLResponse indica al browser come interpretare la stringa (quindi html)
"""
@app.get("/", response_class=HTMLResponse)

async def root():
    return """
    <html>
        <head>
            <title>Cities API</title>
        </head>
        <body>
            <h1>Benvenuto nella API Cities</h1>
            <p>Vai su <a href="/docs">/docs</a> per vedere la documentazione automatica.</p>
        </body>
    </html>
    """

"""
Defininiamo il secondo end point, andando su \cities si attiverà
la funzione get_cities a cui potremmo passare degli attributi country e city
per filtrare e restituire le info filtrate
Per Esempio:
\cities?country=Italy  Abbiamo solo citta italiane
\cities?country=Italy&city=Napoli   Abiamo solo Napoli in pratica
\cities     Non abbiamo dato niente in input quindi la funzione per come l'abbiamo
    costruita restituisce tutto
"""

@app.get("/cities")
async def get_cities(city: Optional[str]= Query(None),country:Optional[str] = Query(None)):
    if city and country:
        filtered_cities = [c for c in data if c.city == city and c.country == country]
    elif city:
        filtered_cities = [c for c in data if c.city == city]
    elif country:
        filtered_cities = [c for c in data if c.country == country]
    else:
        filtered_cities = data
    return filtered_cities

"""
Terzo Endpoint: POST /cities
Questo metodo ascolta sullo stesso indirizzo '/cities' ma risponde solo
alle chiamate di tipo POST (usate per inviare dati/creare risorse).
"""
# devo pero creare un altro file per fare il post con i dati
# che andrà in questo end point con il metodo app.post definito e gli passera i dati
@app.post("/cities")

async def add_city(newcity: City):
    for existing_city in data:
        if existing_city.city == newcity.city and existing_city.country == newcity.country:
            raise HTTPException(status_code=400, detail=f"La città {newcity.city} - {newcity.country} esiste già nel database.")
    data.append(newcity)
    return {"message": f"City {newcity.city} added"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0", port=8000)