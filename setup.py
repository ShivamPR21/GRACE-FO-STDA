# Copyright 2020 Shivam Pandey
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="grace_fo_stda",
    version="0.0.1",
    author="Shivam Pandey",
    author_email="pandeyshivam2017robotics@gmail.com",
    description="Package to read and preprocess the GRACE and GRACE-FO temporal data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/ShivamPR21/grace-fo-stda.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License, Version 2.0",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
