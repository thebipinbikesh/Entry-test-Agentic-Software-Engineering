import requests
import sys
from packaging.version import Version

# Get the input file from the command line
file_name = sys.argv[1]

file = open(file_name, "r")

dependencies = 0
packages_not_found = 0
versions_not_found = 0

oldest_package = ""
oldest_version = ""

for line in file:

    line = line.strip()

    # Ignore empty lines
    if line == "":
        continue

    # Get package name and version
    parts = line.split("==")

    package = parts[0]
    version = parts[1]

    dependencies = dependencies + 1

    # Check if package exists on PyPI
    package_url = "https://pypi.org/pypi/" + package + "/json"

    response = requests.get(package_url)

    if response.status_code == 404:
        packages_not_found = packages_not_found + 1
        continue

    # Check if the specific version exists on PyPI
    version_url = (
        "https://pypi.org/pypi/"
        + package
        + "/"
        + version
        + "/json"
    )

    response = requests.get(version_url)

    if response.status_code == 404:
        versions_not_found = versions_not_found + 1

    # Find the oldest pinned release
    if oldest_version == "":
        oldest_package = package
        oldest_version = version
    elif Version(version) < Version(oldest_version):
        oldest_package = package
        oldest_version = version

file.close()

print()
print("Dependencies checked :", dependencies)
print("Packages not on PyPi:", packages_not_found)
print("Versions not on PyPI:", versions_not_found)

if oldest_package != "":
    print("Oldest pinned release:",oldest_package + "==" + oldest_version)