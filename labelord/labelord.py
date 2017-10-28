import click

from .cli import cli
from .web import app

def main():
    cli(obj={})
