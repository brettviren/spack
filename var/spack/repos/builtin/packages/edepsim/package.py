from spack import *

class Edepsim(CMakePackage):
    """An energy deposition simulation based on Geant4"""
    homepage = "https://github.com/ClarkMcGrew/edep-sim/"
    url = "https://github.com/ClarkMcGrew/edep-sim/archive/2.0.1.tar.gz"

#    version('master', git="https://github.com/ClarkMcGrew/edep-sim.git")
    version('master', git="https://github.com/brettviren/edep-sim.git")
    version('2.0.1', '88afc6f7570f19efd2094fce00585c00')

    depends_on("geant4~qt")
    depends_on("root")
    depends_on('cmake@3.2:', type='build')
