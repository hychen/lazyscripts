#!/usr/bin/env python
#@FIXME: not perfect way.
import os
import sys
import commands

class BuildDeb(object):

    BUILD_DIR = 'bdist'

    #{{{def prepare():
    def prepare(self):
        #Prepare root directory.
        os.system("rm -rf %s" % self.BUILD_DIR)
        os.system("mkdir -p %s" % self.BUILD_DIR)

        #Extract source codes.
        pkgname = 'lazyscripts-%s' % tagname
        gitcmd = "git archive --prefix=%s/ %s | (cd %s && tar xf -)" % \
                    (pkgname, tagname, self.BUILD_DIR)
        ret = commands.getoutput(gitcmd)
        if ret:
            print "Extracting sources faild."
            exit()

        self.TARGET_DIR = os.path.join(self.BUILD_DIR, pkgname)
        #Copy debian direcotry into dist source.
#  cmd = "cp -a %s %s/debian" % (self.DEBIAN_DIR, self.TARGET_DIR)
        os.system(cmd)

        #Change metadata.
    #}}}

    #{{{def build():
    def build(self):
        cmd = "cd %s && debuild -rfakeroot" % self.TARGET_DIR
        os.system(cmd)
        print """The deb created on %s, this is just for test, you should type
         `%s`after the modification""" % (self.BUILD_DIR,cmd)
    #}}}
pass

if __name__ == '__main__':
    #Example: ./build_deb v0.2rc3
    try:
        tagname = sys.argv[1]
        print "Building deb for reversion:%s" % tagname
    except IndexError:
        print "Error!"
        exit()

    o = BuildDeb()
    o.prepare()
    o.build()
