from fabric.api import env

from cloudy.db import *
from cloudy.sys import *
from cloudy.aws import *
from cloudy.srv import *
from cloudy.web import *
from cloudy.util import *
from cloudy.srv.recipe_generic_server import srv_setup_generic_server


def srv_setup_web(cfg_files):
    """ Setup a webserver database server - Ex: (cmd:[cfg-file])"""

    cfg = CloudyConfig(filenames=cfg_files)

    # setup generic stuff
    srv_setup_generic_server(cfg_files)

    # hostname, ips
    hostname = cfg.get_variable('webserver', 'hostname')
    if hostname:
        sys_hostname_configure(hostname)
        sys_add_hosts(hostname, '127.0.0.1')

        # setup db server
        dbhost = cfg.get_variable('dbserver', 'db-host')
        if dbhost:
            dbaddress = cfg.get_variable('dbserver', 'listen-address')
            if dbaddress and '*' not in dbaddress:
                sys_add_hosts(dbhost, dbaddress)

    # setup python stuff
    sys_python_install_common()

    # install cache daemon
    sys_memcached_install()
    sys_memcached_configure_memory()
    sys_memcached_configure_interface()

    # install webserver
    webserver = cfg.get_variable('dbserver', 'webserver')
    if webserver.lower() == 'apache':
        web_apache_install()
        web_apache2_install_mods()
    elif webserver.lower() == 'gunicorn':
        web_supervisor_install()

    # install nginx
    web_nginx_install()

    # create web directory
    web_create_data_directory()
    db_psql_install()
    db_pgis_install()
    sys_remove_default_startup('postgresql')
    db_pgpool2_install()
    db_host = cfg.get_variable('webserver', 'db-host')
    if db_host:
        db_pgpool2_configure(db_host)
        db_listen_address = cfg.get_variable('dbserver', 'listen-address')
        if db_listen_address:
            sys_add_hosts(db_host, db_listen_address)

    # geoIP
    web_geoip_install_requirements()
    web_geoip_install_maxmind_api()
    web_geoip_install_maxmind_country()
    web_geoip_install_maxmind_city()








