from pydantic import BaseModel

# Estructura de datos
class AmazonCredentials(BaseModel):
    email: str
    password: str
    mode: str = "headless"  # o "headed"