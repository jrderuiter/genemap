from setuptools import setup, find_packages
from version import get_git_version

install_requires = ['pandas', 'pybiomart']

setup(
    name='genemap',
    version=get_git_version(),
    url='',
    author='Julian de Ruiter',
    author_email='julianderuiter@gmail.com',
    description='',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    entry_points={'console_scripts': [
        'genemap = genemap.main:main',
    ]},
    extras_require={},
    zip_safe=True,
    classifiers=[],
    install_requires=install_requires
)
