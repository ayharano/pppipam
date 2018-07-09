#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module with helper functions."""

import ipaddress


def clean_address(address_parameter):
    value = None
    try:
        value = ipaddress.ip_address(address_parameter)
    except ipaddress.AddressValueError:
        pass
    return value
