import os
from setuptools import find_packages, setup

# Single source of truth for version
version_ns = {}
with open(os.path.join("cfde_client", "version.py")) as f:
    exec(f.read(), version_ns)
version = version_ns['__version__']

setup(
    name="cfde_client",
    version=version,
    packages=find_packages(),
    entry_points='''
    [console_scripts]
    cfde=cfde_client.main:cli
''',
    install_requires=[
        "bdbag>=1.5.5",
        "Click>=7.0",
        "datapackage>=1.10.0",
        "fair-research-login>=0.1.3",
        "GitPython>=3.0.4",
        "globus-automate-client>=0.4",
        "globus-sdk>=1.8.0",
        "packaging>=20.1",
        "requests>=2.22.0"
    ],
    python_requires=">=3.4"
)
