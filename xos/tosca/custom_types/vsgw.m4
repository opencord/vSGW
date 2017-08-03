tosca_definitions_version: tosca_simple_yaml_1_0

# compile this with "m4 vbbu.m4 > vsgw.yaml"

# include macros
include(macros.m4)

node_types:
    tosca.nodes.VSGWService:
        derived_from: tosca.nodes.Root
        description: >
            VSGW Service
        capabilities:
            xos_base_service_caps
        properties:
            xos_base_props
            xos_base_service_props
            service_message:
                type: string
                required: true

    tosca.nodes.VSGWTenant:
        derived_from: tosca.nodes.Root
        description: >
            VSGW Tenant
        properties:
            xos_base_tenant_props
            tenant_message:
                type: string
                required: true
