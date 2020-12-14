def _get_initial_config(port):
    return {
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
            "x-pods": {
                "pod1": {
                    "name": "pod1",
                    "metrics": {
                        "CPU": "",
                        "RAM": ""
                    },
                    "containers": {
                        "c1": {
                            "id": "c1",
                            "metrics": {
                                "load": ""
                            },
                            "port": port
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
        "paths": {},
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


def generate_configuration(endpoints):
    template = _get_initial_config(4000)
    paths = template["paths"]
    for endpoint in endpoints:
        path = paths.setdefault(endpoint.path.name, {})

        for method in endpoint.path.method_set.all():
            extra_fields = method.extra_fields
            extra_fields["x-location"] = {
                "$ref": "#/info/x-pods/pod1/containers/c1/port"
            }
            extra_fields["x-metrics"] = {
                "load": ""
            }
            path[method.name] = extra_fields

    return template
