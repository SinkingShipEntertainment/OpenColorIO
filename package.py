name = "ocio"

version = "1.0.9"

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

requires = [
]

private_build_requires = [
    "cmake",
    "gcc",
]

variants = [
    ["platform-linux", "arch-x86_64", "os-centos-7", "python-2.7"]
]

uuid = "repository.OpenColorIO"

def commands():
    env.OCIO_LOCATION = "{root}"
    env.OCIO_ROOT = "{root}"
    env.OCIO_INCLUDE_DIR = "{root}/include"
    env.OCIO_LIBRARY_DIR = "{root}/lib"
    env.LD_LIBRARY_PATH.prepend("{root}/lib")
    env.PATH.append("{root}/bin")

