import versioneer
from setuptools import setup, find_packages


setup(
    name='genemap',
    version=versioneer.get_version(),
     cmdclass=versioneer.get_cmdclass(),
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
    install_requires=['future', 'pandas', 'pybiomart']
)
