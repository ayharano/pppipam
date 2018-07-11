#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""PPPIPAM main module."""

class AddressSpace:
    def describe(self, *, ip_parameter, description):
        if not description:
            raise TypeError("description must be str")
        if description == "":
            raise ValueError("No empty description allowed")
        return True
