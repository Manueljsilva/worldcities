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

# Función principal para encontrar las dos ciudades más cercanas de tres ciudades dadas
def find_closest_pair_of_cities(ciudad1: Ciudad, ciudad2: Ciudad, ciudad3: Ciudad):
    csv_service = CsvLocationService('worldcities.csv')
    
    # Obtener las coordenadas de las tres ciudades
    coord1 = csv_service.get_coordinates(ciudad1)
    coord2 = csv_service.get_coordinates(ciudad2)
    coord3 = csv_service.get_coordinates(ciudad3)

    if not coord1 or not coord2 or not coord3:
        print('No se ha encontrado una o más ciudades.')
        return

    # Calcular las distancias entre cada par de ciudades
    distance_1_2 = haversine(coord1, coord2)
    distance_1_3 = haversine(coord1, coord3)
    distance_2_3 = haversine(coord2, coord3)

    # Determinar el par más cercano
    min_distance = min(distance_1_2, distance_1_3, distance_2_3)
    if min_distance == distance_1_2:
        closest_pair = (ciudad1, ciudad2)
    elif min_distance == distance_1_3:
        closest_pair = (ciudad1, ciudad3)
    else:
        closest_pair = (ciudad2, ciudad3)

    print(f'La distancia más corta es entre {closest_pair[0].ciudad}, {closest_pair[0].pais} y {closest_pair[1].ciudad}, {closest_pair[1].pais} con una distancia de {min_distance:.2f} km.')

# Ejemplo de uso
ciudad1 = Ciudad('Peru', 'Lima')
ciudad2 = Ciudad('Colombia', 'Bogota')
ciudad3 = Ciudad('Argentina', 'Buenos Aires')
find_closest_pair_of_cities(ciudad1, ciudad2, ciudad3)
