from setuptools import find_packages, setup

setup(
    name='Transformation',
    version= 1.0,
    description='A base class to handle files.',
    author='Abhinav singh',
    author_email='abhinav.s2@partner.samsung.com',
    include_package_data=True,
    keywords=['Transform'],
    install_requires=['numpy'],
    packages=find_packages(exclude=['docs','tests*','results','venv'])
)