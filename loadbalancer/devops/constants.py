METHOD_TEMPLATE = {
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
        "$ref": "#/info/x-pods/pod1/containers/c1/port"
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
        "$ref": "#/info/x-pods/pod1/containers/c1/port"
    },
    "x-metrics": {
        "load": ""
    }
}
