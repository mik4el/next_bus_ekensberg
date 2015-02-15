from fabric.api import *
from fabric.contrib.files import exists

env.roledefs = {
    'pi': ['pi@10.0.0.15'],  # requires key based auth on server
}

env.project_name = 'next_bus_ekensberg'
env.source_dir = '/home/pi/source'
env.release_dir = '%s/%s' % (env.source_dir, env.project_name)


def provision():
    """
    Should only run once when creating a new server,
    Provisions using require and then installs project.
    """
    # install apt-get dependencies
    sudo('apt-get --yes --force-yes install python-pip', pty=True)
    sudo('apt-get --yes --force-yes install ntp', pty=True)
    sudo('apt-get --yes --force-yes install x11vnc', pty=True)

    # transfer current release
    transfer_project()

    # install current release
    install_project()


def transfer_project():
    if not exists(env.source_dir):
        # create src directory
        sudo("mkdir %s" % env.source_dir)
    if exists(env.release_dir):
        sudo("rm -rf %s" % env.release_dir)
    sudo("mkdir %s" % env.release_dir)
    with cd(env.release_dir):
        # makes an archive from git using git-archive-all https://github.com/Kentzo/git-archive-all
        local("git-archive-all new_release.tar.gz")
        put("new_release.tar.gz", env.source_dir, use_sudo=True)
        sudo("tar zxf %s/new_release.tar.gz" % env.source_dir)
        put("config.py", env.release_dir, use_sudo=True)
        # make sure that the dir is owned by pi user
        sudo("chown pi:pi -R %s" % env.release_dir)
        local("rm -f new_release.tar.gz")


def install_project():
    """
    Install python project
    """
    with cd(env.release_dir):
        sudo("pip install -r requirements.txt", pty=True)


def deploy():
    transfer_project()
    install_project()


def run_python(operation):
    with cd(env.release_dir):
        sudo("python %s" % operation)


def setup_supervisord():
    if not exists("/home/pi/logs"):
        sudo("mkdir /home/pi/logs")
    sudo("cp %s/supervisord /etc/init.d/supervisord" % env.release_dir)
    sudo("chmod +x /etc/init.d/supervisord")
    sudo("update-rc.d supervisord defaults")
    with cd(env.release_dir):
        sudo("/etc/init.d/supervisord restart")
        sudo("supervisorctl restart next_bus_ekensberg")


def restart():
    with cd(env.release_dir):
        sudo("supervisorctl restart next_bus_ekensberg")


def start():
    with cd(env.release_dir):
        run("export DISPLAY=:0.0 && python next_bus.py")


def start_vnc_server():
    sudo("x11vnc -display :0 -usepw -listen 0.0.0.0")