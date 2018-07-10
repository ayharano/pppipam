#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""PPPIPAM main module."""

class AddressSpace:
    def describe(self, *, address, description):
        if description == "":
            raise ValueError("No empty description allowed")
        return True
