#!/usr/bin/env python3

from dataclasses import dataclass
import yaml
import json
from typing import Dict, List, is_typeddict
from collections import namedtuple

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

def get_node(name: str, group: int) -> dict:
  global node_index
  node_index = node_index + 1
  return {'name': name, 'group': group}

def get_link(source: str, target: str, value: int) -> dict:
  return {'source': source, 'target': target, 'value': value}

def get_both(nodes: list[dict], links: list[dict]) -> dict:
  return {'nodes': nodes, 'links': links}

def load_data(path: str) -> Dict:
  with open(path, 'r') as file:
    return yaml.safe_load(file)

def get_id(prefix: str, name: str) -> str:
  id = str(name).lower()
  return prefix + '-' + id if prefix else id

def build_both(prefix: str, data: Dict, level: int) -> dict:
  nodes = []
  links = []
  if isinstance(data, dict):
    for key, value in data.items():
      new_prefix = get_id(prefix, key)
      if prefix:
        links.append(get_link(prefix, new_prefix, 1))
      nodes.append(get_node(new_prefix, level))
      if value:
        both = build_both(new_prefix, value, level+1)
        nodes.extend(both['nodes'])
        links.extend(both['links'])
  else:
    if data != '.' and data != "x":
      links.append(get_link(prefix, data, 1))
  if level == 1:
    nodes.append(get_node('x',9))
  return get_both(nodes, links)

def id_to_index(id: str, nodes: List[dict]):
  index = 0
  for node in nodes:
    if node['name'] == id:
      return index
    index = index + 1
  return index

def ids_to_indexes(both: dict) -> dict:
  id_links = [
    get_link(
      id_to_index(link['source'], both['nodes']),
      id_to_index(link['target'], both['nodes']),
      link['value']
    ) for link in both['links']
  ]
  return get_both(both['nodes'], id_links)

if __name__ == "__main__":
  node_index = 0
  data = load_data('data/rede-electrica.yaml')
  both = build_both('', data, 1)
  both = ids_to_indexes(both)
  print(json.dumps(both))
