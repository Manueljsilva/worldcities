import pandas as pd
import math

# Definir la clase Coordenada
class Coordenada:
    def __init__(self, latitud, longitud) -> None:
        self.latitud = latitud
        self.longitud = longitud

# Definir la clase Ciudad
class Ciudad:
    def __init__(self, pais, ciudad) -> None:
        self.pais = pais
        self.ciudad = ciudad

# Definir la interfaz
class LocationService:
    def get_coordinates(self, ciudad: Ciudad) -> Coordenada:
        raise NotImplementedError("Subclasses should implement this!")

# Implementar la clase que lee del CSV
class CsvLocationService(LocationService):
    def __init__(self, csv_file_path):
        # Leer el archivo CSV en un DataFrame de pandas
        self.df = pd.read_csv(csv_file_path)

    def get_coordinates(self, ciudad: Ciudad) -> Coordenada:
        result = self.df[(self.df['city'].str.lower() == ciudad.ciudad.lower()) & (self.df['country'].str.lower() == ciudad.pais.lower())]
        if not result.empty:
            # Si se encuentra, devolver las coordenadas de la primera fila del resultado
            return Coordenada(result.iloc[0]['lat'], result.iloc[0]['lng'])
        return None

# Función para calcular la distancia usando la fórmula del haversine
def haversine(coord1: Coordenada, coord2: Coordenada) -> float:
    R = 6371  # Radio de la Tierra en km
    lat1, lon1 = coord1.latitud, coord1.longitud
    lat2, lon2 = coord2.latitud, coord2.longitud

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

# Función principal para encontrar la distancia entre dos ciudades
def find_distance_between_cities(ciudad1: Ciudad, ciudad2: Ciudad):
    csv_service = CsvLocationService('worldcities.csv')
    
    # Obtener las coordenadas de las dos ciudades
    coord1 = csv_service.get_coordinates(ciudad1)
    coord2 = csv_service.get_coordinates(ciudad2)

    if not coord1 or not coord2:
        return 'No se ha encontrado una ciudad.'
    #si la ciudad es igual 
    if coord1.latitud == coord2.latitud and coord1.longitud == coord2.longitud:
        return 'Es la misma ciudad.'
    # Calcular la distancia usando la fórmula del haversine
    distance = haversine(coord1, coord2)
    return f'{distance:.2f} km' 

# Ejemplo de uso
ciudad1 = Ciudad('Japan', 'Tokyo')
ciudad2 = Ciudad('Argentina', 'Buenos Aires')
find_distance_between_cities(ciudad1, ciudad2)

