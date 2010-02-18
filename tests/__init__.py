import unittest
import tempfile

# load testsuites from module.
from tests import console, config, pkgmgr, basepool, gitpool, script, env, runner

def suite():
    suite = unittest.TestSuite()
    suite.addTest(config.suite())
    suite.addTest(pkgmgr.suite())
    suite.addTest(basepool.suite())
    suite.addTest(gitpool.suite())
    suite.addTest(script.suite())
    suite.addTest(env.suite())
    suite.addTest(runner.suite())
    suite.addTest(console.suite())
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
