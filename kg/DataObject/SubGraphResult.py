import json
from typing import List, Union, Dict, Any

import pandas as pd


class Node:
    intra_id: int
    statement: str
    tag: str
    id: int
    community: int
    n: Dict[str, Union[str, int]] = None
    degree: int = None

    def __init__(self, intra_id: int, statement: str, id: int, tag: str = '', community: int = 0,
                 n: Dict[str, Union[str, int]] = None, degree: int = None):
        self.intra_id = intra_id
        self.statement = statement
        self.tag = tag
        self.id = id
        self.community = community
        if n:
            self.n = n
        if degree:
            self.degree = degree

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.intra_id == other.intra_id
        return False

    def __hash__(self):
        return hash(self.intra_id)


class Link:
    target: int
    source: int
    tag: str
    value: int

    def __init__(self, target: int, source: int, tag: str = '', value: int = ''):
        self.target = target
        self.source = source
        self.tag = tag
        self.value = value


class ResultItem:
    weight: int
    intra_id: int
    query_id: int
    statement: str
    selected: int
    nodes: List[Node]
    links: List[Link]
    date: str
    channel: List[str]
    location: List[str]
    url: str

    def __init__(self, weight, intra_id, query_id, statement, nodes, links,
                 selected=0, date="", channel=[], location=[], url=""):
        self.weight = weight
        self.intra_id = intra_id
        self.query_id = query_id
        self.selected = selected
        self.statement = statement
        self.nodes = nodes  # This is the list of Node to reach the  target statement
        self.links = links
        self.date = date
        self.channel = channel
        self.location = location
        self.url = url


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (Node, Link, ResultItem)):
            return obj.__dict__
        return super(ComplexEncoder, self).default(obj)
