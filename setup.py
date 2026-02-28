from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="semopy",
    version="2.3.11",
    author="Georgy Meshcheryakov",
    author_email="iam@georgy.top",
    description="Structural Equation Modeling Optimization in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://semopy.com",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "": [
            "examples/*.csv",
            "examples/*.npy",
            "examples/*.txt",
            "report/*.html",
            "report/*.txt",
            "report/css/*.css",
            "report/js/*.js",
        ]
    },

    # Proper dependency specification
    install_requires=[
        "numpy>=1.23",
        "scipy>=1.9",
        "pandas>=1.5",
        "sympy>=1.10",
        "scikit-learn>=1.2",
        "statsmodels>=0.13",
        "numdifftools>=0.9",
    ],

    python_requires=">=3.9",

    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Scientific/Engineering",
        "Operating System :: OS Independent",
    ],
)

