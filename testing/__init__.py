import json
from colorama import Fore, Back, Style
import os
import sys
from collections import namedtuple
from argparse import Namespace
from runpy import run_path


def get_path(path):
  return os.path.join(sys.path[0], path)


def all_files(folder):
  for name in os.listdir(folder):
    if name.endswith(".py"):
      yield os.path.join(folder, name)


def run_file(file):
  if isinstance(file, str):
    run_config(get_config(open(get_path(file))))
  else:
    run_config(get_config(file))


def get_config(file):
  raw_config = json.load(file)

  output = []

  for test_location, code_location in raw_config.items():
    test_path = get_path(test_location)
    code_path = get_path(code_location)
    target = []

    for module_file in os.listdir(code_path):
      module_path = os.path.join(code_path, module_file)
      module_name = module_file.replace(".py", "")
      module = run_path(module_path)

      testables = [
        {
          "name": name,
          "unittest_path": os.path.join(test_path, module_name, name + ".py")
        }
        for name in module if not name.startswith("_")
      ]

      target.append({
        "name": module_name,
        "path": module_path,
        "testables": testables
      })

    output.append(target)

  return output


def run_config(config):
  for target in config:
    for module_spec in target:
      test_module(**module_spec)


def test_module(*, name, path, testables):
  module = run_path(path)
  for testable in testables:
    test_testable(module, name, **testable)


def test_testable(module, module_name, *, name, unittest_path):
  subject = module[name]
  tester = run_path(unittest_path)["test"]
  driver = Driver(subject)

  if isinstance(tester, list):
    driver.its_just_data(tester)
  else:
    tester(driver)

  print_driver_results(f"{module_name}::{name}", driver.tests)


def print_driver_results(name, tests):
  print(Style.BRIGHT + name + Style.RESET_ALL)
  for context, test_results in tests.items():
    indent = len(context) * "     "
    print(indent + Fore.CYAN + context[-1] + Style.RESET_ALL)
    for test_result in test_results:
      print(indent + str_result(test_result))


def str_result(result):
  if result["expected"] == result["actual"]:
    return Fore.GREEN + "V " + Style.RESET_ALL + result["title"]
  else:
    return Fore.RED + "X " + result["title"] + Style.RESET_ALL


def match(subject, test):
  return {
    "title": test["it"],
    "expected": test["e"],
    "actual": subject(*test["i"])
  }


class Driver:
  def __init__(self, subject, context=None):
    if context is None:
      context = []
    self.subject = subject
    self.context = context
    self.tests = {}

  def __call__(self, new_context):
    self.context.append(new_context)
    return self

  def __enter__(self):
    return self

  def __exit__(self, type, value, tb):
    self.context.pop()

  def __matmul__(self, test):
    key = tuple(self.context)
    self.tests[key] = self.tests.get(key, []) + [match(self.subject, test)]
    return self

  def its_just_data(self, its_just_data):
    new_context, tests = its_just_data
    with self(new_context):
      for test in tests:
        if isinstance(test, list): # subcontext
          self.its_just_data(test)
        else: # simple test
          self @ test


  def __repr__(self):
    return "Driver(" + repr(self.subject) + ", " + repr(self.context) + ")"
