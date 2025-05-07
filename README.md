# 🛒 Automatización de Compra en Amazon con Playwright

![Playwright Logo](https://playwright.dev/img/playwright-logo.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Playwright](https://img.shields.io/badge/playwright-1.42.0-green)

## 📌 Descripción

Este proyecto automatiza el proceso de compra en Amazon utilizando Playwright en Python, incluyendo la navegación por menús hasta la sección específica de "Televisión y Video". El sistema expone una API REST para controlar la automatización y puede ejecutarse en modo headless (sin interfaz gráfica) o headed (con navegador visible).

## 🚀 Características

- ✅ Autenticación en Amazon
- ✅ Navegación por menús: Todo → Electrónicos → Televisión y Video
- ✅ Búsqueda y selección de productos
- ✅ Añadir al carrito y proceder al checkout
- ✅ API REST para controlar la automatización
- ✅ SModos headed y headless
- ✅ Sistema de logging completo
- ✅ Configuración mediante variables de entorno

## 📋 Requisitos

| Componente | Versión |
|------------|---------|
| Python | ≥ 3.8 |
| Playwright | 1.42.0 |
| Navegadores | Chromium, Firefox, WebKit |

## 🛠 Instalación

### 1. Clonar repositorio
```bash
git clone https://github.com/tu-usuario/amazon-automation.git
cd bot-automation
```

### 2. Crear entorno virtual (recomendado)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Instalar browsers para Playwright
```bash
playwright install
```

## 🛠 Configuración
### 1. Editar el archivo .env según sea necesario:
```bash
API_HOST=0.0.0.0
API_PORT=8000
```

### Uso 🔧
### 1. Ejecutar la API
```bash
python main.py
```

La API estará disponible en http://localhost:8000

### Endpoints disponibles
### POST /simulate-purchase

Simula el proceso de compra en Amazon.
Parámetros (JSON):

- 🔘 email: Correo electrónico de Amazon

- 🔘 password: Contraseña de Amazon

- 🔘 mode (opcional): "headless" (default) o "headed"

Ejemplo de solicitud:
```bash
curl -X POST "http://localhost:8000/simulate-purchase" \
-H "Content-Type: application/json" \
-d '{"email":"tu-email@example.com","password":"tu-contraseña","mode":"headless"}'
```