from setuptools import setup, find_packages

setup(
    name='mgl2d',
    version='0.1.4',
    description='Simple 2D game library // PySDL2 + modern OpenGL',
    author='maxfish',
    url='https://github.com/maxfish/mgl2d',
    install_requires=[
        'numpy == 1.13.0',
        'Pillow == 4.1.1',
        'PyOpenGL == 3.1.0',
        'PySDL2 == 0.9.6',
        'PyTMX == 3.21.1'
    ],
    packages=find_packages()
)
