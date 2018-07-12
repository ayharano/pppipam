#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""PPPIPAM main module."""

import ipaddress

import pppipam.helpers as helpers


IPAddressTuple = tuple([ipaddress.IPv4Address, ipaddress.IPv6Address])
IPNetworkTuple = tuple([ipaddress.IPv4Network, ipaddress.IPv6Network])


class AddressSpace:
    """IP addresses and networks description manager."""

    def __init__(self):
        """Initialize private attributes."""
        self.__description = dict()
        self.__networks = dict()
        self.__addresses = dict()

    def describe(self, *, ip_parameter, description):
        """Insert an IP address or network with a description.

        Args:
            ip_parameter: value to be processed as an IP address or
                          an IP network.
            description: non-empty str to describe IP address or
                         IP network.

        Returns:
            bool if successfully described.

        Raises:
            TypeError: parameters not of expected type.
            ValueError: invalid description value.
        """

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
        """Retrieve a description of an IP address or IP network.

        Args:
            ip_parameter: value to be processed as an IP address or
                          an IP network.

        Returns:
            Non-empty str if matches a described IP object;
            empty str if matches an address or subnet of
            a described IP Network; or
            None if IP object does not belong in address space.

        Raises:
            TypeError: parameters not of expected type.
        """

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
