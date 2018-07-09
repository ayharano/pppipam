#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module with helper functions."""

import ipaddress


def clean_address(address_parameter):
    value = None
    try:
        value = ipaddress.IPv6Address(address_parameter)
    except ipaddress.AddressValueError:
        try:
            value = ipaddress.IPv4Address(address_parameter)
        except ipaddress.AddressValueError:
            pass
    if value:
        return value
    return value
