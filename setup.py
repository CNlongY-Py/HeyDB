import setuptools

with open("README.md", "r",encoding="utf-8") as fh:
  long_description = fh.read()

setuptools.setup(
  name="HeyDB",
  version="0.1.0",
  author="CNlongY",
  author_email="T3464356490@outlook.com",
  description="NoSQL内嵌数据库",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/CNlongY-Py/HeyDB",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)