##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import os
import spack.llnl.util.tty as tty
from spack.llnl.util.tty.color import *
import spack
from spack.error import SpackError
from spack.util import argparse
import spack.cmd
import pkgutil

# Command parsing
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description="Spack: the Supercomputing PACKage Manager." + colorize("""

spec expressions:
  PACKAGE [CONSTRAINTS]

    CONSTRAINTS:
      @c{@version}
      @g{%compiler  @compiler_version}
      @B{+variant}
      @r{-variant} or @r{~variant}
      @m{=architecture}
      [^DEPENDENCY [CONSTRAINTS] ...]"""))

parser.add_argument('-d', '--debug', action='store_true',
                    help="Write out debug logs during compile")
parser.add_argument('-D', '--pdb', action='store_true',
                    help="Run spack under the pdb debugger")
parser.add_argument('-k', '--insecure', action='store_true',
                    help="Do not check ssl certificates when downloading.")
parser.add_argument('-m', '--mock', action='store_true',
                    help="Use mock packages instead of real ones.")
parser.add_argument('-p', '--profile', action='store_true',
                    help="Profile execution using cProfile.")
parser.add_argument('-v', '--verbose', action='store_true',
                    help="Print additional output during builds")
parser.add_argument('-V', '--version', action='version',
                    version="%s" % spack.spack_version)

# each command module implements a parser() function, to which we pass its
# subparser for setup.
subparsers = parser.add_subparsers(metavar='SUBCOMMAND', dest="command")

# locate commands as modules under spack.cmd
for importer, modname, ispkg in pkgutil.iter_modules(spack.cmd.__path__):
    if ispkg:
        continue
    module = spack.cmd.get_module(modname)
    subparser = subparsers.add_parser(modname, help=module.description)
    module.setup_parser(subparser)


# Just print help and exit if run with no arguments at all
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

# actually parse the args.
args = parser.parse_args()

def main():

    # Set up environment based on args.
    tty.set_verbose(args.verbose)
    tty.set_debug(args.debug)
    spack.debug = args.debug

    if spack.debug:
        import spack.util.debug as debug
        debug.register_interrupt_handler()

    spack.spack_working_dir = os.getcwd()
    if args.mock:
        from spack.repository import RepoPath
        spack.repo.swap(RepoPath(spack.mock_packages_path))

    # If the user asked for it, don't check ssl certs.
    if args.insecure:
        tty.warn("You asked for --insecure, which does not check SSL certificates.")
        spack.curl.add_default_arg('-k')

    # Try to load the particular command asked for and run it
    command = spack.cmd.get_command(args.command)
    try:
        return_val = command(parser, args)
    except SpackError, e:
        e.die()
    except KeyboardInterrupt:
        sys.stderr.write('\n')
        tty.die("Keyboard interrupt.")

    # Allow commands to return values if they want to exit with some other code.
    if return_val is None:
        sys.exit(0)
    elif isinstance(return_val, int):
        sys.exit(return_val)
    else:
        tty.die("Bad return value from command %s: %s" % (args.command, return_val))

def entry():
    # top level switch to run main() under profiler, debugger or just as-is
    if args.profile:
        import cProfile
        cProfile.run('main()', sort='tottime')
    elif args.pdb:
        import pdb
        pdb.run('main()')
    else:
        main()
