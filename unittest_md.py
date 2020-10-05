import sys, unittest
from md import calcenergy
from ase.lattice.cubic import FaceCenteredCubic
from asap3 import EMT

class MdTests(unittest.TestCase):

    def test_calcenergy(self):
        
        atoms = FaceCenteredCubic(directions=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                              symbol="Cu", size=(10, 10, 10), pbc=True)
        atoms.calc = EMT()
        en = calcenergy(atoms)
        bool0 = abs(en[0] + 0.001) < 0.005
        #bool1 = abs(en[1] - 0.039) < 0.005
        #bool2 = abs(en[2] - 301) < 5
        #bool3 = abs(en[3] - 0.038) < 0.005

        self.assertTrue(bool0,"0")
        #self.assertTrue(bool1,"1")
        #self.assertTrue(bool2,"2")
        #self.assertTrue(bool3,"3")
        


if __name__ == '__main__':

    tests = [unittest.TestLoader().loadTestsFromTestCase(MdTests)]
    testsuite = unittest.TestSuite(tests)
    result = unittest.TextTestRunner(verbosity=0).run(testsuite)
    sys.exit(not result.wasSuccessful())
