#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module with helper functions."""

import ipaddress


def clean_address(address_parameter):
    return ipaddress.IPv4Address("192.0.2.1")
