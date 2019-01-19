import typing


def parse_query_string_arguments(*, arguments, main_entity):
    parsed_arguments = {}
    for argument in arguments:
        if main_entity.__annotations__[argument.split('__')[0]].__origin__ is typing.Union:
            var_type = main_entity.__annotations__[argument.split('__')[0]].__args__[0]
        else:
            var_type = main_entity.__annotations__[argument.split('__')[0]]

        if var_type != str:
            parsed_arguments[argument] = [var_type(value) for value in arguments[argument]]
        else:
            parsed_arguments[argument] = [value.decode() for value in arguments[argument]]

    return parsed_arguments
