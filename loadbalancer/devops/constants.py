METHOD_TEMPLATE = {
    "summary": "Add a new pet to the store",
    "description": "",
    "operation_id": "addPet",
    "consumes": [
        "application/json",
        "application/xml"
    ],
    "produces": [
        "application/xml",
        "application/json"
    ],
    "parameters": [
        {
            "in": "body",
            "name": "body",
            "description": "Pet object that needs to be added to the store",
            "required": "true",
            "schema": {
                "$ref": "#/definitions/Pet"
            }
        }
    ],
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
    ]}
