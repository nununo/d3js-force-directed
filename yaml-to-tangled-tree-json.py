#!/usr/bin/env python3

import yaml
import json
from typing import Any, Dict, List, is_typeddict
from collections import namedtuple
from json import JSONEncoder

"""
t4:
  quadro:
    ic1: x
  Escritório:
    caixacima:
      nne: x
      ene: x                          --- x is still undefined
      ese: t4-escritório-interruptor  --- full id in link
    interruptor: .                    --- . in target (to be ignored in links)
"""

class Node:
  name: str
  description: str
  id: int
  parents: List[Any]

  def __init__(self, parent_name: str, description: str):
    self.description = description
    self.name = Node._build_name(parent_name, description)
    self.id = Node._get_next_id()

  def addParent(self, parent):
    self.parents.append(parent)

  def parentIds(self) -> List[int]:
    return [parent.id for parent in self.parents]

  def toJson(self) -> str:
    return '{"id": self.id, "parents": parentIds() }'

  def _build_name(parent_name: str, description: str) -> str:
    name = str(description).lower()
    return parent_name + '-' + name if parent_name else name

  def _get_next_id() -> int:
    global node_id
    node_id = node_id + 1
    return node_id


class NodeEncode(JSONEncoder):
  def default(self, o):
    return o.__dict__


def load_data(path: str) -> Dict:
  with open(path, 'r') as file:
    return yaml.safe_load(file)

def build_nodes(parent_name: str, data: Dict) -> List[Node]:
  nodes = []
  if isinstance(data, dict):
    for key, value in data.items():
      node = Node(parent_name, key)
      nodes.append(node)
      if value:
        children = build_nodes(node.name, value)
        nodes.extend(children)
  return nodes

def nodes_to_dict(nodes: List[Node]) -> List[Dict]:
  return [node.__dict__ for node in nodes]

if __name__ == "__main__":
  node_id = 0
  data = load_data('data/rede-electrica.yaml')
  nodes = build_nodes('', data)
  nodes_dict = nodes_to_dict(nodes)
  print(json.dumps(nodes_dict))
