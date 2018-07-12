#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""PPPIPAM main module."""

from dataclasses import dataclass, field
import ipaddress
import typing

from pppipam.helpers import (
    IPAddressParameter,
    IPNetworkParameter,
    IPAddress,
    IPNetwork,
    clean_address,
    clean_network,
)


IPParameter = typing.Union[IPAddressParameter, IPNetworkParameter]
IPObject = typing.Union[IPAddress, IPNetwork]
IPAddressTuple = tuple([ipaddress.IPv4Address, ipaddress.IPv6Address])
IPNetworkTuple = tuple([ipaddress.IPv4Network, ipaddress.IPv6Network])


@dataclass
class AddressSpace:
    """IP addresses and networks description manager."""

    strict: bool = False
    __description: typing.Dict[IPObject, str] = field(default_factory=dict)
    __networks: typing.Dict[int, typing.Set[IPNetwork]] = field(
        default_factory=dict
    )
    __addresses: typing.Dict[int, typing.Set[IPAddress]] = field(
        default_factory=dict
    )

    def describe(self, *, ip_parameter: IPParameter, description: str) -> bool:
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

        doctest example:
            >>> as_ = AddressSpace()
            >>> as_.describe(description='Famous IPv4 loopback address',
            ...              ip_parameter='127.0.0.1')
            True
            >>> as_.describe(
            ...    description='Not so famous IPv6 loopback address',
            ...    ip_parameter='::1')
            True
            >>> as_.describe(ip_parameter="0.0.0.0/0",
            ...              description="all IPv4 network")
            True
            >>> as_.describe(description="all IPv6 network",
            ...              ip_parameter="::/0")
            True
            >>> as_.describe(description="", ip_parameter="::1")
            Traceback (most recent call last):
                ...
            ValueError: No empty description allowed
            >>> as_.describe(description="valid description",
            ...              ip_parameter="invalid IP parameter")
            Traceback (most recent call last):
                ...
            TypeError: ip_parameter must be a valid IP parameter
            >>> as_.describe(description="int IP parameter",
            ...              ip_parameter=123)
            Traceback (most recent call last):
                ...
            TypeError: ip_parameter must not be int
            >>>
        """

        if description == "":
            raise ValueError("No empty description allowed")
        if not isinstance(description, str):
            raise TypeError("description must be str")
        if isinstance(ip_parameter, int):
            raise TypeError("ip_parameter must not be int")

        as_address = clean_address(ip_parameter)
        as_network = clean_network(ip_parameter)

        described = False

        if isinstance(as_address, IPAddressTuple):
            version_set = self.__addresses.setdefault(
                as_address.version, set()
            )
            version_set.add(as_address)
            self.__description[as_address] = description
            described = True
        elif isinstance(as_network, IPNetworkTuple):
            version_set = self.__networks.setdefault(as_network.version, set())
            version_set.add(as_network)
            self.__description[as_network] = description
            described = True
        else:
            raise TypeError("ip_parameter must be a valid IP parameter")

        return described

    def description(self, ip_parameter: IPParameter) -> typing.Optional[str]:
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

        doctest example:
            >>> as_ = AddressSpace()
            >>> as_.describe(
            ...     description='An IPv6 documentation network',
            ...     ip_parameter='2001:db8:abcd::/48')
            True
            >>> as_.describe(description='An IPv6 address in doc net',
            ...              ip_parameter='2001:db8:abcd::1234')
            True
            >>> as_.describe(ip_parameter='198.51.100.0/24',
            ...              description="TEST-NET-2 (RFC5735)")
            True
            >>> as_.describe(description="An address in test net",
            ...              ip_parameter="198.51.100.123")
            True
            >>> as_.description("2001:db8:abcd::/48")
            'An IPv6 documentation network'
            >>> as_.description("2001:db8:abcd::1234")
            'An IPv6 address in doc net'
            >>> as_.description("2001:db8:abcd::98:7654:3210")
            ''
            >>> as_.description("2001:db8:abcd::/64")
            ''
            >>> as_.description("2001:db8:1234::/48")
            >>> as_.description("fe80::")
            >>> as_.description("198.51.100.0/24")
            'TEST-NET-2 (RFC5735)'
            >>> as_.description("198.51.100.123")
            'An address in test net'
            >>> as_.description("198.51.100.100")
            ''
            >>> as_.description("198.51.100.128/25")
            ''
            >>> as_.description("198.51.99.0")
            >>> as_.description("198.51.123.0/24")
            >>> as_.description(None)
            Traceback (most recent call last):
                ...
            TypeError: ip_parameter must be a valid IP parameter
            >>> as_.description('abc')
            Traceback (most recent call last):
                ...
            TypeError: ip_parameter must be a valid IP parameter
            >>> as_.description(123)
            Traceback (most recent call last):
                ...
            TypeError: ip_parameter must not be int
            >>>
        """

        if isinstance(ip_parameter, int):
            raise TypeError("ip_parameter must not be int")

        as_address = clean_address(ip_parameter)
        as_network = clean_network(ip_parameter)

        if not isinstance(as_address, IPAddressTuple) and not isinstance(
            as_network, IPNetworkTuple
        ):
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
