#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""PPPIPAM main module."""

from dataclasses import dataclass, field, InitVar
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


class StrictSupernetError(Exception):
    """Error related to supernet missing or present."""
    pass


class SameDelegationAsNewError(Exception):
    """Attempt to insert already existing delegated network."""
    pass


@dataclass(init=False)
class AddressSpace:
    """IP addresses and networks description manager."""

    __strict: bool
    __description: typing.Dict[IPObject, str]
    __networks: typing.Dict[int, typing.Set[IPNetwork]]
    __addresses: typing.Dict[int, typing.Set[IPAddress]]
    strict: InitVar[bool] = True

    def __init__(self, *, strict: bool = True) -> None:
        """Handles init-only var into private var."""
        self.__strict = bool(strict)
        self.__description = dict()
        self.__networks = dict()
        self.__addresses = dict()

    def __get_supernet(self, cleaned_ip_object):

        version = cleaned_ip_object.version

        if version not in self.__networks:
            return None

        if isinstance(cleaned_ip_object, IPAddressTuple):
            for tentative_supernet in self.__networks[version]:
                if cleaned_ip_object in tentative_supernet:
                    return tentative_supernet

        if isinstance(cleaned_ip_object, IPNetworkTuple):
            for tentative_supernet in self.__networks[version]:
                if cleaned_ip_object == tentative_supernet:
                    continue
                if cleaned_ip_object.subnet_of(tentative_supernet):
                    return tentative_supernet

    @property
    def strict(self) -> bool:
        """Returns strict value."""
        return bool(self.__strict)

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
            >>> as_ = AddressSpace(strict=False)
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
            if self.__strict and self.__get_supernet(as_address) is None:
                raise StrictSupernetError()
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

    def describe_new_delegated_network(
        self, *, network_parameter, description
    ):
        if isinstance(network_parameter, int):
            raise TypeError("network_parameter must not be int")

        as_network = clean_network(network_parameter)

        if isinstance(as_network, IPNetworkTuple):
            if self.__get_supernet(as_network) is not None:
                raise StrictSupernetError()
            if as_network in self.__description:
                raise SameDelegationAsNewError()
        else:
            raise TypeError("network_parameter must be "
                            "a valid IP network parameter")

        return self.describe(
            ip_parameter=as_network,
            description=description
        )

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
            >>> as_ = AddressSpace(strict=False)
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
