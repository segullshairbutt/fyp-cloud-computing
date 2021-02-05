MAX_WN_LOAD = 50
MIN_WN_LOAD = 20
MAX_POD_LOAD = 50
MIN_POD_LOAD = 30
DEFAULT_SCHEMA_NAME = 'default'
POD_LEVEL = "pod"
CL_LEVEL = "cluster"
WN_LEVEL = "worker-node"
SCHEMA_LEVEL = "x-storage-level"

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
              "load": 82
            },
            "name": "wn1",
            "pods": {
              "pod1": {
                "name": "pod1",
                "metrics": {
                  "load": 46
                },
                "containers": {
                  "c1": {
                    "id": "c1",
                    "metrics": {
                      "load": 17
                    }
                  },
                  "c2": {
                    "id": "c2",
                    "metrics": {
                      "load": 2
                    }
                  },
                  "c3": {
                    "id": "c3",
                    "metrics": {
                      "load": 4
                    }
                  },
                  "c4": {
                    "id": "c4",
                    "metrics": {
                      "load": 19
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
            "load": 48
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
            "load": 36
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
            "load": 34
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
            "load": 45
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
            "load": 33
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
            "load": 49
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
            "load": 49
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
          "load": 94
        },
        "worker-nodes": {
          "wn1": {
            "metrics": {
              "load": 89
            },
            "name": "wn1",
            "pods": {
              "pod1": {
                "name": "pod1",
                "metrics": {
                  "load": 52
                },
                "containers": {
                  "c1": {
                    "id": "c1",
                    "metrics": {
                      "load": 28
                    }
                  },
                  "c2": {
                    "id": "c2",
                    "metrics": {
                      "load": 9
                    }
                  },
                  "c3": {
                    "id": "c3",
                    "metrics": {
                      "load": 20
                    }
                  },
                  "c4": {
                    "id": "c4",
                    "metrics": {
                      "load": 27
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
            "load": 44
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
            "load": 47
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
            "load": 45
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
            "load": 35
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
            "load": 42
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
            "load": 47
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
            "load": 43
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
          "load": 87
        },
        "worker-nodes": {
          "wn1": {
            "metrics": {
              "load": 86
            },
            "name": "wn1",
            "pods": {
              "pod1": {
                "name": "pod1",
                "metrics": {
                  "load": 59
                },
                "containers": {
                  "c1": {
                    "id": "c1",
                    "metrics": {
                      "load": 21
                    }
                  },
                  "c2": {
                    "id": "c2",
                    "metrics": {
                      "load": 28
                    }
                  },
                  "c3": {
                    "id": "c3",
                    "metrics": {
                      "load": 31
                    }
                  },
                  "c4": {
                    "id": "c4",
                    "metrics": {
                      "load": 25
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
            "load": 34
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
            "load": 45
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
            "load": 46
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
            "load": 48
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
            "load": 47
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
            "load": 41
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
            "load": 33
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
