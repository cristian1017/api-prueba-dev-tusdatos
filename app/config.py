from dotenv import load_dotenv
import os

load_dotenv()

url_scraper = 'https://procesosjudiciales.funcionjudicial.gob.ec/busqueda-filtros'

jwt_secret_key = os.getenv('SECRET_KEY', 'C4.48*234/$23)?898')

is_get_activity_for_actuaciones_judiciales = False
is_view_chrome_headless = True

user_login_success = {
    'username': os.getenv('AUTH_USERNAME', 'tusdatos'),
    'password': os.getenv('AUTH_PASSWORD', '123456')
}

array_search = [
    {"type": "ofendido",  "id": "0968599020001"},
    {"type": "ofendido",  "id": "0992339411001"},
    {"type": "demandado", "id": "1791251237001"},
    {"type": "demandado", "id": "0968599020001"}
]
