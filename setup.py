from setuptools import setup, find_packages

if __name__ == "__main__":  # Ensure setup.py code only runs when executed directly
  setup(
    name='valdata',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
      'pandas>=1.5.2',
      'numpy>=1.22.4',
      'pyspark>=3.1.1',
      'pytz>=2024.1',
      'tabulate>=0.9.0',
      'IPython>=8.18.1',
    ],
    description='A Python package for validating data consistency',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='GabrielGod1',
    author_email='altGeneric@hotmail.com',
    url="https://github.com/GabrielGod1/valdata",
    python_requires='>=3.6',
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
  )