from setuptools import setup
from glob import glob

package_name = 'image_system'

setup(

    name=package_name,
    version='0.0.1',
    packages=[],
    py_modules=[
        'image_system',
    ],
    data_files=[
        ('lib/' + package_name, ['package.xml']),
        ('lib/' + package_name + '/cascades', glob('./cascades/*')),
        ('lib/' + package_name + '/modules', glob('./modules/*'))
    ],
    install_requires=['setuptools'],
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
    description='image syste is made using ROS2',
    license='Apache License, Version 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'image_system=image_system:main'
        ],
    },
)
