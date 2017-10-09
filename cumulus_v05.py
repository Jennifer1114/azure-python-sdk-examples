#!/usr/bin/python3
#
# cumulus.py
#
# Modified on 9/18/2017
# by Jennifer Yarboro
#
###############################################################################
# Version 01
# **********
# Modified cumulus.py from
# https://github.com/rafael6/stratus/blob/master/stratus/cumulus.py
#
# Created a main function to test the create, delete, and get functions for
# Virtual Network Operations. Hardcoded the Service Principal and subscription
# credentials for CHQ_DR_Test. Created the delete and get functions for
# virtual networks.
###############################################################################
# Version 02
# **********
#
# Added subnet Network Operation functions to test create_or_update, delete,
# and get.
###############################################################################
# Version 03
# **********
#
# Added route and route table Network Operation functions to test
# create_or_update, delete, and get. Updated the create_update_subnet
# function call parameters to attach route table.
###############################################################################
# Version 04
# **********
#
# Added peerings Network Operation functions to test create_or_update,
# delete, and get.
###############################################################################
# Version 04
# **********
#
# Updated all methods to not include a network_client parameter. Client is now
# global and reassigned in the main function. Storing all credentials and
# sensitive key information in a consumer file.
#
# Added Local Network Gateways Operation functions to test create_or_update,
# delete, and get.
###############################################################################

__author__ = 'rafael'
__version__ = '0.0'

# Compute and network
from azure.common.credentials import ServicePrincipalCredentials
from msrestazure.azure_cloud import AZURE_US_GOV_CLOUD
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient

from msrestazure import azure_exceptions
from msrest.exceptions import AuthenticationError

import json

# Cloud definitions:
# AZURE_PUBLIC_CLOUD
# AZURE_CHINA_CLOUD
# AZURE_US_GOV_CLOUD
# AZURE_GERMAN_CLOUD

'''
Create create_update, delete, and get functions for each networknclass at
https://azure-sdk-for-python.readthedocs.io/en/latest/ref/azure.mgmt.network.v2017_03_01.operations.html
'''

network_client = None
resource_client = None

# Credentials set
CLIENT = ''  # SP
KEY = ''  # SP password
TENANT_ID = ''

# Client set
subscription_id = ''
hub_subscription_id = ''
my_location = ''

# Texas resources set
GROUP_NAME = ''
VNET_NAME = ''
SUBNET_NAME = ''
RT_NAME = ''
ROUTE_NAME = ''


# Virginia resources set
HUB_GROUP_NAME = ''
HUB_VNET_NAME = ''
SPOKE_GROUP_NAME = ''
SPOKE_VNET_NAME = ''

#Subnet resources set
GW_SUBNET_NAME = ''
HUB_SUBNET_NAME_1 = ''
HUB_SUBNET_NAME_2 = ''
HUB_SUBNET_NAME_3 = ''
SPOKE_SUBNET_NAME_1 = ''
SPOKE_SUBNET_NAME_2 = ''
SPOKE_SUBNET_NAME_3 = ''

# Route resources set
HUB_RT_NAME = ''
SPOKE_RT_NAME = ''

# Peerings set
HUB_NAME = ''
SPOKE_NAME = ''

# Resource Group Operations
def create_update_resource_group(
        resource_group_name,
        parameters,
        custom_headers=None,
        raw=False
):
    """
    Creates or updates a resource group.

    :param resource_group_name: (str) – The name of the resource group to
        create or update.
    :param parameters: (ResourceGroup) – Parameters supplied to the create or
        update a resource group.
    :param custom_headers: (dict) – headers that will be added to the request
    :param raw: (bool) – returns the direct response alongside the deserialized
        response
    :return: ResourceGroup or ClientRawResponse if raw=true
    """

    try:
        rg_info = resource_client.resource_groups.create_or_update(
            resource_group_name,
            parameters
        )
        return rg_info.properties.provisioning_state

    except azure_exceptions.CloudError as e:
        print(e)


def get_resource_group(
        resource_group_name,
        custom_headers=None,
        raw=False
):
    """
    Gets a resource group.

    :param resource_group_name: (str) – The name of the resource group to
        create or update.
    :param custom_headers: (dict) – headers that will be added to the request
    :param raw: (bool) – returns the direct response alongside the deserialized
        response
    :return: ResourceGroup or ClientRawResponse if raw=true
    """

    try:
        rg_info = resource_client.resource_groups.get(
            resource_group_name
        )
        return rg_info

    except azure_exceptions.CloudError as e:
        print(e)


def delete_resource_group(
        resource_group_name,
        custom_headers=None,
        raw=False
):
    """
    Deletes a resource group.

    :param resource_group_name: (str) – The name of the resource group to
        delete. The name is case insensitive.
    :param custom_headers: (dict) – headers that will be added to the request
    :param raw: (bool) – returns the direct response alongside the deserialized
        response
    :return: AzureOperationPoller instance that returns None or
        ClientRawResponse if raw=true
    """

    try:
        rg_info = resource_client.resource_groups.delete(
            resource_group_name,
            custom_headers=None,
            raw=False)
        rg_info.wait()

        return rg_info.status()

    except azure_exceptions.CloudError as e:
        return e


# Virtual Networks Operations:
def create_update_vnet(
        resource_group_name,
        virtual_network_name,
        parameters,
        custom_headers=None,
        raw=False
):
    """
    Creates or updates a virtual network in the specified resource group.

    :param network_client: (NetworkManagementClient) - created using Service
        Principal
    :param resource_group_name: (str) – The name of the resource group.
    :param virtual_network_name: (str) – The name of the virtual network.
    :param parameters: (VirtualNetwork) – Parameters supplied to the create or
        update virtual network operation.
    :param custom_headers: (dict) – headers that will be added to the request.
    :param raw: (bool) – returns the direct response alongside the deserialized
        response.
    :return: AzureOperationPoller instance that returns Subnet or
        ClientRawResponse if raw=true
    :raises: CloudError
    """

    try:
        vnet_info = network_client.virtual_networks.create_or_update(
            resource_group_name,
            virtual_network_name,
            parameters,
            custom_headers=None,
            raw=False)
        vnet_info.wait()
        return vnet_info.result().provisioning_state

    except azure_exceptions.CloudError as e:
        return e

def get_vnet(
        resource_group_name,
        virtual_network_name,
        expand=None,
        custom_headers=None,
        raw=False
):
    """
    Gets the specified virtual network by resource group.

    :param network_client: (NetworkManagementClient) - object created using
        Service Principal
    :param resource_group_name: (str) – The name of the resource group.
    :param virtual_network_name: (str) – The name of the virtual network.
    :param expand: (str) – Expands referenced resources.
    :param custom_headers: (dict) – headers that will be added to the request.
    :param raw: (bool) – returns the direct response alongside the deserialized
        response.
    :return: VirtualNetwork or ClientRawResponse if raw=true
    :raises: CloudError
    """
    try:
        vnet_info = network_client.virtual_networks.get(
            resource_group_name,
            virtual_network_name,
            expand=None,
            custom_headers=None,
            raw=False)

        return vnet_info

    except azure_exceptions.CloudError as e:
        return e

def delete_vnet(
        resource_group_name,
        virtual_network_name,
        custom_headers=None,
        raw=False
):
    """
    Deletes the specified virtual network.

    :param network_client: (NetworkManagementClient) - object created using
        Service Principal
    :param resource_group_name: (str) – The name of the resource group.
    :param virtual_network_name: (str) – The name of the virtual network.
    :param custom_headers: (dict) – headers that will be added to the request.
    :param raw: (bool) – returns the direct response alongside the deserialized
        response.
    :return: AzureOperationPoller instance that returns None or
        ClientRawResponse if raw=true
    :raises: CloudError
    """

    try:
        vnet_info = network_client.virtual_networks.delete(
            resource_group_name,
            virtual_network_name,
            custom_headers=None,
            raw=False)

        #do we need the wait?
        vnet_info.wait()
        return vnet_info.status()

    except azure_exceptions.CloudError as e:
        return e


# Subnets Operations:
def create_update_subnet(
        resource_group_name,
        virtual_network_name,
        subnet_name,
        subnet_parameters,
        custom_headers=None,
        raw=False
): 
    """
    Creates or updates a subnet in the specified virtual network.

    :param network_client: (NetworkManagementClient) - object created using
        Service Principal
    :param resource_group_name: (str) – The name of the resource group.
    :param virtual_network_name: (str) – The name of the virtual network
    :param subnet_name: (str) – The name of the subnet.
    :param subnet_parameters: (Subnet) – Parameters supplied to the create
        or update subnet operation.
    :param custom_headers: (dict) – headers that will be added to the request
    :param raw: (bool) – returns the direct response alongside the deserialized
        response
    :return: AzureOperationPoller instance that returns Subnet or
        ClientRawResponse if raw=true
    :raises: CloudError
    """
    try:
        subnet_creation = network_client.subnets.create_or_update(
            resource_group_name,
            virtual_network_name,
            subnet_name,
            subnet_parameters,
            custom_headers=None,
            raw=False
        )
        return subnet_creation.result().provisioning_state

    except azure_exceptions.CloudError as e:
        return e

def get_subnet(
        resource_group_name,
        virtual_network_name,
        subnet_name,
        expand=None,
        custom_headers=None,
        raw=False
):
    """
    Gets the specified subnet by virtual network and resource group.

    :param network_client: (NetworkManagementClient) - object created using
        Service Principal
    :param resource_group_name: (str) – The name of the resource group.
    :param virtual_network_name: (str) – The name of the virtual network
    :param subnet_name: (str) – The name of the subnet.
    :param expand: (str) – Expands referenced resources.
    :param custom_headers: (dict) – headers that will be added to the request
    :param raw: (bool) – returns the direct response alongside the deserialized
        response
    :return: Subnet or ClientRawResponse if raw=true
    :raises: CloudError
    """
    try:
        subnet_info = network_client.subnets.get(
            resource_group_name,
            virtual_network_name,
            subnet_name,
            expand=None,
            custom_headers=None,
            raw=False
        )
        return subnet_info

    except azure_exceptions.CloudError as e:
        return e

def delete_subnet(
        resource_group_name,
        virtual_network_name,
        subnet_name,
        custom_headers=None,
        raw=False
):
    """
    Deletes the specified subnet.

    :param network_client: (NetworkManagementClient) - object created using
        Service Principal
    :param resource_group_name: (str) – The name of the resource group.
    :param virtual_network_name: (str) – The name of the virtual network.
    :param subnet_name: (str) – The name of the subnet.
    :param custom_headers: (dict) – headers that will be added to the request.
    :param raw: (bool) – returns the direct response alongside the deserialized
        response.
    :return: AzureOperationPoller instance that returns Subnet or
        ClientRawResponse if raw=true.
    :raises: CloudError
    """

    try:
        subnet_info = network_client.subnets.delete(
            resource_group_name,
            virtual_network_name,
            subnet_name,
            custom_headers=None,
            raw=False
        )
        subnet_info.wait()
        return subnet_info.status()

    except azure_exceptions.CloudError as e:
        return e

# Route Tables Operations
def create_update_route_table(
        resource_group_name,
        route_table_name,
        parameters,
        custom_headers=None,
        raw=False
):
    """
    Create or updates a route table in a specified resource group.

    :param network_client: (NetworkManagementClient) - object created using
        Service Principal
    :param resource_group_name:  (str) – The name of the resource group
    :param route_table_name: (str) – The name of the route table.
    :param parameters: (RouteTable) – Parameters supplied to the create or
        update route table operation.
    :param custom_headers: (dict) – headers that will be added to the request
    :param raw: (bool) – returns the direct response alongside the deserialized
        response
    :return: AzureOperationPoller instance that returns RouteTable or
        ClientRawResponse if raw=true
    """

    try:
        route_table_creation = network_client.route_tables.create_or_update(
            resource_group_name,
            route_table_name,
            parameters,
            custom_headers=None,
            raw=False
        )
        return route_table_creation.result().provisioning_state

    except azure_exceptions.CloudError as e:
        return e

def get_route_table(
        resource_group_name,
        route_table_name,
        expand=None,
        custom_headers=None,
        raw=False
):
    """
    Gets the specified route table.

    :param network_client: (NetworkManagementClient) - object created using
        Service Principal
    :param resource_group_name:  (str) – The name of the resource group
    :param route_table_name: (str) – The name of the route table.
    :param expand: (str) – Expands referenced resources.
    :param custom_headers: (dict) – headers that will be added to the request
    :param raw: (bool) – returns the direct response alongside the deserialized
        response
    :return: RouteTable or ClientRawResponse if raw=true
    """

    try:
        route_table_info = network_client.route_tables.get(
            resource_group_name,
            route_table_name,
            expand=None,
            custom_headers=None,
            raw=False
        )
        return route_table_info

    except azure_exceptions.CloudError as e:
        return e

def delete_route_table(
        resource_group_name,
        route_table_name,
        custom_headers=None,
        raw=False
):
    """
    Deletes the specified route table.

    :param network_client: (NetworkManagementClient) - object created using
        Service Principal
    :param resource_group_name:  (str) – The name of the resource group
    :param route_table_name: (str) – The name of the route table.
    :param custom_headers: (dict) – headers that will be added to the request
    :param raw: (bool) – returns the direct response alongside the deserialized
        response
    :return: AzureOperationPoller instance that returns None or
        ClientRawResponse if raw=true
    """

    try:
        route_table_info = network_client.route_tables.delete(
            resource_group_name,
            route_table_name,
            custom_headers=None,
            raw=False
        )
        route_table_info.wait()
        return route_table_info.status()

    except azure_exceptions.CloudError as e:
        return e

# Routes Operations
def create_update_route(
        resource_group_name,
        route_table_name,
        route_name,
        route_parameters,
        custom_headers=None,
        raw=False
):
    """
    Creates or updates a route in the specified route table.

    :param network_client: (NetworkManagementClient) - object created using
        Service Principal
    :param resource_group_name:  (str) – The name of the resource group
    :param route_table_name: (str) – The name of the route table.
    :param route_name: (str) – The name of the route.
    :param route_parameters: (Route) – Parameters supplied to the create or
        update route operation.
    :param custom_headers: (dict) – headers that will be added to the request
    :param raw: (bool) – returns the direct response alongside the deserialized
        response
    :return: AzureOperationPoller instance that returns Route or
        ClientRawResponse if raw=true
    """

    try:
        route_creation = network_client.routes.create_or_update(
            resource_group_name,
            route_table_name,
            route_name,
            route_parameters,
            custom_headers=None,
            raw=False
        )
        return route_creation.result().provisioning_state

    except azure_exceptions.CloudError as e:
        return e

def get_route(
        resource_group_name,
        route_table_name,
        route_name,
        custom_headers=None,
        raw=False
):
    """
    Gets the specified route from a route table.

    :param network_client: (NetworkManagementClient) - object created using
        Service Principal
    :param resource_group_name:  (str) – The name of the resource group
    :param route_table_name: (str) – The name of the route table.
    :param route_name: (str) – The name of the route.
    :param custom_headers: (dict) – headers that will be added to the request
    :param raw: (bool) – returns the direct response alongside the deserialized
        response
    :return: Route or ClientRawResponse if raw=true
    """

    try:
        route_info = network_client.routes.get(
            resource_group_name,
            route_table_name,
            route_name,
            custom_headers=None,
            raw=False
        )
        return route_info

    except azure_exceptions.CloudError as e:
        return e

def delete_route(
        resource_group_name,
        route_table_name,
        route_name,
        custom_headers=None,
        raw=False
):
    """
    Deletes the specified route from a route table.

    :param network_client: (NetworkManagementClient) - object created using
        Service Principal
    :param resource_group_name:  (str) – The name of the resource group
    :param route_table_name: (str) – The name of the route table.
    :param route_name: (str) – The name of the route.
    :param custom_headers: (dict) – headers that will be added to the request
    :param raw: (bool) – returns the direct response alongside the deserialized
        response
    :return: AzureOperationPoller instance that returns None or
        ClientRawResponse if raw=true
    """

    try:
        route_info = network_client.routes.delete(
            resource_group_name,
            route_table_name,
            route_name,
            custom_headers=None,
            raw=False
        )
        route_info.wait()
        return route_info.status()

    except azure_exceptions.CloudError as e:
        return e


# Virtual Network Peerings Operations
def create_update_peering(
        resource_group_name,
        virtual_network_name,
        virtual_network_peering_name,
        virtual_network_peering_parameters,
        custom_headers=None,
        raw=False
):
    """
    Creates or updates a peering in the specified virtual network.

    :param network_client: (NetworkManagementClient) - object created using
        Service Principal
    :param resource_group_name: (str) – The name of the resource group.
    :param virtual_network_name: (str) – The name of the virtual network.
    :param virtual_network_peering_name: (str) – The name of the virtual
        network peering.
    :param virtual_network_peering_parameters:
    :param custom_headers: (dict) – headers that will be added to the request.
    :param raw: (bool) – returns the direct response alongside the deserialized
        response.
    :return: AzureOperationPoller instance that returns None or
        ClientRawResponse if raw=true
    """
    try:
        peering_creation = network_client.virtual_network_peerings.create_or_update(
            resource_group_name,
            virtual_network_name,
            virtual_network_peering_name,
            virtual_network_peering_parameters,
            custom_headers=None,
            raw=False
        )
        return peering_creation.result().provisioning_state

    except azure_exceptions.CloudError as e:
        return e


def get_peering(
        resource_group_name,
        virtual_network_name,
        virtual_network_peering_name,
        custom_headers=None,
        raw=False
):
    """
    Gets the specified virtual network peering.

    :param network_client: (NetworkManagementClient) - object created using
        Service Principal
    :param resource_group_name: (str) – The name of the resource group.
    :param virtual_network_name: (str) – The name of the virtual network.
    :param virtual_network_peering_name: (str) – The name of the virtual
        network peering.
    :param custom_headers: (dict) – headers that will be added to the request.
    :param raw: (bool) – returns the direct response alongside the deserialized
        response.
    :return: VirtualNetworkPeering or ClientRawResponse if raw=true
    """
    try:
        route_info = network_client.virtual_network_peerings.get(
            resource_group_name,
            virtual_network_name,
            virtual_network_peering_name,
            custom_headers=None,
            raw=False
        )
        return route_info

    except azure_exceptions.CloudError as e:
        return e

def delete_peering(
        resource_group_name,
        virtual_network_name,
        virtual_network_peering_name,
        custom_headers=None,
        raw=False
):
    """
    Deletes the specified virtual network peering.

    :param network_client: (NetworkManagementClient) - object created using
        Service Principal
    :param resource_group_name: (str) – The name of the resource group.
    :param virtual_network_name: (str) – The name of the virtual network.
    :param virtual_network_peering_name: (str) – The name of the virtual
        network peering.
    :param custom_headers: (dict) – headers that will be added to the request.
    :param raw: (bool) – returns the direct response alongside the deserialized
        response.
    :return: AzureOperationPoller instance that returns None or
        ClientRawResponse if raw=true
    """
    try:
        route_info = network_client.virtual_network_peerings.delete(
            resource_group_name,
            virtual_network_name,
            virtual_network_peering_name,
            custom_headers=None,
            raw=False
        )
        route_info.wait()
        return route_info.status()

    except azure_exceptions.CloudError as e:
        return e

# Local Network Gateway Operations
def create_update_local_net_gateway_ops(
        resource_group_name,
        local_network_gateway_name,
        parameters,
        custom_headers=None,
        raw=None
):
    """
    Creates or updates a local network gateway in the specified resource group.

    :param resource_group_name: (str) – The name of the resource group.
    :param local_network_gateway_name: (str) – The name of the local network
        gateway.
    :param parameters: (LocalNetworkGateway) – Parameters supplied to the
        create or update local network gateway operation.
    :param custom_headers: (dict) – headers that will be added to the request
    :param raw: (bool) – returns the direct response alongside the deserialized
        response
    :return: AzureOperationPoller instance that returns LocalNetworkGateway or
        ClientRawResponse if raw=true
    """

def get_local_net_gateway_ops(
        resource_group_name,
        local_network_gateway_name,
        custom_headers=None,
        raw=None
):
    """
    Gets the specified local network gateway in a resource group.

    :param resource_group_name: (str) – The name of the resource group.
    :param local_network_gateway_name: (str) – The name of the local network
        gateway.
    :param custom_headers: (dict) – headers that will be added to the request
    :param raw: (bool) – returns the direct response alongside the deserialized
        response
    :return: LocalNetworkGateway or ClientRawResponse if raw=true
    """

def delete_local_net_gatewat_ops(
        resource_group_name,
        local_network_gateway_name,
        custom_headers=None,
        raw=None
):
    """
    Deletes the specified local network gateway.

    :param resource_group_name: (str) – The name of the resource group.
    :param local_network_gateway_name: (str) – The name of the local network
        gateway.
    :param custom_headers: (dict) – headers that will be added to the request
    :param raw: (bool) – returns the direct response alongside the deserialized
        response
    :return: AzureOperationPoller instance that returns None or
        ClientRawResponse if raw=true
    """

# Main test function for Texas:
def main_tx():

    global network_client

    # Create Service Principal
    try:
        credentials = ServicePrincipalCredentials(
            client_id=CLIENT,
            secret=KEY,
            tenant=TENANT_ID,
            cloud_environment=AZURE_US_GOV_CLOUD)

    except AuthenticationError as e:
        return e


    # Client example
    network_client = NetworkManagementClient(credentials, subscription_id,
        base_url=AZURE_US_GOV_CLOUD.endpoints.resource_manager)

    # VNet create or update and get example
    print("Creating virtual network...")
    print(create_update_vnet(
        GROUP_NAME,
        VNET_NAME,
        {'location': my_location,
         'address_space': {'address_prefixes': ['10.70.192.0/20']},
         'dhcp_options': {'dns_servers': ['10.64.0.139', '10.64.4.129']}})
    )

    print("Getting virtual network info...")
    print(get_vnet(
        GROUP_NAME,
        VNET_NAME)
    )

    # Route and route table example
    print("Creating route table...")
    print(create_update_route_table(
        GROUP_NAME,
        RT_NAME,
        {'location': my_location})
    )

    print("Creating default route...")
    print(create_update_route(
        GROUP_NAME,
        RT_NAME,
        ROUTE_NAME,
        {'address_prefix': '0.0.0.0/0',
         'next_hop_type': 'VirtualNetworkGateway'})
    )

    print("Get route info...")
    print(get_route(
        GROUP_NAME,
        RT_NAME,
        ROUTE_NAME)
    )

    print("Get route table info...")
    print(get_route_table(
        GROUP_NAME,
        RT_NAME)
    )

    # Subnet get and create or update example: Make a dynamic reference to route_Table id?
    print("Creating subnet...")
    print(create_update_subnet(
        GROUP_NAME,
        VNET_NAME,
        SUBNET_NAME,
        {'address_prefix': '10.70.192.0/22',
         'route_table': {'id': '/subscriptions/7c138a92-f525-4446-88a9-7c5f8d818633/resourceGroups/CHQ_DR_Test_VNet_RG/providers/Microsoft.Network/routeTables/CHQ_DR_Test_RT'}})
    )

    print("Get subnet info...")
    print(get_subnet(
        GROUP_NAME,
        VNET_NAME,
        SUBNET_NAME)
    )

    # Peerings example
    print("Creating virtual network spoke peering...")
    print(create_update_peering(
        GROUP_NAME,
        VNET_NAME,
        SPOKE_NAME,
        {'remote_virtual_network': {
            'id': '/subscriptions/777c45ba-c8a0-4ae7-88c1-5b7945b004a6/resourceGroups/CHQ_DR_Core_VNet_RG/providers/Microsoft.Network/virtualNetworks/CHQ_DR_Core_VNet'},
         'use_remote_gateways': True,
         'allow_forwarded_traffic': True})
    )

    print("Get spoke peering info...")
    print(get_peering(
        GROUP_NAME,
        VNET_NAME,
        SPOKE_NAME)
    )

    # Use hub network client with CHQ_DR_Core subscription
    network_client =  NetworkManagementClient(credentials, hub_subscription_id,
        base_url=AZURE_US_GOV_CLOUD.endpoints.resource_manager)

    print("Creating virtual network hub peering...")
    print(create_update_peering(
        HUB_GROUP_NAME,
        HUB_VNET_NAME,
        HUB_NAME,
        {'remote_virtual_network': {'id': '/subscriptions/7c138a92-f525-4446-88a9-7c5f8d818633/resourceGroups/CHQ_DR_Test_VNet_RG/providers/Microsoft.Network/virtualNetworks/CHQ_DR_Test_VNet2'},
        'allow_gateway_transit': True})
    )

    print("Get hub peering info...")
    print(get_peering(
        HUB_GROUP_NAME,
        HUB_VNET_NAME,
        HUB_NAME)
    )

    print("Deleting virtual network hub peering...")
    print(delete_peering(
        HUB_GROUP_NAME,
        HUB_VNET_NAME,
        HUB_NAME)
    )

    # Switch back to CHQ_DR_Test subscription
    network_client = NetworkManagementClient(credentials, subscription_id,
        base_url=AZURE_US_GOV_CLOUD.endpoints.resource_manager)

    # Test cascading deletes for dependencies
    print("Deleting virtual network spoke peering...")
    print(delete_peering(
        GROUP_NAME,
        VNET_NAME,
        SPOKE_NAME)
    )

    print("Deleting subnet...")
    print(delete_subnet(
        GROUP_NAME,
        VNET_NAME,
        SUBNET_NAME)
    )

    print("Deleting virtual network...")
    print(delete_vnet(
        GROUP_NAME,
        VNET_NAME)
    )

    print("Deleting route...")
    print(delete_route(
        GROUP_NAME,
        RT_NAME,
        ROUTE_NAME)
    )

    print("Deleting route table...")
    print(delete_route_table(
        GROUP_NAME,
        RT_NAME)
    )

# Main test function for Virginia
def main_va():

    global network_client
    global resource_client

    # Create Service Principal
    try:
        credentials = ServicePrincipalCredentials(
            client_id=CLIENT,
            secret=KEY,
            tenant=TENANT_ID,
            cloud_environment=AZURE_US_GOV_CLOUD)

    except AuthenticationError as e:
        return e

    # Create hub and spoke clients
    network_client = NetworkManagementClient(credentials, subscription_id,
                                             base_url=AZURE_US_GOV_CLOUD.endpoints.resource_manager)

    resource_client = ResourceManagementClient(credentials,
                                               subscription_id,
                                               base_url=AZURE_US_GOV_CLOUD.endpoints.resource_manager)

    # Resource group example
    print("Creating hub resource group...")
    print(create_update_resource_group(
        HUB_GROUP_NAME,
        {'location': my_location})
    )
    print("Get hub resource group...")
    print(get_resource_group(
        HUB_GROUP_NAME)
    )
    print("Creating spoke resource group...")
    print(create_update_resource_group(
        SPOKE_GROUP_NAME,
        {'location': my_location})
    )
    print("Get spoke resource group...")
    print(get_resource_group(
        SPOKE_GROUP_NAME)
    )

    # VNet example
    print("Creating hub virtual network...")
    print(create_update_vnet(
        HUB_GROUP_NAME,
        HUB_VNET_NAME,
        {'location': my_location,
         'address_space': {'address_prefixes': ['10.71.0.0/20']},
         'dhcp_options': {'dns_servers': ['10.64.0.139', '10.64.4.129']}}
         )
    )

    print("Creating spoke virtual network...")
    print(create_update_vnet(
        SPOKE_GROUP_NAME,
        SPOKE_VNET_NAME,
        {'location': my_location,
         'address_space': {'address_prefixes': ['10.71.64.0/20']},
         'dhcp_options': {'dns_servers': ['10.64.0.139', '10.64.4.129']}}
         )
    )

    print("Getting hub virtual network info...")
    print(get_vnet(
        HUB_GROUP_NAME,
        HUB_VNET_NAME)
    )

    print("Getting spoke virtual network info...")
    print(get_vnet(
        SPOKE_GROUP_NAME,
        SPOKE_VNET_NAME)
    )

    # Route and route table example for hub
    print("Creating hub route table...")
    print(create_update_route_table(
        HUB_GROUP_NAME,
        HUB_RT_NAME,
        {'location': my_location})
    )

    print("Creating hub default route...")
    print(create_update_route(
        HUB_GROUP_NAME,
        HUB_RT_NAME,
        ROUTE_NAME,
        {'address_prefix': '0.0.0.0/0',
         'next_hop_type': 'VirtualNetworkGateway'})
    )

    print("Get hub route info...")
    print(get_route(
        HUB_GROUP_NAME,
        HUB_RT_NAME,
        ROUTE_NAME)
    )

    print("Get hub route table info...")
    print(get_route_table(
        HUB_GROUP_NAME,
        HUB_RT_NAME)
    )

    # Route and route table example for spoke
    print("Creating spoke route table...")
    print(create_update_route_table(
        SPOKE_GROUP_NAME,
        SPOKE_RT_NAME,
        {'location': my_location})
    )

    print("Creating spoke default route...")
    print(create_update_route(
        SPOKE_GROUP_NAME,
        SPOKE_RT_NAME,
        ROUTE_NAME,
        {'address_prefix': '0.0.0.0/0',
         'next_hop_type': 'VirtualNetworkGateway'})
    )

    print("Get spoke route info...")
    print(get_route(
        SPOKE_GROUP_NAME,
        SPOKE_RT_NAME,
        ROUTE_NAME)
    )

    print("Get spoke route table info...")
    print(get_route_table(
        SPOKE_GROUP_NAME,
        SPOKE_RT_NAME)
    )

    # Subnet examples
    print("Creating hub subnets...")
    print(create_update_subnet(
        HUB_GROUP_NAME,
        HUB_VNET_NAME,
        HUB_SUBNET_NAME_1,
        {'address_prefix': '10.71.0.0/22',
         'route_table': {
             'id': '/subscriptions/149ea8e4-d7b6-4cb6-99c8-d36ad98aecb2/resourceGroups/PGM_Core_VNet_RG/providers/Microsoft.Network/routeTables/PGM_Core_RT'}})
    )
    print(create_update_subnet(
        HUB_GROUP_NAME,
        HUB_VNET_NAME,
        HUB_SUBNET_NAME_2,
        {'address_prefix': '10.71.4.0/22',
         'route_table': {
             'id': '/subscriptions/149ea8e4-d7b6-4cb6-99c8-d36ad98aecb2/resourceGroups/PGM_Core_VNet_RG/providers/Microsoft.Network/routeTables/PGM_Core_RT'}})
    )
    print(create_update_subnet(
        HUB_GROUP_NAME,
        HUB_VNET_NAME,
        HUB_SUBNET_NAME_3,
        {'address_prefix': '10.71.8.0/22',
         'route_table': {
             'id': '/subscriptions/149ea8e4-d7b6-4cb6-99c8-d36ad98aecb2/resourceGroups/PGM_Core_VNet_RG/providers/Microsoft.Network/routeTables/PGM_Core_RT'}})
    )

    # Gateway subnet example
    print("Creating gateway subnet...")
    print(create_update_subnet(
        HUB_GROUP_NAME,
        HUB_VNET_NAME,
        GW_SUBNET_NAME,
        {'address_prefix': '10.71.15.0/27',
         'route_table': {
             'id': '/subscriptions/149ea8e4-d7b6-4cb6-99c8-d36ad98aecb2/resourceGroups/PGM_Core_VNet_RG/providers/Microsoft.Network/routeTables/PGM_Core_RT'}})
    )

    print("Get gateway subnet info...")
    print(get_subnet(
        HUB_GROUP_NAME,
        HUB_VNET_NAME,
        GW_SUBNET_NAME)
    )

    print("Creating spoke subnets...")
    print(create_update_subnet(
        SPOKE_GROUP_NAME,
        SPOKE_VNET_NAME,
        SPOKE_SUBNET_NAME_1,
        {'address_prefix': '10.71.64.0/22',
         'route_table': {
             'id': '/subscriptions/149ea8e4-d7b6-4cb6-99c8-d36ad98aecb2/resourceGroups/PGM_Test_VNet_RG/providers/Microsoft.Network/routeTables/PGM_Test_RT'}})
    )
    print(create_update_subnet(
        SPOKE_GROUP_NAME,
        SPOKE_VNET_NAME,
        SPOKE_SUBNET_NAME_2,
        {'address_prefix': '10.71.68.0/22',
         'route_table': {
             'id': '/subscriptions/149ea8e4-d7b6-4cb6-99c8-d36ad98aecb2/resourceGroups/PGM_Test_VNet_RG/providers/Microsoft.Network/routeTables/PGM_Test_RT'}})
    )
    print(create_update_subnet(
        SPOKE_GROUP_NAME,
        SPOKE_VNET_NAME,
        SPOKE_SUBNET_NAME_3,
        {'address_prefix': '10.71.72.0/22',
         'route_table': {
             'id': '/subscriptions/149ea8e4-d7b6-4cb6-99c8-d36ad98aecb2/resourceGroups/PGM_Test_VNet_RG/providers/Microsoft.Network/routeTables/PGM_Test_RT'}})
    )

    # # Peerings example
    # print("Creating virtual network spoke peering...")
    # print(create_update_peering(
    #     GROUP_NAME,
    #     VNET_NAME,
    #     SPOKE_NAME,
    #     {'remote_virtual_network': {
    #         'id': ''},
    #         'use_remote_gateways': True,
    #         'allow_forwarded_traffic': True})
    # )
    #
    # print("Get spoke peering info...")
    # print(get_peering(
    #     GROUP_NAME,
    #     VNET_NAME,
    #     SPOKE_NAME)
    # )
    #
    # # Use hub network client with CHQ_DR_Core subscription
    # network_client = NetworkManagementClient(credentials, hub_subscription_id,
    #                                          base_url=AZURE_US_GOV_CLOUD.endpoints.resource_manager)

    # print("Creating virtual network hub peering...")
    # print(create_update_peering(
    #     HUB_GROUP_NAME,
    #     HUB_VNET_NAME,
    #     HUB_NAME,
    #     {'remote_virtual_network': {
    #         'id': ''},
    #      'allow_gateway_transit': True})
    # )
    #
    # print("Get hub peering info...")
    # print(get_peering(
    #     HUB_GROUP_NAME,
    #     HUB_VNET_NAME,
    #     HUB_NAME)
    # )

    # print("Deleting virtual network hub peering...")
    # print(delete_peering(
    #     HUB_GROUP_NAME,
    #     HUB_VNET_NAME,
    #     HUB_NAME)
    # )
    #
    # # Switch back to CHQ_DR_Test subscription
    # network_client = NetworkManagementClient(credentials, subscription_id,
    #                                          base_url=AZURE_US_GOV_CLOUD.endpoints.resource_manager)
    #
    # # Test cascading deletes for dependencies
    # print("Deleting virtual network spoke peering...")
    # print(delete_peering(
    #     GROUP_NAME,
    #     VNET_NAME,
    #     SPOKE_NAME)
    # )
    #
    # print("Deleting subnet...")
    # print(delete_subnet(
    #     GROUP_NAME,
    #     VNET_NAME,
    #     SUBNET_NAME)
    # )

    # print("Deleting hub virtual network...")
    # print(delete_vnet(
    #     HUB_GROUP_NAME,
    #     HUB_VNET_NAME)
    # )
    #
    # print("Deleting spoke virtual network...")
    # print(delete_vnet(
    #     SPOKE_GROUP_NAME,
    #     SPOKE_VNET_NAME)
    # )
    #
    # print("Deleting hub default route...")
    # print(delete_route(
    #     HUB_GROUP_NAME,
    #     HUB_RT_NAME,
    #     ROUTE_NAME)
    # )
    #
    # print("Deleting spoke default route...")
    # print(delete_route(
    #     SPOKE_GROUP_NAME,
    #     SPOKE_RT_NAME,
    #     ROUTE_NAME)
    # )
    #
    # print("Deleting hub route table...")
    # print(delete_route_table(
    #     HUB_GROUP_NAME,
    #     HUB_RT_NAME)
    # )
    #
    # print("Deleting spoke route table...")
    # print(delete_route_table(
    #     SPOKE_GROUP_NAME,
    #     SPOKE_RT_NAME)
    # )
    #
    # print("Deleting hub resource group...")
    # print(delete_resource_group(
    #     HUB_GROUP_NAME)
    # )
    #
    # print("Deleting spoke resource group...")
    # print(delete_resource_group(
    #     SPOKE_GROUP_NAME)
    # )

# END OF CUMULUS.PY