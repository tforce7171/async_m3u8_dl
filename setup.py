import setuptools

requires = [
    "m3u8",
    "async_requests @ git+https://github.com/tforce7171/async_requests.git"
]

setuptools.setup(
    name="async-m3u8-dl",
    version="0.1.0",
    author="tforce7171",
    author_email="taiseimaruyama7171@gmail.com",
    description="asyncronusly download files according to m3u8 data",
    url="https://github.com/tforce7171/async-m3u8-dl.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=requires
)