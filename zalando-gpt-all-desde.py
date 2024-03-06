from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Configuración del WebDriver
service = Service(executable_path="C:\\chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.maximize_window()
url = "https://www.zalando.es/release-calendar/zapatillas-mujer/"
driver.get(url)

# Espera explícita hasta que el contenedor de productos esté presente
contenedor_productos_xpath = '//*[@id="themed-homes-pagemon"]/div[2]/div/div'
contenedor_productos = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, contenedor_productos_xpath)))

# Obtener todos los productos dentro del contenedor
productos = contenedor_productos.find_elements(By.XPATH, './div')

# Lista para almacenar los datos de los productos
datos_productos = []

# Iterar sobre cada producto encontrado
for producto in productos:
    datos = {}
    datos['Marca'] = producto.find_element(By.XPATH, ".//header/div[1]/h3[1]").text
    datos['Modelo'] = producto.find_element(By.XPATH, ".//header/div[1]/h3[2]").text

    # Intentar encontrar el precio con múltiples XPaths
    precio_xpath_options = [
        ".//header/section/article/p/span",  # Estructura con nodo <article>
        ".//header/section/p/span"  # Estructura sin nodo <article>
    ]
    
    precio_encontrado = False
    for precio_xpath in precio_xpath_options:
        try:
            datos['Precio'] = producto.find_element(By.XPATH, precio_xpath).text
            precio_encontrado = True
            break
        except Exception:
            continue
    
    if not precio_encontrado:
        datos['Precio'] = "No disponible"
    
    try:
        datos['Imagen'] = producto.find_element(By.XPATH, ".//a/figure/div/div/img").get_attribute("src")
    except Exception:
        datos['Imagen'] = "No disponible"
    
    # Intentar encontrar la fecha de salida
    fecha_salida_elementos = producto.find_elements(By.CSS_SELECTOR, ".sDq_FX.lystZ1.dgII7d.HlZ_Tf")
    if fecha_salida_elementos:
        datos['Fecha Salida'] = fecha_salida_elementos[0].text
    else:
        datos['Fecha Salida'] = "No disponible"
    
    datos_productos.append(datos)

# Convertir la lista a DataFrame
df_productos = pd.DataFrame(datos_productos)

# Mostrar el DataFrame
print(df_productos)

# Cerrar el navegador
driver.quit()