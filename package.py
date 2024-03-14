
################################################
################################################
# Building OCIO and OIIO:
#
# Order of building:
# 1) OpenEXR
# 2) OCIO (core), meaning no APPS (command line utilities)
# 3) OIIO using OCIO (core)
# 4) OCIO (full), meaning with APPS
#
# Note that the 4th step is not necessary to run OIIO tools, like:
# - oiiotools
# - maketx.
# The 4th step is only necessary to run OCIO tools like:
# - ociobakelut
# - ociocheck
# - ociochecklut
# - ocioconvert
# - ociodisplay
# - ociolutimage
# - ociomakeclf
# - ocioperf
# - ociowrite
# - pyociodisplay
#
# So, OpenEXR and OIIO are normal REZ packages with their dependencies.
# OCIO is special. There are 2 REZ packages, being created from the same Github repo
# https://github.com/SinkingShipEntertainment/OpenColorIO
#
# There is a branch named rez-vX.X.X which represents the core build.
# There is a branch named rez-vX.X.X-tools which represents the full build.
#
# Once released, both will create different REZ packages at the release area.
# One named "ocio_core" and the other "ocio".
################################################
################################################


name = "ocio"  # Change to OFF in CMakeLists.txt: option(OCIO_BUILD_APPS "Set to OFF to disable command-line apps"
# name = "ocio_tools"  # Change to ON in CMakeLists.txt: option(OCIO_BUILD_APPS "Set to OFF to disable command-line apps"

version = "2.3.2"

description = \
    """
    OpenColorIO (OCIO) is a complete color management solution geared towards motion
    picture production with an emphasis on visual effects and computer animation.
    """

with scope("config") as c:
    import os
    c.release_packages_path = os.environ["SSE_REZ_REPO_RELEASE_EXT"]

# ---------------------------------------
# For building ocio
requires = [
    "glew",
    "libexpat",
    "pybind11",
    "imath",
]

# ---------------------------------------
# For building ocio_tools
# requires = [
#     "glew",
#     "libexpat",
#     "pybind11",
#     "imath",
#     "lcms",
#     "oiio-2.3.15.0",
# ]

private_build_requires = [
]

variants = [
    ["python-3.7"],
    ["python-3.9"],
]

uuid = "repository.OpenColorIO"


def pre_build_commands():

    info = {}
    with open("/etc/os-release", 'r') as f:
        for line in f.readlines():
            if line.startswith('#'):
                continue
            line_info = line.replace('\n', '').split('=')
            if len(line_info) != 2:
                continue
            info[line_info[0]] = line_info[1].replace('"', '')
    linux_distro = info.get("NAME", "centos")
    print("Using Linux distro: " + linux_distro)

    if linux_distro.lower().startswith("centos"):
        command("source /opt/rh/devtoolset-6/enable")
    elif linux_distro.lower().startswith("rocky"):
        pass

def commands():
    env.OCIO_LOCATION = "{root}"
    env.OCIO_ROOT = "{root}"
    env.OCIO_INCLUDE_DIR = "{root}/include"
    env.OCIO_LIBRARY_DIR = "{root}/lib"
    env.PATH.append("{root}/bin")
    env.LD_LIBRARY_PATH.prepend("{root}/lib64")

    if resolve.python.version.major == 3:
        if resolve.python.version.minor == 7:
            env.PYTHONPATH.append("{root}/lib64/python3.7/site-packages")
        elif resolve.python.version.minor == 9:
            env.PYTHONPATH.append("{root}/lib64/python3.9/site-packages")