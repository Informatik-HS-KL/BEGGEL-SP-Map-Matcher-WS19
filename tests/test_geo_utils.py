import unittest

from src.geo_utils import great_circle, dot_product, vector_addition, scalar_multiplication, vector_subtraction,\
    orthogonal_projection, vector_norm, vectors_have_same_direction, vectors_are_parallel

from math import sqrt


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

    def test_vector_norm(self):
        self.assertEqual(0, vector_norm((0, 0, 0)))
        self.assertEqual(5, vector_norm((0, -5)))
        self.assertEqual(4, vector_norm((-2, -2, 2, 2)))

        self.assertAlmostEqual(sqrt(13), vector_norm((-2, 0, 3)), 16)

        self.assertRaises(Exception, vector_norm, ())

    def test_vectors_are_parallel(self):
        self.assertTrue(vectors_are_parallel((2, 2), (2, 2)))
        self.assertTrue(vectors_are_parallel((1, 1), (-3.7, -3.7)))
        self.assertTrue(vectors_are_parallel((3, -7, 2), (-1.5, 3.5, -1)))
        self.assertTrue(vectors_are_parallel((-2, -11), (-2/9, -11/9)))

        self.assertFalse(vectors_are_parallel((1, 1), (2, 2.000000001)))
        self.assertFalse(vectors_are_parallel((10, -4, 5), (-19.99999999, 8, -10)))
        self.assertFalse(vectors_are_parallel((-4, -5), (8, 10.00000001)))

        self.assertRaises(Exception, vectors_are_parallel, (), ())
        self.assertRaises(Exception, vectors_are_parallel, (1, 2), (1, 2, 0))

    def test_vectors_have_same_direction(self):
        self.assertTrue(vectors_have_same_direction((3, 3), (3, 3)))
        self.assertTrue(vectors_have_same_direction((1, 1), (3.7, 3.7)))
        self.assertTrue(vectors_have_same_direction((3, -7, 2), (1.5, -3.5, 1)))
        self.assertTrue(vectors_have_same_direction((-2, -11), (-2/9, -11/9)))

        self.assertFalse(vectors_have_same_direction((1, 1), (-1, -1)))
        self.assertFalse(vectors_have_same_direction((2, 5, 7), (2, 5.000000001, 7)))
        self.assertFalse(vectors_have_same_direction((3, 4), (-3, 4)))

        self.assertRaises(Exception, vectors_have_same_direction, (), ())
        self.assertRaises(Exception, vectors_have_same_direction, (1, 2), (1, 2, 0))
