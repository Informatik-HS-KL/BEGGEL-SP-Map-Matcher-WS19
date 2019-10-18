import unittest

from src.geo_utils import great_circle, dot_product, vector_addition, scalar_multiplication, vector_subtraction, orthogonal_projection


class TestLinkDistance(unittest.TestCase):

    def test_great_circle(self):
        a = (49.186697, 7.629492)
        b = (49.187240, 7.629905)

        self.assertEqual(round(great_circle(a, b), 5), 0.06743)

    def test_dot_product(self):
        a = (1, 2)
        b = (3, 4)
        self.assertEqual(dot_product(a, b), 11)
        a = (-1, -2)
        b = (3, -4)
        self.assertEqual(dot_product(a, b), 5)
        a = (1, 0)
        b = (0, 1)
        self.assertEqual(dot_product(a, b), 0)
        a = (1, 0, 3, 4)
        b = (0, 1, 5, 6)
        self.assertEqual(dot_product(a, b), 39)
        a = (1, 2, 3)
        b = (4, 5, 6, 7)
        self.assertRaises(Exception, dot_product, a, b)
        a = ()
        b = ()
        self.assertRaises(Exception, dot_product, a, b)

    def test_vector_addition(self):
        a = (1, 2)
        b = (3, 4)
        self.assertEqual(vector_addition(a, b), (4, 6))
        a = (-1, -2)
        b = (3, -4)
        self.assertEqual(vector_addition(a, b), (2, -6))
        a = (1, 0)
        b = (0, 1)
        self.assertEqual(vector_addition(a, b), (1, 1))
        a = (1, 0, 3, 4)
        b = (0, 1, 5, 6)
        self.assertEqual(vector_addition(a, b), (1, 1, 8, 10))
        a = (1, 2, 3)
        b = (4, 5, 6, 7)
        self.assertRaises(Exception, vector_addition, a, b)
        a = ()
        b = ()
        self.assertRaises(Exception, vector_addition, a, b)

    def test_scalar_multiplication(self):
        a = 2
        b = (3, 4)
        self.assertEqual(scalar_multiplication(a, b), (6, 8))
        a = -1
        b = (3, -4)
        self.assertEqual(scalar_multiplication(a, b), (-3, 4))
        a = 3
        b = (0, 1)
        self.assertEqual(scalar_multiplication(a, b), (0, 3))
        a = 0
        b = (0, 1, 5, 6)
        self.assertEqual(scalar_multiplication(a, b), (0, 0, 0, 0))
        a = 1
        b = ()
        self.assertRaises(Exception, scalar_multiplication, a, b)

    def test_orthogonal_projection(self):
        a = (1, 2)
        b = (3, 4)
        c = orthogonal_projection(a, b)
        self.assertAlmostEqual(c[0], 33/25, 7)
        self.assertAlmostEqual(c[1], 44 / 25, 7)
        a = (-1, -2)
        b = (3, -4)
        c = orthogonal_projection(a, b)
        self.assertAlmostEqual(c[0], 3 / 5, 7)
        self.assertAlmostEqual(c[1], -4/5, 7)
        pass

    def test_vector_subtraction(self):
        a = (1, 2)
        b = (3, 4)
        self.assertEqual(vector_subtraction(a, b), (-2, -2))
        a = (-1, -2)
        b = (3, -4)
        self.assertEqual(vector_subtraction(a, b), (-4, 2))
        a = (1, 0)
        b = (0, 1)
        self.assertEqual(vector_subtraction(a, b), (1, -1))
        a = (1, 0, 3, 4)
        b = (0, 1, 5, 6)
        self.assertEqual(vector_subtraction(a, b), (1, -1, -2, -2))
        a = (1, 2, 3)
        b = (4, 5, 6, 7)
        self.assertRaises(Exception, vector_subtraction, a, b)
        a = ()
        b = ()
        self.assertRaises(Exception, vector_subtraction, a, b)
