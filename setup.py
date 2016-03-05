from setuptools import setup, find_packages
setup(
    name = 'spack',
    version = '0.0',
    license = 'GPL',
    url = 'https://github.com/LLNL/spack',
    description = 'A flexible package manager designed to support multiple versions, configurations, platforms, and compilers.',
    author = 'Todd Gamblin',
    author_email = 'spack@googlegroups.com',
    maintainer = 'Brett Viren',
    maintainer_email = 'brett.viren@gmail.com',

    package_dir = {'spack':'lib/spack/spack'},

    packages = find_packages("lib/spack",exclude=('external*',)),

    install_requires = [l for l in open("requirements.txt").readlines() if l.strip()],

    entry_points = dict(
        console_scripts = [
            'spack = spack.cli:main',
        ]
    ),


)

