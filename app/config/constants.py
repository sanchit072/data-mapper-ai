# Configuration dictionary for the application
APP_CONFIG = {
    # User related constants
    "user": {
        "tenant_id": "1730790390858",
        "tenant_uuid": "85fbe0ad-a6e0-4e03-bbae-2b2c7005c60b",
        "user_id": "1699944233037"
    },
    "connection": {
        "mode": "TL",
        "service": "SHIPMENT_STATUS_CSV",
        "interaction_type": "CARRIER_PUSH",
        "entity_id": "AI_DEMO",
        "connection_strategy": "TL_STATUS_UPDATE_PUSH_PUBLISHER",
        "connection_id": "TL.SHIPMENT_STATUS_CSV.CARRIER_PUSH.AI_DEMO"  # Will be updated after connection creation
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
                "templateValue": "",
                "webhookConfig": None,
                "dslTemplateName": "headerDslTemplate_1.json",
                "dslTemplateValue": None,
                "executionOrder": [],
                "realizedTemplate": None
            },
            "requestBodyTemplate": {
                "type": None,
                "templateName": "requestBodyTemplate_1.ftl",
                "templateValue": "",
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
    },
    "trials": {
        "connectionId": "TL.SHIPMENT_STATUS_CSV.CARRIER_PUSH.AI_DEMO", # Will be updated after connection creation
        "contextId": "",
        "trialId": None,
        "description": "Test",
        "displayName": "DM_TRIAL",
        "certified": True,
        "updateTimestamp": "2025-02-20T17:00:30Z",
        "inputData": "",
        "userId": "1701952475614",
        "interactions": [
            {
                "sequence": 1,
                "requestData": "",
                "mockResponse": "",
                "mockFilePayload": "",
                "benchmarkResult": {
                    "sequence": 1,
                    "control": "{\n\"delimiter\":\",\"\n}\n",
                    "url": None,
                    "header": "{}",
                    "request": "",
                    "rawResponse": "",
                    "filePayload": "",
                    "response": "",
                    "mockResponse": "",
                    "mockFilePayload": "",
                    "error": None,
                    "interactionDiff": {
                        "sequence": 1,
                        "control": None,
                        "url": None,
                        "header": None,
                        "request": None,
                        "response": None
                    },
                    "passed": True
                }
            }
        ],
        "ignoredFields": []
    }
}