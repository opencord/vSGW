tosca_definitions_version: tosca_simple_yaml_1_0

# compile this with "m4 vsgwc.m4 > vsgwc.yaml"

# include macros
include(macros.m4)

node_types:
    tosca.nodes.VSGWCService:
        derived_from: tosca.nodes.Root
        description: >
            VSGWC Service
        capabilities:
            xos_base_service_caps
        properties:
            xos_base_props
            xos_base_service_props

    tosca.nodes.VSGWCTenant:
        derived_from: tosca.nodes.Root
        description: >
            VSGWC Tenant
        properties:
            xos_base_tenant_props
            tenant_message:
                type: string
                required: false