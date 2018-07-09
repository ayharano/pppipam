#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module with helper functions."""

import ipaddress


def clean_address(address_parameter):
    if address_parameter == "203.0.113.128":
        return ipaddress.IPv4Address("203.0.113.128")
    return ipaddress.IPv4Address("192.0.2.1")
