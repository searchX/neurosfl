from neurosfl.consts import BackendType
from neurosfl.frontend.parser import lexer, parser
from neurosfl.backend.elasticbool import ElasticBoolBackend

def parse_from_string(code: str, debug: bool = False, backend: BackendType = BackendType.ELASTICSEARCH):
    """Used to parse code from string, and return the parsed code for the given backend, only supports Elasticsearch for now

    :param code: Code to parse
    :param debug: Enable debugging
    :param backend: Backend to use for parsing
    :type code: str
    :type debug: bool, optional
    :type backend: :class:`BackendType`, optional
    :return: Parsed boolean filter query
    :rtype: dict

    :raises ValueError: If there is an error in parsing
    :raises NotImplementedError: If the backend is not supported or the parse token operation is not supported

    .. code-block:: python

        from neurosfl.main import parse_from_string
        bool_filter = parse_from_string("company = 'NIKE'")

    .. code-block:: python

        from neurosfl.main import parse_from_string
        bool_filter = parse_from_string("where company = 'NIKE' and category = 'Shoes' or (listPrice <= 1000 AND price >= 500)", debug=True)
        
    .. note:: The debug parameter is used to enable debugging, which will print the tokens and the parsed tree
    """

    # Only support Elasticsearch for now
    if backend != BackendType.ELASTICSEARCH:
        raise NotImplementedError("Only Elasticsearch is supported for now")

    # Lexical analysis if debugging is needed
    if debug:
        lexer.input(code)
        for token in lexer:
            print(token)

    node = parser.parse(code, lexer=lexer)
    if not node:
        raise ValueError("Parsing failed")
    if debug:
        print(node)

    return ElasticBoolBackend().parse(node)