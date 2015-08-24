from setuptools import setup, find_packages

install_requires = ['pandas', 'rpy2']

setup(
    name='genemap',
    version='0.1.0',
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
