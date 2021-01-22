MAX_WN_LOAD = 50
MAX_POD_LOAD = 50

data_array = [
    {
        "x-clusters": {
            "cl1": {
                "name": "cl1",
                "metrics": {
                    "load": 89
                },
                "worker-nodes": {
                    "wn1": {
                        "metrics": {
                            "load": 60
                        },
                        "name": "wn1",
                        "pods": {
                            "pod1": {
                                "name": "pod1",
                                "metrics": {
                                    "load": 79
                                },
                                "containers": {
                                    "c1": {
                                        "id": "c1",
                                        "metrics": {
                                            "load": 90
                                        }
                                    },
                                    "c2": {
                                        "id": "c2",
                                        "metrics": {
                                            "load": 34
                                        }
                                    },
                                    "c3": {
                                        "id": "c3",
                                        "metrics": {
                                            "load": 56
                                        }
                                    },
                                    "c4": {
                                        "id": "c4",
                                        "metrics": {
                                            "load": 7
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "paths": {
            "/pets": {
                "post": {
                    "tags": [
                        "pet"
                    ],
                    "summary": "Add a new pet to the store",
                    "description": "",
                    "requestBody": {
                        "description": "description about addition to pet",
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Pet"
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
                        "load": 53
                    }
                },
                "get": {
                    "tags": [
                        "pet"
                    ],
                    "summary": "Add a new pet to the store",
                    "description": "",
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
                        "$ref": "#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c2"
                    },
                    "x-metrics": {
                        "load": 89
                    }
                }
            },
            "/users": {
                "patch": {
                    "tags": [
                        "pet"
                    ],
                    "summary": "Add a new pet to the store",
                    "description": "",
                    "requestBody": {
                        "description": "description about addition to pet",
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/User"
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
                        "$ref": "#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c3"
                    },
                    "x-metrics": {
                        "load": 5
                    }
                },
                "delete": {
                    "tags": [
                        "pet"
                    ],
                    "summary": "Add a new pet to the store",
                    "description": "",
                    "requestBody": {
                        "description": "description about addition to pet",
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/User"
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
                        "$ref": "#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c3"
                    },
                    "x-metrics": {
                        "load": 50
                    }
                },
                "get": {
                    "tags": [
                        "pet"
                    ],
                    "summary": "Add a new pet to the store",
                    "description": "",
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
                        "$ref": "#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c2"
                    },
                    "x-metrics": {
                        "load": 55
                    }
                }
            },
            "/orders": {
                "get": {
                    "tags": [
                        "pet"
                    ],
                    "summary": "Add a new pet to the store",
                    "description": "",
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
                        "$ref": "#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c2"
                    },
                    "x-metrics": {
                        "load": 58
                    }
                },
                "patch": {
                    "tags": [
                        "pet"
                    ],
                    "summary": "Add a new pet to the store",
                    "description": "",
                    "requestBody": {
                        "description": "description about addition to pet",
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Order"
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
                        "$ref": "#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c4"
                    },
                    "x-metrics": {
                        "load": 85
                    }
                }
            }
        }
    },
    {
        "x-clusters": {
            "cl1": {
                "name": "cl1",
                "metrics": {
                    "load": 72
                },
                "worker-nodes": {
                    "wn1": {
                        "metrics": {
                            "load": 19
                        },
                        "name": "wn1",
                        "pods": {
                            "pod1": {
                                "name": "pod1",
                                "metrics": {
                                    "load": 41
                                },
                                "containers": {
                                    "c1": {
                                        "id": "c1",
                                        "metrics": {
                                            "load": 30
                                        }
                                    },
                                    "c2": {
                                        "id": "c2",
                                        "metrics": {
                                            "load": 27
                                        }
                                    },
                                    "c3": {
                                        "id": "c3",
                                        "metrics": {
                                            "load": 16
                                        }
                                    },
                                    "c4": {
                                        "id": "c4",
                                        "metrics": {
                                            "load": 13
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "paths": {
            "/pets": {
                "post": {
                    "tags": [
                        "pet"
                    ],
                    "summary": "Add a new pet to the store",
                    "description": "",
                    "requestBody": {
                        "description": "description about addition to pet",
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Pet"
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
                        "load": 92
                    }
                },
                "get": {
                    "tags": [
                        "pet"
                    ],
                    "summary": "Add a new pet to the store",
                    "description": "",
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
                        "$ref": "#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c2"
                    },
                    "x-metrics": {
                        "load": 78
                    }
                }
            },
            "/users": {
                "patch": {
                    "tags": [
                        "pet"
                    ],
                    "summary": "Add a new pet to the store",
                    "description": "",
                    "requestBody": {
                        "description": "description about addition to pet",
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/User"
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
                        "$ref": "#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c3"
                    },
                    "x-metrics": {
                        "load": 89
                    }
                },
                "delete": {
                    "tags": [
                        "pet"
                    ],
                    "summary": "Add a new pet to the store",
                    "description": "",
                    "requestBody": {
                        "description": "description about addition to pet",
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/User"
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
                        "$ref": "#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c3"
                    },
                    "x-metrics": {
                        "load": 68
                    }
                },
                "get": {
                    "tags": [
                        "pet"
                    ],
                    "summary": "Add a new pet to the store",
                    "description": "",
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
                        "$ref": "#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c2"
                    },
                    "x-metrics": {
                        "load": 66
                    }
                }
            },
            "/orders": {
                "get": {
                    "tags": [
                        "pet"
                    ],
                    "summary": "Add a new pet to the store",
                    "description": "",
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
                        "$ref": "#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c2"
                    },
                    "x-metrics": {
                        "load": 21
                    }
                },
                "patch": {
                    "tags": [
                        "pet"
                    ],
                    "summary": "Add a new pet to the store",
                    "description": "",
                    "requestBody": {
                        "description": "description about addition to pet",
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Order"
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
                        "$ref": "#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c4"
                    },
                    "x-metrics": {
                        "load": 70
                    }
                }
            }
        }
    },
    {
        "x-clusters": {
            "cl1": {
                "name": "cl1",
                "metrics": {
                    "load": 70
                },
                "worker-nodes": {
                    "wn1": {
                        "metrics": {
                            "load": 24
                        },
                        "name": "wn1",
                        "pods": {
                            "pod1": {
                                "name": "pod1",
                                "metrics": {
                                    "load": 41
                                },
                                "containers": {
                                    "c1": {
                                        "id": "c1",
                                        "metrics": {
                                            "load": 20
                                        }
                                    },
                                    "c2": {
                                        "id": "c2",
                                        "metrics": {
                                            "load": 22
                                        }
                                    },
                                    "c3": {
                                        "id": "c3",
                                        "metrics": {
                                            "load": 22
                                        }
                                    },
                                    "c4": {
                                        "id": "c4",
                                        "metrics": {
                                            "load": 7
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "paths": {
            "/pets": {
                "post": {
                    "tags": [
                        "pet"
                    ],
                    "summary": "Add a new pet to the store",
                    "description": "",
                    "requestBody": {
                        "description": "description about addition to pet",
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Pet"
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
                        "load": 89
                    }
                },
                "get": {
                    "tags": [
                        "pet"
                    ],
                    "summary": "Add a new pet to the store",
                    "description": "",
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
                        "$ref": "#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c2"
                    },
                    "x-metrics": {
                        "load": 13
                    }
                }
            },
            "/users": {
                "patch": {
                    "tags": [
                        "pet"
                    ],
                    "summary": "Add a new pet to the store",
                    "description": "",
                    "requestBody": {
                        "description": "description about addition to pet",
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/User"
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
                        "$ref": "#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c3"
                    },
                    "x-metrics": {
                        "load": 21
                    }
                },
                "delete": {
                    "tags": [
                        "pet"
                    ],
                    "summary": "Add a new pet to the store",
                    "description": "",
                    "requestBody": {
                        "description": "description about addition to pet",
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/User"
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
                        "$ref": "#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c3"
                    },
                    "x-metrics": {
                        "load": 30
                    }
                },
                "get": {
                    "tags": [
                        "pet"
                    ],
                    "summary": "Add a new pet to the store",
                    "description": "",
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
                        "$ref": "#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c2"
                    },
                    "x-metrics": {
                        "load": 52
                    }
                }
            },
            "/orders": {
                "get": {
                    "tags": [
                        "pet"
                    ],
                    "summary": "Add a new pet to the store",
                    "description": "",
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
                        "$ref": "#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c2"
                    },
                    "x-metrics": {
                        "load": 62
                    }
                },
                "patch": {
                    "tags": [
                        "pet"
                    ],
                    "summary": "Add a new pet to the store",
                    "description": "",
                    "requestBody": {
                        "description": "description about addition to pet",
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Order"
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
                        "$ref": "#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c4"
                    },
                    "x-metrics": {
                        "load": 14
                    }
                }
            }
        }
    }
]

config = {
    "openapi": "3.0.0",
    "info": {
        "description": "This is a sample server Petstore server.  You can find out more about     Swagger at [http://swagger.io](http://swagger.io) or on [irc.freenode.net, #swagger](http://swagger.io/irc/).      For this sample, you can use the api key `special-key` to test the authorization     filters.",
        "version": "1.0.0",
        "title": "Swagger Petstore",
        "termsOfService": "http://swagger.io/terms/",
        "contact": {
            "email": "apiteam@swagger.io"
        },
        "license": {
            "name": "Apache 2.0",
            "url": "http://www.apache.org/licenses/LICENSE-2.0.html"
        },
        "x-clusters": {
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
                                    },
                                    "c2": {
                                        "id": "c2",
                                        "metrics": {
                                            "load": ""
                                        }
                                    },
                                    "c3": {
                                        "id": "c3",
                                        "metrics": {
                                            "load": ""
                                        }
                                    },
                                    "c4": {
                                        "id": "c4",
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
    },
    "servers": [
        {
            "url": "https://petstore.swagger.io",
            "description": "Optional server description, e.g. Main (production) server"
        }
    ],
    "tags": [
        {
            "name": "pet",
            "description": "Everything about your Pets",
            "externalDocs": {
                "description": "Find out more",
                "url": "http://swagger.io"
            }
        },
        {
            "name": "store",
            "description": "Access to Petstore orders"
        },
        {
            "name": "user",
            "description": "Operations about user",
            "externalDocs": {
                "description": "Find out more about our store",
                "url": "http://swagger.io"
            }
        }
    ],
    "paths": {
        "/pets": {
            "post": {
                "tags": [
                    "pet"
                ],
                "summary": "Add a new pet to the store",
                "description": "",
                "requestBody": {
                    "description": "description about addition to pet",
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/Pet"
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
            },
            "get": {
                "tags": [
                    "pet"
                ],
                "summary": "Add a new pet to the store",
                "description": "",
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
                    "$ref": "#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c2"
                },
                "x-metrics": {
                    "load": ""
                }
            }
        },
        "/users": {
            "patch": {
                "tags": [
                    "pet"
                ],
                "summary": "Add a new pet to the store",
                "description": "",
                "requestBody": {
                    "description": "description about addition to pet",
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/User"
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
                    "$ref": "#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c3"
                },
                "x-metrics": {
                    "load": ""
                }
            },
            "delete": {
                "tags": [
                    "pet"
                ],
                "summary": "Add a new pet to the store",
                "description": "",
                "requestBody": {
                    "description": "description about addition to pet",
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/User"
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
                    "$ref": "#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c3"
                },
                "x-metrics": {
                    "load": ""
                }
            },
            "get": {
                "tags": [
                    "pet"
                ],
                "summary": "Add a new pet to the store",
                "description": "",
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
                    "$ref": "#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c2"
                },
                "x-metrics": {
                    "load": ""
                }
            }
        },
        "/orders": {
            "get": {
                "tags": [
                    "pet"
                ],
                "summary": "Add a new pet to the store",
                "description": "",
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
                    "$ref": "#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c2"
                },
                "x-metrics": {
                    "load": ""
                }
            },
            "patch": {
                "tags": [
                    "pet"
                ],
                "summary": "Add a new pet to the store",
                "description": "",
                "requestBody": {
                    "description": "description about addition to pet",
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/Order"
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
                    "$ref": "#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c4"
                },
                "x-metrics": {
                    "load": ""
                }
            }
        }
    },
    "components": {
        "securitySchemes": {
            "petstore_auth": {
                "type": "oauth2",
                "flows": {
                    "authorizationCode": {
                        "authorizationUrl": "/oauth/dialog",
                        "tokenUrl": "/oauth/token",
                        "scopes": {
                            "write:pets": "modify pets in your account",
                            "read:pets": "read your pets"
                        }
                    }
                }
            },
            "api_key": {
                "type": "apiKey",
                "name": "api_key",
                "in": "header"
            }
        },
        "schemas": {
            "Order": {
                "x-storage-level": "pod",
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "format": "int64"
                    },
                    "petId": {
                        "type": "integer",
                        "format": "int64"
                    },
                    "quantity": {
                        "type": "integer",
                        "format": "int32"
                    },
                    "shipDate": {
                        "type": "string",
                        "format": "date-time"
                    },
                    "status": {
                        "type": "string",
                        "description": "Order Status",
                        "enum": [
                            "placed",
                            "approved",
                            "delivered"
                        ]
                    },
                    "complete": {
                        "type": "boolean",
                        "default": False
                    }
                },
                "xml": {
                    "name": "Order"
                }
            },
            "Category": {
                "x-storage-level": "pod",
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "format": "int64"
                    },
                    "name": {
                        "type": "string"
                    }
                },
                "xml": {
                    "name": "Category"
                }
            },
            "User": {
                "x-storage-level": "pod",
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "format": "int64"
                    },
                    "username": {
                        "type": "string"
                    },
                    "firstName": {
                        "type": "string"
                    },
                    "lastName": {
                        "type": "string"
                    },
                    "email": {
                        "type": "string"
                    },
                    "password": {
                        "type": "string"
                    },
                    "phone": {
                        "type": "string"
                    },
                    "userStatus": {
                        "type": "integer",
                        "format": "int32",
                        "description": "User Status"
                    }
                },
                "xml": {
                    "name": "User"
                }
            },
            "Tag": {
                "x-storage-level": "pod",
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "format": "int64"
                    },
                    "name": {
                        "type": "string"
                    }
                },
                "xml": {
                    "name": "Tag"
                }
            },
            "Pet": {
                "x-storage-level": "pod",
                "type": "object",
                "required": [
                    "name",
                    "photoUrls"
                ],
                "properties": {
                    "id": {
                        "type": "integer",
                        "format": "int64"
                    },
                    "category": {
                        "$ref": "#/components/schemas/Category"
                    },
                    "name": {
                        "type": "string",
                        "example": "doggie"
                    },
                    "photoUrls": {
                        "type": "array",
                        "xml": {
                            "name": "photoUrl",
                            "wrapped": True
                        },
                        "items": {
                            "type": "string"
                        }
                    },
                    "tags": {
                        "type": "array",
                        "xml": {
                            "name": "tag",
                            "wrapped": True
                        },
                        "items": {
                            "$ref": "#/components/schemas/Tag"
                        }
                    },
                    "status": {
                        "type": "string",
                        "description": "pet status in the store",
                        "enum": [
                            "available",
                            "pending",
                            "sold"
                        ]
                    }
                },
                "xml": {
                    "name": "Pet"
                }
            }
        }
    },
    "externalDocs": {
        "description": "Find out more about Swagger",
        "url": "http://swagger.io"
    }
}
