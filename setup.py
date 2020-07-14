from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Education',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8'
]

setup(
    name='localchat',
    version='1.0.1',
    description='Group Chat on a Local Area Network',
    long_description=open('README.txt').read() + '\n',
    long_description_content_type="text/markdown",
    url='https://github.com/DeepakJha01/localchat',
    author='Deepak Jha',
    author_email='deepakjha18598@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords=['chat','chatapp','group-chat','localchat','socket','server','client','lan'],
    packages=find_packages(),
    install_requires=[''],
    python_requires='>=3.6'
)
