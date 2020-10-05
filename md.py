from asap3 import Trajectory
from ase.lattice.cubic import FaceCenteredCubic
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.verlet import VelocityVerlet
from ase import units

# Use Asap for a huge performance increase if it is installed
use_asap = True

if use_asap:
    from asap3 import EMT
    size = 10
else:
    from ase.calculators.emt import EMT
    size = 3

def calcenergy(a):
    """Function to print the potential, kinetic and total energy."""
    epot = a.get_potential_energy() / len(a) * 100
    ekin = a.get_kinetic_energy() / len(a)
    temp = ekin / (1.5 * units.kB)
    etot = epot + ekin
    return (epot, ekin, temp, etot)

def run_md():
    
    # Set up a crystal
    atoms = FaceCenteredCubic(directions=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                              symbol="Cu",
                              size=(size, size, size),
                              pbc=True)

    # Describe the interatomic interactions with the Effective Medium Theory
    atoms.calc = EMT()
    
    # Set the momenta corresponding to T=300K
    MaxwellBoltzmannDistribution(atoms, 300 * units.kB)

    # We want to run MD with constant energy using the VelocityVerlet algorithm.
    dyn = VelocityVerlet(atoms, 2 * units.fs)  # 5 fs time step.
    traj = Trajectory('cu.traj', 'w', atoms)
    dyn.attach(traj.write, interval=10)


    def printenergy(a=atoms):  # store a reference to atoms in the definition.
         print('Energy per atom: Epot = %.3feV  Ekin = %.3feV (T=%3.0fK)  '
               'Etot = %.3feV' % calcenergy(a))

    # Now run the dynamics
    dyn.attach(printenergy, interval=10)
    printenergy()
    dyn.run(500)

if __name__ == "__main__":
    run_md()
