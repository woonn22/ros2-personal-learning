from setuptools import find_packages, setup

package_name = 'robot_basics'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ww',
    maintainer_email='ww@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
	    'robot_node = robot_basics.robot_node:main',
	    'monitor_node = robot_basics.monitor_node:main',
        'service_node = robot_basics.service_node:main',
        'client_node = robot_basics.client_node:main',
        ],
    },
)
