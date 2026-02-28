import unittest
from ..polycorr import bivariate_cdf


class TestPolycorr(unittest.TestCase):
    def test_bivariate_cdf(self):
        self.assertAlmostEqual(
            first=bivariate_cdf(lower=[-100, -100], upper=[100, 100], corr=1),
            second=1,
            places=3)
