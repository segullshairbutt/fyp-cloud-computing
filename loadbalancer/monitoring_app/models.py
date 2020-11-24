class Path:
    def __init__(self, name, methods):
        self.name = name
        self.methods = methods


class Method:
    def __init__(
            self, name, parameters, produces, consumes, operation_id, summary, description,
            responses, security):
        self.name = name
        self.parameters = parameters
        self.produces = produces
        self.consumes = consumes
        self.operation_id = operation_id
        self.summary = summary
        self.description = description
        self.responses = responses
        self.security = security
