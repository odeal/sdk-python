from setuptools import setup, find_packages

setup(
    name='odeal-sdk',
    version='0.1.6',
    description='Odeal Entegrasyon SDK (Otomatik Üretildi)',
    author='Odeal',
    author_email='',
    url='https://github.com/odeal/sdk',
    license='MIT',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'requests>=2.31.0',
    ],
    python_requires='>=3.8',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
