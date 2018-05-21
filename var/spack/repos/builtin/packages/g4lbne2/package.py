from spack import *
import platform

## home of current version:
#https://cdcvs.fnal.gov/redmine/projects/lbne-beamsim/wiki
## some build instructions
#https://cdcvs.fnal.gov/redmine/projects/lbne-beamsim/wiki/Installation

## home of v2
# https://github.com/DUNE/g4lbne

class G4lbne2(CMakePackage):
    """G4LBNE2 is an unmaintained older version of G4LBNE now at least at
    v3.  G4LBNE uses Geant4 to simulate the LBNE, now DUNE, beam
    neutrino flux.  """

    version('2.5.0', git="https://github.com/DUNE/g4lbne.git", tag="2.5.0")

    depends_on('cmake@3:', type='build')
    depends_on("root@6.10.08")
    depends_on("geant4@10.03.p03")
