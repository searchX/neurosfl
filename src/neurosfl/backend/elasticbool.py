from typing import Union
from neurosfl.frontend.structs import Node, UnaryOp, BinaryOp, StringLiteral, NumberLiteral, StartNode, LogicalOp, ComparisonOp
from neurosfl.backend.backend import Backend

class ElasticBoolBackend(Backend):
    """Backend for ElasticSearch's bool query"
    """

    def _extract_value(self, node: Node, symbols: dict = {}):
        """Extract value from node
        
        :param node: Node to extract value from
        :param symbols: Dictionary of symbols to use for extracting value
        :type node: :class:`Node`
        :type symbols: dict"""
        if isinstance(node, StringLiteral) or isinstance(node, NumberLiteral):
            return node.value
        else:
            raise NotImplementedError(f"ElasticBoolBackend::_extract_value(): Node type {type(node)} is not supported, node={node}")

    # Optimize this, I will cry
    def _create_comparison(self, field_name: str, op: str, right: Union[StringLiteral, NumberLiteral], symbols: dict = {}):
        """Create comparison query for ElasticSearch's bool query

        :param field_name: Field name to compare (elasticsearch field name, case sensitive)
        :param op: Operator to use for comparison (ex: =, !=, >, <, >=, <=)
        :param right: Right side of the comparison (:class:`StringLiteral` or :class:`NumberLiteral`)
        :param symbols: Dictionary of symbols to use for comparison
        :type field_name: str
        :type op: str
        :type right: Union[:class:`StringLiteral`, :class:`NumberLiteral`]
        :type symbols: dict
        :return: Comparison query for ElasticSearch's bool query
        :rtype: dict
        """
        right_value = self._extract_value(right, symbols)
        
        if op == "=":
            return {
                "bool": {
                    "must": {
                        "term": {
                            field_name: {
                                "value": right_value,
                                "boost": 1.0
                            }
                        }
                    }
                }
            }
        elif op == "!=":
            return {
                "bool": {
                    "must_not": {
                        "term": {
                            field_name: {
                                "value": right_value,
                                "boost": 1.0
                        }
                    }
                }
            }
        }
        elif op == ">":
            return {
                "bool": {
                    "must": {
                        "range": {
                            field_name: {
                                "gt": right_value
                            }
                        }
                    }
                }
            }
        elif op == "<":
            return {
                "bool": {
                    "must": {
                        "range": {
                            field_name: {
                                "lt": right_value
                            }
                        }
                    }
                }
            }
        elif op == ">=":
            return {
                "bool": {
                    "must": {
                        "range": {
                            field_name: {
                                "gte": right_value
                            }
                        }
                    }
                }
            }
        elif op == "<=":
            return {
                "bool": {
                    "must": {
                        "range": {
                            field_name: {
                                "lte": right_value
                            }
                        }
                    }
                }
            }
        else:
            raise NotImplementedError(f"ElasticBoolBackend::_create_comparison(): Operator {op} is not supported, field_name={field_name}, right={right}")

    def _create_logical(self, left: dict, op: str, right: dict):
        """Create logical query for ElasticSearch's bool query

        :param left: Left side of the logical operator
        :param op: Operator to use for logical operation (and, or)
        :param right: Right side of the logical operator
        :type left: dict
        :type op: str
        :type right: dict
        :return: Logical query for ElasticSearch's bool query
        :rtype: dict
        """
        if op == "and":
            return {
                "bool": {
                    "must": [left, right]
                }
            }
        elif op == "or":
            return {
                "bool": {
                    "should": [left, right]
                }
            }
        else:
            raise NotImplementedError(f"ElasticBoolBackend::create_logical(): Operator {op} is not supported, left={left}, right={right}")

    def _parse(self, node: BinaryOp, symbols: dict = {}):
        """Parse binary operation node"""
        # Because every node is a binary operation, we can just parse the left and right nodes

        # Check if type is logical op or comparison op
        if isinstance(node, LogicalOp):
            left = self._parse(node.left, symbols)
            right = self._parse(node.right, symbols)

            return self._create_logical(left, node.op, right)
        elif isinstance(node, ComparisonOp):
            field_name = node.left
            operator_used = node.op
            right_node = node.right

            return self._create_comparison(field_name, operator_used, right_node, symbols)
        else:
            raise NotImplementedError(f"ElasticBoolBackend::_parse(): Node type {type(node)} is not supported, node={node}")

    def parse(self, node: StartNode, symbols: dict = {}):
        """Parse :class:`StartNode` into ElasticSearch's bool query

        :param node: parser output
        :param symbols: Dictionary of symbols to use for parsing
        :type node: :class:`StartNode`
        :type symbols: dict
        :return: ElasticSearch's bool query
        :rtype: dict
        """

        return self._parse(node.data, symbols)