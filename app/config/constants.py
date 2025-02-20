# Configuration dictionary for the application
APP_CONFIG = {
    # User related constants
    "user": {
        "tenant_id": "1730790390858",
        "tenant_uuid": "85fbe0ad-a6e0-4e03-bbae-2b2c7005c60b",
        "user_id": "1701952475614"
    },
    "connection": {
        "mode": "TL",
        "service": "SHIPMENT_STATUS_CSV",
        "interaction_type": "CARRIER_PUSH",
        "entity_id": "string",
        "connection_strategy": "TL_STATUS_UPDATE_PUSH_PUBLISHER",
        "connection_id": None  # Will be updated after connection creation
    },
    "interaction":{
        "sequence": 1,
        "metaData": {
            "connectionType": "DROP_EVENT",
            "encryptionProtocol": null,
            "httpMethod": "GET",
            "httpClientVersion": null,
            "httpStatusesToIgnore": [],
            "contentType": "CSV",
            "paginationRequired": false,
            "responseSchema": null,
            "rootNodeName": null,
            "uriTemplate": {
                "type": "DSL",
                "templateName": "uriTemplate_1.ftl",
                "templateValue": null,
                "webhookConfig": null,
                "dslTemplateName": "uriDslTemplate_1.json",
                "dslTemplateValue": {
                    "format": "JSON",
                    "conditionalMappingList": [
                        {
                        "mappingList": [
                            {
                            "name": "host",
                            "conditionList": [
                                {
                                "container": {
                                    "dataType": "STRING",
                                    "value": {
                                    "constantValue": "p44-production-us-central1-arcesb"
                                    }
                                }
                                }
                            ]
                            },
                            {
                            "name": "remoteLocation",
                            "conditionList": [
                                {
                                "container": {
                                    "dataType": "STRING",
                                    "value": {
                                    "constantValue": "eualex_tl"
                                    }
                                }
                                }
                            ]
                            }
                        ]
                        }
                    ]
                },
                "executionOrder": [],
                "realizedTemplate": null
            },
            "headerTemplate": {
                "type": null,
                "templateName": "headerTemplate_1.ftl",
                "templateValue": null,
                "webhookConfig": null,
                "dslTemplateName": "headerDslTemplate_1.json",
                "dslTemplateValue": null,
                "executionOrder": [],
                "realizedTemplate": null
            },
            "requestBodyTemplate": {
                "type": null,
                "templateName": "requestBodyTemplate_1.ftl",
                "templateValue": null,
                "webhookConfig": null,
                "dslTemplateName": "requestBodyDslTemplate_1.json",
                "dslTemplateValue": null,
                "executionOrder": [],
                "realizedTemplate": null
            },
            "responseBodyTemplate": {
                "type": "DSL",
                "templateName": "responseBodyTemplate_1.ftl",
                "templateValue": null,
                "webhookConfig": null,
                "dslTemplateName": "responseBodyDslTemplate_1.json",
                "dslTemplateValue": null,
                "executionOrder": [],
                "realizedTemplate": null
            },
            "controlTemplate": {
                "type": "DSL",
                "templateName": "controlTemplate_1.ftl",
                "templateValue": null,
                "webhookConfig": null,
                "dslTemplateName": "controlDslTemplate_1.json",
                "dslTemplateValue": {
                    "format": "JSON",
                    "conditionalMappingList": [
                    {
                        "mappingList": [
                        {
                            "name": "csvExtractorConfiguration",
                            "conditionList": [
                            {
                                "container": {
                                "dataType": "OBJECT",
                                "children": [
                                    {
                                    "name": "delimiter",
                                    "conditionList": [
                                        {
                                        "container": {
                                            "dataType": "STRING",
                                            "value": {
                                            "constantValue": ","
                                            }
                                        }
                                        }
                                    ]
                                    }
                                ]
                                }
                            }
                            ]
                        }
                        ]
                    }
                    ]
                },
                "executionOrder": [],
                "realizedTemplate": null
            }
        },
        "direction": "BOTH",
        "httpRedirectPolicy": "NORMAL"
    }
} 