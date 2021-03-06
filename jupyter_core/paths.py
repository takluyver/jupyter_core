# encoding: utf-8
"""Path utility functions."""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Derived from IPython.utils.path, which is
# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.


import os
import sys

pjoin = os.path.join


def get_home_dir():
    """Get the real path of the home directory"""
    homedir = os.path.expanduser('~')
    # Next line will make things work even when /home/ is a symlink to
    # /usr/home as it is on FreeBSD, for example
    homedir = os.path.realpath(homedir)
    return homedir


def jupyter_config_dir():
    """Get the Jupyter config directory for this platform and user.
    
    Returns JUPYTER_CONFIG_DIR if defined, else ~/.jupyter
    """

    env = os.environ
    home_dir = get_home_dir()

    if env.get('JUPYTER_CONFIG_DIR'):
        return env['JUPYTER_CONFIG_DIR']
    
    return pjoin(home_dir, '.jupyter')


def jupyter_data_dir():
    """Get the config directory for Jupyter data files.
    
    These are non-transient, non-configuration files.
    
    Returns JUPYTER_DATA_DIR if defined, else a platform-appropriate path.
    """
    env = os.environ
    
    if env.get('JUPYTER_DATA_DIR'):
        return env['JUPYTER_DATA_DIR']
    
    home = get_home_dir()

    if sys.platform == 'darwin':
        return os.path.join(home, 'Library', 'Jupyter')
    elif os.name == 'nt':
        appdata = os.environ.get('APPDATA', None)
        if appdata:
            return pjoin(appdata, 'jupyter')
        else:
            return pjoin(jupyter_config_dir(), 'data')
    else:
        # Linux, non-OS X Unix, AIX, etc.
        xdg = env.get("XDG_DATA_HOME", None)
        if not xdg:
            xdg = pjoin(home, '.local', 'share')
        return pjoin(xdg, 'jupyter')


def jupyter_runtime_dir():
    """Return the runtime dir for transient jupyter files.
    
    Returns JUPYTER_RUNTIME_DIR if defined.
    
    Respects XDG_RUNTIME_HOME on non-OS X, non-Windows,
    falls back on data_dir/runtime otherwise.
    """
    env = os.environ
    
    if env.get('JUPYTER_RUNTIME_DIR'):
        return env['JUPYTER_RUNTIME_DIR']
    
    if sys.platform == 'darwin':
        return pjoin(jupyter_data_dir(), 'runtime')
    elif os.name == 'nt':
        return pjoin(jupyter_data_dir(), 'runtime')
    else:
        # Linux, non-OS X Unix, AIX, etc.
        xdg = env.get("XDG_RUNTIME_HOME", None)
        if xdg:
            return pjoin(xdg, 'jupyter')
        return pjoin(jupyter_data_dir(), 'runtime')


if os.name == 'nt':
    programdata = os.environ.get('PROGRAMDATA', None)
    if programdata:
        SYSTEM_JUPYTER_PATH = [pjoin(programdata, 'jupyter')]
    else:  # PROGRAMDATA is not defined by default on XP.
        SYSTEM_JUPYTER_PATH = [os.path.join(sys.prefix, 'share', 'jupyter')]
else:
    SYSTEM_JUPYTER_PATH = [
        "/usr/local/share/jupyter",
        "/usr/share/jupyter",
    ]

ENV_JUPYTER_PATH = [os.path.join(sys.prefix, 'share', 'jupyter')]


def jupyter_path(*subdirs):
    """Return the list of directories to search
    
    JUPYTER_PATH environment variable has highest priority.
    
    If *subdirs are given, that subdirectory will be added to each element.
    
    Examples:
    
    >>> jupyter_path()
    ['~/.local/jupyter', '/usr/local/share/jupyter']
    >>> jupyter_path('kernels')
    ['~/.local/jupyter/kernels', '/usr/local/share/jupyter/kernels']
    """
    
    paths = []
    # highest priority is env
    if os.environ.get('JUPYTER_PATH'):
        paths.extend(
            p.rstrip(os.sep)
            for p in os.environ['JUPYTER_PATH'].split(os.pathsep)
        )
    # then user dir
    paths.append(jupyter_data_dir())
    # then sys.prefix
    for p in ENV_JUPYTER_PATH:
        if p not in SYSTEM_JUPYTER_PATH:
            paths.append(p)
    # finally, system
    paths.extend(SYSTEM_JUPYTER_PATH)
    
    # add subdir, if requested
    if subdirs:
        paths = [ pjoin(p, *subdirs) for p in paths ]
    return paths

