#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module with helper functions."""

import ipaddress


def clean_address(address_parameter):
    try:
        value = ipaddress.IPv4Address(address_parameter)
    except ipaddress.AddressValueError:
        return None
    return value
