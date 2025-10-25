# pre-entrega-automation-testing-Cristian-Vivar

## Propósito

Automatizar flujos básicos del sitio https://www.saucedemo.com usando Selenium WebDriver y Pytest. Incluye: login, verificación del inventario y agregar producto al carrito.

## Tecnologías

- Python 3.8+
- pytest
- selenium
- webdriver-manager
- pytest-html

## Estructura del repositorio

- tests/                   -> pruebas: `test_login.py`, `test_inventory.py`, `test_cart.py`
- utils/                   -> helpers y page objects: `driver_factory.py`, `pages.py`, `helpers.py`
- reports/                 -> reportes HTML y capturas
  - screenshots/           -> capturas en fallos
- requirements.txt
- conftest.py
- pytest.ini
- README.md

## Instalación de dependencias

1. Crear y activar entorno virtual
   - macOS / Linux:
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```
   - Windows (PowerShell):
     ```powershell
     python -m venv venv
     venv\Scripts\Activate.ps1
     ```
2. Instalar paquetes
   ```bash
   pip install -r requirements.txt