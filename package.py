name = "memoboard"

version = "1.0.0"

authors = [
    "Nico Van den Bosch"
]

description = \
    """
    A memcached based shared clipboard solution
    """

tools = [
    "myth_protocol_handler"
]

requires = [
    "python",
    "python_memcached",
    "pyperclip"
]

uuid = "packages.memoboard"

# this appears to be the recommended way to install internally developed packages
# into a non-desktop release path
# unclear if support for multiple release paths was actually implemented/released in rez:
#https://github.com/nerdvegas/rez/issues/426
#https://github.com/nerdvegas/rez/pull/402
with scope("config") as c:
    c.release_packages_path = "/software/packages/internal"

def commands():
    env.PYTHONPATH.append("{root}/python")
    env.PATH.append("{root}/bin")
