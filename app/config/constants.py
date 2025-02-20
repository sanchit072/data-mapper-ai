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
            "encryptionProtocol": None,
            "httpMethod": "GET",
            "httpClientVersion": None,
            "httpStatusesToIgnore": [],
            "contentType": "CSV",
            "paginationRequired": False,
            "responseSchema": None,
            "rootNodeName": None,
            "uriTemplate": {
                "type": "DSL",
                "templateName": "uriTemplate_1.ftl",
                "templateValue": None,
                "webhookConfig": None,
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
                "realizedTemplate": None
            },
            "headerTemplate": {
                "type": None,
                "templateName": "headerTemplate_1.ftl",
                "templateValue": None,
                "webhookConfig": None,
                "dslTemplateName": "headerDslTemplate_1.json",
                "dslTemplateValue": None,
                "executionOrder": [],
                "realizedTemplate": None
            },
            "requestBodyTemplate": {
                "type": None,
                "templateName": "requestBodyTemplate_1.ftl",
                "templateValue": None,
                "webhookConfig": None,
                "dslTemplateName": "requestBodyDslTemplate_1.json",
                "dslTemplateValue": None,
                "executionOrder": [],
                "realizedTemplate": None
            },
            "responseBodyTemplate": {
                "type": "DSL",
                "templateName": "responseBodyTemplate_1.ftl",
                "templateValue": None,
                "webhookConfig": None,
                "dslTemplateName": "responseBodyDslTemplate_1.json",
                "dslTemplateValue": None,
                "executionOrder": [],
                "realizedTemplate": None
            },
            "controlTemplate": {
                "type": "DSL",
                "templateName": "controlTemplate_1.ftl",
                "templateValue": None,
                "webhookConfig": None,
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
                "realizedTemplate": None
            }
        },
        "direction": "BOTH",
        "httpRedirectPolicy": "NORMAL"
    }
} 