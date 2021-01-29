def _gen_dict_extract(key, var):
    if hasattr(var, 'items'):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in _gen_dict_extract(key, v):
                    yield result
            elif isinstance(v, (list)):
                for d in v:
                    for result in _gen_dict_extract(key, d):
                        yield result


def _get_schema_only(references):
    saved_schema = 'default'
    for reference in references:
        schema = reference.split("#/components/schemas/")
        try:
            saved_schema = schema[1]
        except IndexError:
            pass

    return saved_schema


def _get_schemas_only(references):
    saved_schemas = []
    for reference in references:
        schema = reference.split("#/components/schemas/")
        try:
            saved_schemas.append(schema[1])
        except IndexError:
            pass

    return saved_schemas


def _join_components(threshold, components):
    joined_components = []
    remaining_components = []
    collective_contribution = 0
    for i in range(len(components)):
        component = components[i]
        collective_contribution += component.contribution

        if collective_contribution < threshold:
            joined_components.append(component)
        else:
            remaining_components.append(component)

    return joined_components, remaining_components
