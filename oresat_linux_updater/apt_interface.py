"""simplified apt interface"""

import json
from apt import cache, debfile


class AptInterface():
    """
    Manges commication to apt using the python apt library. See
    https://apt-team.pages.debian.net/python-apt/contents.html for python-apt's
    API.
    """

    def __init__(self):
        self._cache = cache.Cache()

    def install(self, package_path: str) -> bool:
        """Installs local deb package.

        Parameters
        ----------
        package_path : str
            Absoulte path to a deb package to install.

        Returns
        -------
        bool
            True if package was installed or False on failure.
        """

        deb = debfile.DebPackage(package_path)
        if not deb.check() or deb.install() != 0:
            return False

        return True

    def remove(self, pkg_name: str) -> bool:
        """Removes a package, equivant to `apt remove <pkg_name>`.

        Parameters
        ----------
        pkg_name : str
            A package to remove.

        Returns
        -------
        bool
            True if the package was removed or False on failure.
        """

        package = self._cache[pkg_name]
        if package is None:
            return False

        package.mark_delete()

        self._cache.commit()
        return True

    def package_list(self) -> str:
        """Make a JSON str with a list of all packages currently installed.

        Returns
        -------
        str
            A JSON dictionary of packages and their versions that are
            installed. The key is the package name and value is the package
            version.

        """

        apt_list = {}

        for pkg in self._cache:
            if pkg.is_installed:
                for ver in pkg.versions:
                    if ver.is_installed:
                        apt_list[pkg.shortname] = ver.version

        apt_json = json.dumps(apt_list)

        return apt_json
