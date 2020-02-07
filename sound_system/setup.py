from setuptools import setup
from glob import glob

package_name = 'sound_system'

setup(
    name=package_name,
    version='0.0.1',
    packages=[],
    py_modules=[
        'sound_system'
    ],
    install_requires=['setuptools'],
    data_files=[
        ('lib/' + package_name, ['package.xml', 'sound_system.py']),
        ('lib/' + package_name + '/module',glob('module/*.py')),
        ('lib/sound_system/dictionary',glob('dictionary/*.dict')),
        ('lib/sound_system/dictionary',glob('dictionary/*.gram')),
        ('lib/sound_system/dictionary/QandA',glob('dictionary/QandA/*')),
        ('lib/sound_system/beep',glob('beep/*'))
    ],
    zip_safe=True,
    author='momonga',
    author_email='is0506he@ed.ritsumei.ac.jp',
    maintainer='momonga',
    maintainer_email='is0506he@ed.ritsumei.ac.jp',
    keywords=['ROS2'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description='sound package for SPR',
    license='Apache License, Version 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'sound_system = sound_system:main',
        ],
    },
)
