from setuptools import setup, find_packages

setup(
    name="custom_exception_python",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["requests"],
    author="Gosha",
    author_email="lyhtyrageorgiu@gmail.com",
    description="Custom error monitoring SDK like Sentry",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Gooooosha/custom_exception_python#",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
