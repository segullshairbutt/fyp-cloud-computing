def generate_method(schema_name):
    return {
        "tags": [
            "pet"
        ],
        "summary": "Add a new pet to the store",
        "description": "",
        # "operationId": "addPet",
        "requestBody": {
            "description": "description about addition to pet",
            "required": True,
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/" + schema_name
                    }
                }
            }
        },
        "responses": {
            "405": {
                "description": "Invalid input"
            }
        },
        "security": [
            {
                "petstore_auth": [
                    "write:pets",
                    "read:pets"
                ]
            }
        ],
        "x-location": {
            "$ref": "#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c1"
        },
        "x-metrics": {
            "load": ""
        }
    }


GET_METHOD_TEMPLATE = {
    "tags": [
        "pet"
    ],
    "summary": "Add a new pet to the store",
    "description": "",
    # "operationId": "addPet",
    "responses": {
        "405": {
            "description": "Invalid input"
        }
    },
    "security": [
        {
            "petstore_auth": [
                "write:pets",
                "read:pets"
            ]
        }
    ],
    "x-location": {
        "$ref": "#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c1"
    },
    "x-metrics": {
        "load": ""
    }
}

CLUSTER_TEMPLATE = {
    "cl1": {
        "name": "cl1",
        "metrics": {
            "load": ""
        },
        "worker-nodes": {
            "wn1": {
                "metrics": {
                    "load": ""
                },
                "name": "wn1",
                "pods": {
                    "pod1": {
                        "name": "pod1",
                        "metrics": {
                            "load": ""
                        },
                        "containers": {
                            "c1": {
                                "id": "c1",
                                "metrics": {
                                    "load": ""
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
