from setuptools import setup

package_name = 'vr_JekkoController'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Görkem Can Ertemli',
    maintainer_email='goerkem.can.ertemli@rwth-aachen.de',
    description='ROS 2 package for controlling the Jekko',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'vr_controller = vr_JekkoController.vr_JekkoController:main',
        ],
    },
)
