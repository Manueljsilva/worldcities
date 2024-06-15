import hola 
import unittest

class TestLocateCities(unittest.TestCase):
    
    def test_know_cities(self):
        ciudad1 = hola.Ciudad('Japan', 'Tokyo')
        ciudad2 = hola.Ciudad('Argentina', 'Buenos Aires')
        result = hola.find_distance_between_cities(ciudad1, ciudad2)
        self.assertEqual(result,'18369.58 km')
    def test_city_not_found(self):
        ciudad1 = hola.Ciudad('Westeros', 'Desembarco del Rey')
        ciudad2 = hola.Ciudad('Argentina', 'Buenos Aires')
        result = hola.find_distance_between_cities(ciudad1, ciudad2)
        self.assertEqual(result, 'No se ha encontrado una ciudad.')

if __name__ == '__main__':
    unittest.main()


