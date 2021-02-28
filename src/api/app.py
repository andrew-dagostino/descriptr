#!/usr/bin/env python3
import os
from classes.descriptr import Descriptr

""" Change working directory to here """
os.chdir(os.path.dirname(__file__))

if __name__ == "__main__":
    Descriptr()