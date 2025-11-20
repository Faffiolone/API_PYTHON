import requests
import io 
from PIL import Image

response = requests.get("https://cataas.com/cat?filter=mono")

image = Image.open(io.BytesIO(response.content))

print(response)
print(type(response.content))
image.save("cat.jpeg")
print("Salvata immagine")