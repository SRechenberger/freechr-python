import unittest
import random
import math
from examples.gcd import *
from examples.fd import *
from free_chr.finite_domains.constraints import in_domain

class TestGCD(unittest.TestCase):
    def test_gcd_solver(self):
        for _ in range(0,1000):
            a = random.randrange(2, 10000)
            b = random.randrange(2, 10000)
            cs = list(gcd_solver(a,b).constraints())
            self.assertEqual(len(cs), 1)
            self.assertEqual(cs[0], math.gcd(a,b))


class TestFD(unittest.TestCase):
    def test_intersection(self):
        cs = list(fd_solver(
            in_domain('a', 1, 2, 3),
            in_domain('a', 1, 3, 4, 5)
        ).constraints())
        self.assertEqual(len(cs), 1)
        self.assertEqual(cs[0], in_domain('a', 1, 3))

    def test_subsumption(self):
        cs = list(fd_solver(
            in_domain('a', 1, 2, 3),
            in_domain('a', 1, 2),
            in_domain('a', 1)
        ).constraints())
        self.assertEqual(len(cs), 1)
        self.assertEqual(cs[0], in_domain('a', 1))

    def test_inconsistency(self):
        self.assertRaises(Bottom, fd_solver, in_domain('a'))
        self.assertRaises(Bottom, fd_solver, in_domain('a', 1), in_domain('a', 2))



if __name__ == '__main__':
    unittest.main()