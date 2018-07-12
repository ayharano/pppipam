#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""PPPIPAM main module."""

import ipaddress

import pppipam.helpers as helpers


class AddressSpace:

    def __init__(self):
        self.__description = dict()

    def describe(self, *, ip_parameter, description):

        if description == "":
            raise ValueError("No empty description allowed")
        if not isinstance(description, str):
            raise TypeError("description must be str")
        if isinstance(ip_parameter, int):
            raise TypeError("ip_parameter must not be int")

        as_address = helpers.clean_address(ip_parameter)
        as_network = helpers.clean_network(ip_parameter)

        described = False

        if isinstance(
            as_address,
            (ipaddress.IPv4Address, ipaddress.IPv6Address),
        ):
            self.__description[as_address] = description
            described = True
        elif isinstance(
            as_network,
            (ipaddress.IPv4Network, ipaddress.IPv6Network),
        ):
            self.__description[as_network] = description
            described = True
        else:
            raise TypeError("ip_parameter must be a valid IP parameter")

        return described

    def description(self, ip_parameter):
        if isinstance(ip_parameter, int):
            raise TypeError("ip_parameter must not be int")

        as_address = helpers.clean_address(ip_parameter)
        as_network = helpers.clean_network(ip_parameter)

        if not isinstance(
            as_address,
            (ipaddress.IPv4Address, ipaddress.IPv6Address),
        ) and not isinstance(
            as_network,
            (ipaddress.IPv4Network, ipaddress.IPv6Network),
        ):
            raise TypeError("ip_parameter must be a valid IP parameter")

        if as_address in self.__description:
            return self.__description[as_address]
        elif as_network in self.__description:
            return self.__description[as_network]

        # if ip_parameter == "0.0.0.0":
        #     return "address 0 for ipv4"
        # if ip_parameter == "2001:db8::2018:7:12":
        #     return "hey! an IPv6 Address"
        # return "should be the same"
