#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""PPPIPAM main module."""

import ipaddress
import typing
from dataclasses import dataclass, InitVar

from . import helpers


IPParameter = typing.Union[helpers.IPAddressParameter, helpers.IPNetworkParameter]
IPObject = typing.Union[helpers.IPAddress, helpers.IPNetwork]
IPAddressTuple = tuple([ipaddress.IPv4Address, ipaddress.IPv6Address])
IPNetworkTuple = tuple([ipaddress.IPv4Network, ipaddress.IPv6Network])


class StrictSupernetError(Exception):
    """Error related to supernet missing or present."""
    pass


class SameDelegationAsNewError(Exception):
    """Attempt to insert already existing delegated network."""
    pass


class IPObjectNotInSpaceError(Exception):
    """Error due to IP object not in space and should be treated."""
    pass


@dataclass(init=False)
class AddressSpace:
    """IP addresses and networks description manager."""

    __strict: bool
    __description: typing.Dict[IPObject, str]
    __networks: typing.Dict[int, typing.Set[helpers.IPNetwork]]
    __addresses: typing.Dict[int, typing.Set[helpers.IPAddress]]
    __parent_supernet: typing.Dict[IPObject, helpers.IPNetwork]
    __children_ip_object: typing.Dict[
        typing.Optional[helpers.IPNetwork], typing.Set[IPObject]
    ]
    strict_: InitVar[bool] = True

    def __init__(self, *, strict_: bool = True) -> None:
        """Handles init-only var into private var.

        Args:
            strict_: if evaluated to True, stricts address space
                     handling by only permitting descriptions if
                     previous delegated networks are inserted.
        """
        self.__strict = bool(strict_)
        self.__description = dict()
        self.__networks = dict()
        self.__addresses = dict()
        self.__parent_supernet = dict()
        self.__children_ip_object = dict()

        # None is address space top supernet parent.
        self.__children_ip_object[None] = set()

    def __get_supernet(
        self, cleaned_ip_object: IPObject
    ) -> typing.Optional[helpers.IPNetwork]:
        """Retrieves the smallest supernet of IP object, if described.

        Args:
            cleaned_ip_object: IP object to be verified.

        Returns:
            An IP network object with the largest prefix length
            if a supernet exists or None, otherwise.

        Raises:
            AttribureError: if parameter is not an IP object.
        """

        version = cleaned_ip_object.version

        if version not in self.__networks:
            return None

        current_tentative = None
        current_prefixlen = None

        if isinstance(cleaned_ip_object, IPAddressTuple):
            for tentative_supernet in self.__networks[version]:
                if cleaned_ip_object in tentative_supernet:
                    if (current_prefixlen is None or
                            tentative_supernet.prefixlen > current_prefixlen):
                        current_tentative = tentative_supernet
                        current_prefixlen = tentative_supernet.prefixlen

        if isinstance(cleaned_ip_object, IPNetworkTuple):
            for tentative_supernet in self.__networks[version]:
                if cleaned_ip_object == tentative_supernet:
                    continue
                if cleaned_ip_object.subnet_of(tentative_supernet):
                    if (current_prefixlen is None or
                            tentative_supernet.prefixlen > current_prefixlen):
                        current_tentative = tentative_supernet
                        current_prefixlen = tentative_supernet.prefixlen

        return current_tentative

    def __remove_ip_object(self, ip_object: IPObject) -> bool:
        """Adjust private variables to remove an IP object.

        Args:
            ip_object: IP object registered in address space.

        Returns:
            bool if successfully removed.

        Raises:
            TypeError: parameters not of expected type.
        """

        if ip_object not in self.__description:
            raise IPObjectNotInSpaceError(
                "cannot remove undescribed IP object"
            )

        if isinstance(ip_object, IPAddressTuple):

            supernet = self.__parent_supernet[ip_object]
            self.__children_ip_object[supernet].remove(ip_object)
            del self.__parent_supernet[ip_object]
            del self.__description[ip_object]
            self.__addresses[ip_object.version].remove(ip_object)
            if not self.__addresses[ip_object.version]:
                del self.__addresses[ip_object.version]

        elif isinstance(ip_object, IPNetworkTuple):

            supernet = self.__parent_supernet[ip_object]
            children_of_supernet = (
                self.__children_ip_object.setdefault(supernet, set())
            )

            for child in self.__children_ip_object[ip_object]:
                self.__parent_supernet[child] = supernet
                children_of_supernet.add(child)

            self.__children_ip_object[supernet].remove(ip_object)
            del self.__children_ip_object[ip_object]
            del self.__parent_supernet[ip_object]
            del self.__description[ip_object]
            self.__networks[ip_object.version].remove(ip_object)
            if not self.__networks[ip_object.version]:
                del self.__networks[ip_object.version]

        else:

            raise TypeError("ip_parameter must be a valid IP object")

        return True

    def __cascading_remove_ip_network(
        self, ip_network_object: helpers.IPNetwork
    ) -> bool:
        """Recursively removes children IP objects and itself.

        Args:
            ip_network_object: IP Network object registered in
                               address space.

        Returns:
            bool if successfully removed.

        Raises:
            TypeError: parameters not of expected type.
        """

        children = list(self.__children_ip_object[ip_network_object])

        for child in children:
            if child not in self.__description:
                continue

            if isinstance(child, IPAddressTuple):
                self.__remove_ip_object(child)
            elif isinstance(child, IPNetworkTuple):
                self.__cascading_remove_ip_network(child)
            else:
                raise TypeError("child must be a valid IP object")

        return self.__remove_ip_object(ip_network_object)

    @property
    def strict(self) -> bool:
        """Returns strict value."""
        return bool(self.__strict)

    def describe(
        self,
        *,
        ip_parameter: IPParameter,
        description: str,
        is_new_delegated_net: bool = False,
    ) -> bool:
        """Insert an IP address or network with a description.

        Args:
            ip_parameter: value to be processed as an IP address or
                          an IP network.
            description: non-empty str to describe IP address or
                         IP network.
            is_new_delegated_net: if evaluates to True, will be used to
                                  check if it must be treated as a new
                                  network delegation.

        Returns:
            bool if successfully described.

        Raises:
            TypeError: parameters not of expected type.
            ValueError: invalid description value.

        doctest example:
            >>> as_ = AddressSpace(strict_=False)
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
            >>> sas = AddressSpace(strict_=True)
            >>> sas.describe(description="address without supernet",
            ...              ip_parameter="10.98.76.54")
            Traceback (most recent call last):
                ...
            pppipam.pppipam.StrictSupernetError: supernet not found
            >>> sas.describe(description="network without supernet",
            ...              ip_parameter="2001:db8:abcd::/48")
            Traceback (most recent call last):
                ...
            pppipam.pppipam.StrictSupernetError: supernet not found
            >>> sas.describe_new_delegated_network(
            ...     network_parameter="2000::/3",
            ...     description="current global IPv6 network")
            True
            >>> sas.describe_new_delegated_network(
            ...     network_parameter="127.0.0.0/8",
            ...     description="IPv4 loopback network")
            True
            >>> sas.describe(description="IPv6 doc net part of global",
            ...              ip_parameter="2001:db8::/32")
            True
            >>> sas.describe(ip_parameter='127.0.0.1',
            ...              description='I have seen this in a t-shirt')
            True
            >>>
        """

        if description == "":
            raise ValueError("No empty description allowed")
        if not isinstance(description, str):
            raise TypeError("description must be str")
        if isinstance(ip_parameter, int):
            raise TypeError("ip_parameter must not be int")

        is_new_delegated_net = bool(is_new_delegated_net)

        as_address = helpers.clean_address(ip_parameter)
        as_network = helpers.clean_network(ip_parameter)

        described = False

        if isinstance(as_address, IPAddressTuple):
            if is_new_delegated_net:
                raise ValueError(
                    "is_new_delegated_net was set with address parameter"
                )

            supernet = self.__get_supernet(as_address)
            if self.__strict and supernet is None:
                raise StrictSupernetError("supernet not found")

            version_set = self.__addresses.setdefault(
                as_address.version, set()
            )
            version_set.add(as_address)
            self.__description[as_address] = description
            described = True

            self.__parent_supernet[as_address] = supernet
            children_of_supernet = (
                self.__children_ip_object.setdefault(supernet, set())
            )
            children_of_supernet.add(as_address)
        elif isinstance(as_network, IPNetworkTuple):
            supernet = self.__get_supernet(as_network)
            if is_new_delegated_net and supernet is not None:
                raise ValueError(
                    "Invalid combination of existing supernet "
                    "and new delegated network"
                )
            if (
                self.__strict and supernet is None and not is_new_delegated_net
            ):
                raise StrictSupernetError("supernet not found")


            version_set = self.__networks.setdefault(as_network.version, set())
            version_set.add(as_network)
            self.__description[as_network] = description
            described = True

            self.__parent_supernet[as_network] = supernet
            children_of_as_network = (
                self.__children_ip_object.setdefault(as_network, set())
            )
            children_of_supernet = (
                self.__children_ip_object.setdefault(supernet, set())
            )
            # Supernet's child can be as_network's child
            version = as_network.version
            to_arrange = set()
            for tentative_child in children_of_supernet:
                if (isinstance(tentative_child, IPAddressTuple)
                        and tentative_child.version == version
                        and tentative_child in as_network):
                    to_arrange.add(tentative_child)
                elif (isinstance(tentative_child, IPNetworkTuple)
                        and tentative_child.version == version
                        and tentative_child.subnet_of(as_network)):
                    to_arrange.add(tentative_child)
            for child in to_arrange:
                self.__parent_supernet[child] = as_network
                children_of_as_network.add(child)
                children_of_supernet.remove(child)
            children_of_supernet.add(as_network)
        else:
            raise TypeError("ip_parameter must be a valid IP parameter")

        return described

    def describe_new_delegated_network(
        self, *, network_parameter: helpers.IPNetworkParameter, description: str
    ) -> bool:
        """Describe a new delegated network, if possible.

        Args:
            network_parameter: value to be processed as an IP network.
            description: non-empty str to describe IP network.

        Returns:
            bool if successfully described.

        Raises:
            TypeError: parameters not of expected type.
            ValueError: invalid description value.
            StrictSupernetError: a supernet of network parameter
                                 already exists.
            SameDelegationAsNewError: trying to insert a network
                                      as new when already present.

        doctest example:
            >>> as_ = AddressSpace(strict_=False)
            >>> as_.describe(ip_parameter="127.127.127.127",
            ...              description="a IPv4 loopback address")
            True
            >>> as_.describe_new_delegated_network(
            ...     network_parameter="127.127.127.127/32",
            ...     description="same address, as a network")
            True
            >>> as_.describe(ip_parameter="10.10.0.0/16",
            ...              description="a private new")
            True
            >>> as_.describe_new_delegated_network(
            ...     description="describing a network without supernet "
            ...                 "is the same as inserting a delegated net "
            ...                 "even if strict is False",
            ...     network_parameter="10.10.0.0/16")
            Traceback (most recent call last):
                ...
            pppipam.pppipam.SameDelegationAsNewError: already described
            >>> as_.describe_new_delegated_network(
            ...     network_parameter="10.0.0.0/8",
            ...     description="supernet is fine")
            True
            >>> as_.describe_new_delegated_network(
            ...     network_parameter="10.0.0.0/12",
            ...     description="no subnet, even in non strict")
            Traceback (most recent call last):
                ...
            pppipam.pppipam.StrictSupernetError: supernet already described
            >>> sas = AddressSpace(strict_=True)
            >>> sas.describe(ip_parameter="2001:db8::/48",
            ...              description="must delegate first in strict")
            Traceback (most recent call last):
                ...
            pppipam.pppipam.StrictSupernetError: supernet not found
            >>> sas.describe(ip_parameter="2001:db8::",
            ...              description="of course for address too")
            Traceback (most recent call last):
                ...
            pppipam.pppipam.StrictSupernetError: supernet not found
            >>> sas.describe_new_delegated_network(
            ...     network_parameter="2001:db8:abcd::",
            ...     description="but not an address")
            Traceback (most recent call last):
                ...
            ValueError: No address as parameter allowed
            >>> sas.describe_new_delegated_network(
            ...     network_parameter="2001:db8:abcd::/48",
            ...     description="now it's a go, at least for ipv6")
            True
            >>> sas.describe_new_delegated_network(
            ...     network_parameter="127.127.0.0/16",
            ...     description="and ipv4 also")
            True
            >>> sas.describe_new_delegated_network(
            ...     network_parameter="2001:db8:abcd::/48",
            ...     description="but not more than once")
            Traceback (most recent call last):
                ...
            pppipam.pppipam.SameDelegationAsNewError: already described
            >>>
        """

        if isinstance(network_parameter, int):
            raise TypeError("network_parameter must not be int")

        as_address = helpers.clean_address(network_parameter)
        as_network = helpers.clean_network(network_parameter)

        if isinstance(as_address, IPAddressTuple):
            raise ValueError("No address as parameter allowed")

        if isinstance(as_network, IPNetworkTuple):
            if self.__get_supernet(as_network) is not None:
                raise StrictSupernetError("supernet already described")
            if as_network in self.__description:
                raise SameDelegationAsNewError("already described")
        else:
            raise TypeError("network_parameter must be "
                            "a valid IP network parameter")

        return self.describe(
            ip_parameter=as_network,
            description=description,
            is_new_delegated_net=True,
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
            >>> as_ = AddressSpace(strict_=False)
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
            >>> sas = AddressSpace(strict_=True)
            >>> sas.describe_new_delegated_network(
            ...     description='An IPv6 documentation network',
            ...     network_parameter='2001:db8:abcd::/48')
            True
            >>> sas.describe(description='An IPv6 address in doc net',
            ...              ip_parameter='2001:db8:abcd::1234')
            True
            >>> sas.describe_new_delegated_network(
            ...     network_parameter='198.51.100.0/24',
            ...     description="TEST-NET-2 (RFC5735)")
            True
            >>> sas.describe(description="An address in test net",
            ...              ip_parameter="198.51.100.123")
            True
            >>> sas.description("2001:db8:abcd::/48")
            'An IPv6 documentation network'
            >>> sas.description("2001:db8:abcd::1234")
            'An IPv6 address in doc net'
            >>> sas.description("2001:db8:abcd::98:7654:3210")
            ''
            >>> sas.description("2001:db8:abcd::/64")
            ''
            >>> sas.description("2001:db8:1234::/48")
            >>> sas.description("fe80::")
            >>> sas.description("198.51.100.0/24")
            'TEST-NET-2 (RFC5735)'
            >>> sas.description("198.51.100.123")
            'An address in test net'
            >>> sas.description("198.51.100.100")
            ''
            >>> sas.description("198.51.100.128/25")
            ''
            >>> sas.description("198.51.99.0")
            >>> sas.description("198.51.123.0/24")
            >>>
        """

        if isinstance(ip_parameter, int):
            raise TypeError("ip_parameter must not be int")

        as_address = helpers.clean_address(ip_parameter)
        as_network = helpers.clean_network(ip_parameter)

        if not isinstance(as_address, IPAddressTuple) and not isinstance(
            as_network, IPNetworkTuple
        ):
            raise TypeError("ip_parameter must be a valid IP parameter")


        if isinstance(as_address, IPAddressTuple):
            if as_address in self.__description:
                return self.__description[as_address]

            supernet = self.__get_supernet(as_address)
            if supernet is not None:
                return str("")

        if isinstance(as_network, IPNetworkTuple):
            if as_network in self.__description:
                return self.__description[as_network]

            supernet = self.__get_supernet(as_network)
            if supernet is not None:
                return str("")

        return None

    def delete(self, *, ip_parameter: IPParameter, cascade: bool) -> bool:
        """Delete only described IP object and optionally its children.

        Args:
            ip_parameter: value to be processed as an IP address or
                          an IP network.
            cascade: if evaluated as True, deletes children IP objects.

        Returns:
            bool if successfully removed.

        Raises:
            TypeError: parameters not of expected type.
            IPObjectNotInSpaceError: if a tentative IP object is
                                     not registered.
        """

        as_address = helpers.clean_address(ip_parameter)
        as_network = helpers.clean_network(ip_parameter)

        if as_address in self.__description:
            return self.__remove_ip_object(as_address)
        elif as_network in self.__description:
            if cascade:
                return self.__cascading_remove_ip_network(as_network)
            else:
                return self.__remove_ip_object(as_network)

        raise IPObjectNotInSpaceError("cannot delete undescribed IP object")

    def __gather_nested_children(
       self, ip_object: IPObject
    ) -> typing.Dict[IPObject, dict]:
        """Retrieves nested children of an IP object.

        If parameter is an address, there is no child.
        If parameter is a network, recursively calculates children's
        nested children.

        Args:
            ip_object: IP object registered in address space.

        Returns:
            dict instance with nested children's dicts.

        Raises:
            TypeError: parameters not of expected type.
            ValueError: children set not defined.
        """

        nested_dict = dict()

        if isinstance(ip_object, IPAddressTuple):

            pass

        elif isinstance(ip_object, IPNetworkTuple):

            if ip_object not in self.__children_ip_object:
                raise ValueError("Network value should have children set")

            for child in self.__children_ip_object[ip_object]:
                nested_dict[child] = self.__gather_nested_children(child)

        else:
            raise TypeError(f"unexpected parameter type: {type(ip_object)}")

        return nested_dict


    def export_data(self) -> typing.Dict[str, dict]:
        """Exports data as dict.

        Returns:
            dict composed by a dict of IP objects' descriptions and
            a dict of nested IP objects according to
            available IP objects' version.
        """

        nested_ip_objects = dict()

        if self.__children_ip_object and None in self.__children_ip_object:
            children_per_version = dict()
            for child in self.__children_ip_object[None]:
                version_set = children_per_version.setdefault(
                    child.version, set()
                )
                version_set.add(child)

            for version in children_per_version:
                version_nest = nested_ip_objects.setdefault(version, dict())
                for child in children_per_version[version]:
                    version_nest[child] = self.__gather_nested_children(child)

        return dict({
            "description": dict(self.__description),
            "nested_ip_objects": nested_ip_objects,
        })
