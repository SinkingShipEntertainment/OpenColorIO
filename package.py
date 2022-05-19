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


# name = "ocio"
name = "ocio_tools"

version = "2.1.1"

description = \
    """
    OpenColorIO (OCIO) is a complete color management solution geared towards motion
    picture production with an emphasis on visual effects and computer animation.
    """

with scope("config") as c:
    # Determine location to release: internal (int) vs external (ext)

    # NOTE: Modify this variable to reflect the current package situation
    release_as = "ext"

    # The `c` variable here is actually rezconfig.py
    # `release_packages_path` is a variable defined inside rezconfig.py

    import os
    if release_as == "int":
        c.release_packages_path = os.environ["SSE_REZ_REPO_RELEASE_INT"]
    elif release_as == "ext":
        c.release_packages_path = os.environ["SSE_REZ_REPO_RELEASE_EXT"]

# ---------------------------------------
# For building ocio
# requires = [
#     "glew",
#     "libexpat",
#     "yamlcpp",
#     "pystring",
#     "pybind11",
#     "imath",
# ]

# ---------------------------------------
# For building ocio_tools
requires = [
    "glew",
    "libexpat",
    "yamlcpp",
    "pystring",
    "pybind11",
    "imath",
    "lcms",
    "oiio",
]

private_build_requires = [
]

variants = [
    ["platform-linux", "arch-x86_64", "os-centos-7", "python-2"],
    ["platform-linux", "arch-x86_64", "os-centos-7", "python-3"],
]

uuid = "repository.OpenColorIO"


def pre_build_commands():
    command("source /opt/rh/devtoolset-6/enable")

def commands():
    env.OCIO_LOCATION = "{root}"
    env.OCIO_ROOT = "{root}"
    env.OCIO_INCLUDE_DIR = "{root}/include"
    env.OCIO_LIBRARY_DIR = "{root}/lib"
    env.PATH.append("{root}/bin")