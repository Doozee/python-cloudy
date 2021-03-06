import os
import re
import sys
from operator import itemgetter

from fabric.api import local
from fabric.api import run
from fabric.api import task
from fabric.api import sudo
from fabric.api import put
from fabric.api import env
from fabric.api import settings
from fabric.api import hide
from fabric.contrib import files

from cloudy.db.psql import db_psql_default_installed_version
from cloudy.sys.etc import sys_etc_git_commit


def db_pgbouncer_install():
    """ Install pgbouncer - Ex: (cmd:)"""

    # requirements
    requirements = '%s' % ' '.join([
        'pgbouncer',
    ])
    
    # install requirements
    sudo('apt-get -y install {0}'.format(requirements))
    sys_etc_git_commit('Installed pgbouncer')


def db_pgbouncer_configure(dbhost=''):
    """ Install pgbouncer - Ex: (cmd:)"""
    cfgdir = os.path.join(os.path.dirname( __file__), '../cfg')
    
    localcfg = os.path.expanduser(os.path.join(cfgdir, 'pgbouncer/pgbouncer.ini'))
    remotecfg = '/etc/pgbouncer/pgbouncer.ini'
    sudo('rm -rf ' + remotecfg)
    put(localcfg, remotecfg, use_sudo=True)
    if dbhost:
        sudo('sed -i "s/dbhost/{0}/g" {1}'.format(dbhost, remotecfg))

    localdefault = os.path.expanduser(os.path.join(cfgdir, 'pgbouncer/default-pgbouncer'))
    remotedefault = '/etc/default/pgbouncer'
    sudo('rm -rf ' + remotedefault)
    put(localdefault, remotedefault, use_sudo=True)

    sys_etc_git_commit('Configured pgbouncer')


def db_pgbouncer_set_user_password(user, password):
    """ Add user:pass to auth_user in pgbounce - Ex: (cmd:<name>,<password>)"""
    userlist = '/etc/pgbouncer/userlist.txt'
    sudo('touch {0}'.format(userlist))
    sudo('>>{0} echo "{1}" "{2}"'.format(userlist, user, password))
    sudo('chown postgres:postgres {0}'.format(userlist))
    sudo('chmod 600 {0}'.format(userlist))









