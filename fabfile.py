# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import re
from datetime import datetime


# 导入API
from fabric.api import *


env.user = 'ubuntu'
env.sudo_user = 'root'
env.hosts = ['52.196.36.151']


_TAR_FILE = 'dist-simp1e.tar.gz'
_REMOTE_TMP_TAR = '/tmp/%s' % _TAR_FILE
_REMOTE_BASE_DIR = '/srv/Webapp'


def build():
    includes = ['static', 'templates', 'favicon.ico', '*py']
    excludes = ['test', '.*', '*.pyc', '*pyo']
    local('rm -f dist/%s' % _TAR_FILE)
    with lcd(os.path.join(os.path.abspath('.'), 'wwww')):
        cmd = ['tar', '--dereference', '-czvf', '../dist/%' % _TAR_FILE]
        cmd.extend(['--exclude=\'%s\'' % ex for ex in excludes])
        cmd.extend(includes)
        local(''.join(cmd))


def delpay():
    newdir = 'simp1e-%s' % datetime.now().strftime('%y-%m-%d\
                                                    _%H.%M.%S')
    run('rm -f %s' % _REMOTE_TMP_TAR)
    put('dist/%s' % _TAR_FILE, _REMOTE_TMP_TAR)

    with cd(_REMOTE_BASE_DIR):
        sudo('mkdir %s' % newdir)
    with cd('%s%s' % (_REMOTE_BASE_DIR, newdir)):
        sudo('tar -xzvf %s' % _REMOTE_TMP_TAR)
