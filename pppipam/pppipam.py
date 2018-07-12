#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""PPPIPAM main module."""

import ipaddress

import pppipam.helpers as helpers


IPAddressTuple = tuple([ipaddress.IPv4Address, ipaddress.IPv6Address])
IPNetworkTuple = tuple([ipaddress.IPv4Network, ipaddress.IPv6Network])


class AddressSpace:

    def __init__(self):
        self.__description = dict()
        self.__networks = dict()
        self.__addresses = dict()

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

        if isinstance(as_address, IPAddressTuple):
            version_set = (
                self.__addresses.setdefault(as_address.version, set())
            )
            version_set.add(as_address)
            self.__description[as_address] = description
            described = True
        elif isinstance(as_network, IPNetworkTuple):
            version_set = (
                self.__networks.setdefault(as_network.version, set())
            )
            version_set.add(as_network)
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

        if (not isinstance(as_address, IPAddressTuple)
                and not isinstance(as_network, IPNetworkTuple)):
            raise TypeError("ip_parameter must be a valid IP parameter")

        if as_address in self.__description:
            return self.__description[as_address]
        elif as_network in self.__description:
            return self.__description[as_network]

        if isinstance(as_address, IPAddressTuple):
            if as_address.version in self.__networks:
                for tentative_net in self.__networks[as_address.version]:
                    if as_address in tentative_net:
                        return str("")

        if isinstance(as_network, IPNetworkTuple):
            if as_network.version in self.__networks:
                for tentative_net in self.__networks[as_network.version]:
                    if as_network.subnet_of(tentative_net):
                        return str("")
