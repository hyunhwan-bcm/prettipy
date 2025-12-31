"""
Prettipy - Beautiful Python Code to PDF Converter

A Python package that converts Python source code into beautifully formatted,
syntax-highlighted PDF documents.
"""

__version__ = "0.2.1"
__author__ = "Hyun-Hwan Jeong"
__email__ = "hyun-hwan.jeong@bcm.edu"

from .core import PrettipyConverter
from .config import PrettipyConfig

__all__ = ["PrettipyConverter", "PrettipyConfig"]
