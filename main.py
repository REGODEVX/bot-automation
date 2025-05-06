from  fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from amazon.amazon_bot import AmazonAutomation
from amazon.models import AmazonCredentials
from config import API_HOST, API_PORT
import logging

# Crea API
app = FastAPI()

#Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitudes de cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los headers
)

#endpoint POST 
@app.post("/simulate-purchase")
def simulate_purchase(credentials: AmazonCredentials):
    try:
        bot = AmazonAutomation(mode=credentials.mode)
        success = bot.simulate_purchase(
            email=credentials.email,
            password=credentials.password,
        )

        if not success:
            raise HTTPException(status_code=400, detail="Error durante la simulación de compra")

        return {"message": "Simulación de compra completada exitosamente"}

    except Exception as e:
        logging.error(f"Error en la API: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)


