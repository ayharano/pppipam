#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""PPPIPAM main module."""

class AddressSpace:
    def describe(self, *, ip_parameter, description):
        if not ip_parameter:
            raise TypeError("ip_parameter must be a valid IP parameter")
        if description == "":
            raise ValueError("No empty description allowed")
        if not isinstance(description, str):
            raise TypeError("description must be str")
        return True
