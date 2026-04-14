"""Hermes plugin entrypoint for hermes-lark."""

from hermes_lark.registration import register_plugin


def register(ctx):
    """Hermes plugin hook."""
    register_plugin(ctx)
