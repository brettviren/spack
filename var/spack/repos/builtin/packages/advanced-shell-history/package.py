from spack import *
import os
import sys

class AdvancedShellHistory(Package):
    """ Advanced Shell History """

    homepage = "https://github.com/brettviren/advanced-shell-history/"
    url = "https://github.com/brettviren/advanced-shell-history/0.0.0.tar.gz"
    
    version('develop', branch='master',
            git='https://github.com/brettviren/advanced-shell-history.git')


    depends_on('sqlite')

    def install(self, spec, prefix):
        config_args = ['waf','configure', '--prefix={0}'.format(prefix),
                       '--with-sqlite={}'.format(spec['sqlite'].prefix)]
        config_argstr = ' '.join(config_args)

        syspy = which("python")

        syspy(*config_args)
        syspy('waf')
        syspy('waf', 'install')

