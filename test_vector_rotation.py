# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 14:25:54 2014

@author: rob
"""
import unittest
import pandas as pd
import numpy as np
from vectorrotation import *

class VectorRotation(unittest.TestCase):
    def setUp(self):
        self.x = pd.Series([0.5, 3, 0.1, 5, 20, 3, 13])
        self.y = pd.Series([1, 8, 12, 6, 6, 9, 2])
        self.z = pd.Series([1, 2, 3, 4, 5])
        self.theta = angle_between(self.x, self.y)

    def test_norm(self):
        z_norm = norm(self.z)
        # 55 = 25 + 16 + 9 + 4 + 1
        self.assertEqual(z_norm, np.sqrt(55))

    def test_normalise(self):
        normalise_z = normalise(self.z)
        self.assertTrue(np.allclose(normalise_z, self.z / np.sqrt(55)))

    def test_equate_lengths(self):
        y = equate_lengths(self.x, self.y)
        self.assertAlmostEqual(norm(self.x), norm(y))

    def test_equate_sum(self):
        y = equate_sum(self.x, self.y)
        self.assertAlmostEqual(self.x.sum(), y.sum())
        
    def test_angle_between(self):
        """
        A triangle with h = 1, a = sqrt(3)/2, o = 0.5
        has angle 30 degrees
        """
        a = np.sqrt(3) / 2
        o = 0.5
        x = pd.Series([a, 0])
        y = pd.Series([a, o])
        theta = angle_between(x, y)
        self.assertAlmostEqual(np.rad2deg(theta), 30)
        
    def test_gs(self):
        self.assertTrue(is_orthonormal(gs(self.x, self.y)))
        
    def test_vector_rotate_2d(self):
        """
        Starting at (0, 1) and rotating 60 degrees
        toward (1, 0) should leave us at (sqrt(3)/2, 0.5).
        But since the elements have to sum to one, z should be rescaled
        appropriately.
        So we should have (3 / (3 + root3), root3 / (3 + root3)
        """
        x = pd.Series([0, 1])
        y = pd.Series([1, 0])
        z = vector_rotate(x, y, np.deg2rad(60))
        root3 = np.sqrt(3)
        self.assertAlmostEqual(z[0], 3 / (3 + root3))
        self.assertAlmostEqual(z[1], root3 / (3 + root3))
      
    def test_vector_rotate_high_d(self):
        """
        Rotate x all the way round to y.
        Should leave x and y colinear.
        """
        x = pd.Series(np.random.rand(35) * 1e6)
        y = pd.Series(np.random.rand(35))
        theta = angle_between(x, y)
        x_dash = vector_rotate(x, y, theta)
        # Is x_dash the same as y (once adjusted for constant sum)
        self.assertTrue(np.allclose(x_dash, equate_sum(x, y)))
        self.assertTrue(_vectors_are_colinear(x_dash, y))
    
    def test_vector_rotate_by_zero(self):
        """
        Rotate by zero should leave x unchanged
        """
        x = pd.Series(np.random.rand(35) * 1e6)
        y = pd.Series(np.random.rand(35))
        x_dash = vector_rotate(x, y, 0)
        self.assertTrue(np.allclose(x, x_dash))
        self.assertTrue(_vectors_are_colinear(x, x_dash))

    def test_rotate_and_go_back(self):
        """
        If you rotate x toward y and back toward x by the
        same angle, you should end up with exactly x
        """
        x = pd.Series(np.random.rand(35) * 1e6)
        y = pd.Series(np.random.rand(35))
        alpha = np.deg2rad(1)
        x_dash = vector_rotate(x, y, alpha)
        x_dash_dash = vector_rotate(x_dash, x, alpha)
        self.assertTrue(np.allclose(x, x_dash_dash))
        
        
def _vectors_are_colinear(x, y):
    """
    If vectors are colinear dot product should be equal
    to product of L2 norms
    """
    return np.allclose(x.dot(y), norm(x) * norm(y))
        
if __name__ == '__main__':
    unittest.main(exit=False)