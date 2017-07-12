from setuptools import setup, find_packages

setup(
    name='mgl2d',
    version='0.1.0',
    description='Simple 2D game library // PySDL2 + modern OpenGL',
    author='maxfish',
    url='https://github.com/maxfish/mgl2d',
    install_requires=[
        'numpy == 1.13.0',
        'Pillow == 4.1.1',
        'PyOpenGL == 3.1.0',
        'PySDL2 == 0.9.5',
        # 'PyTMX == 3.20.17'
        # Manual install a fork with fixes from git+https://github.com/maxfish/PyTMX.git#egg=PyTMX
    ],
    packages=find_packages()
)
