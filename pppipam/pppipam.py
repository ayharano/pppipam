#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""PPPIPAM main module."""

import pppipam.helpers as helpers


class AddressSpace:
    def describe(self, *, ip_parameter, description):
        if isinstance(ip_parameter, int):
            raise TypeError("ip_parameter must not be int")
        as_address = helpers.clean_address(ip_parameter)
        as_network = helpers.clean_network(ip_parameter)
        if not as_address and not as_network:
            raise TypeError("ip_parameter must be a valid IP parameter")
        if description == "":
            raise ValueError("No empty description allowed")
        if not isinstance(description, str):
            raise TypeError("description must be str")
        return True
