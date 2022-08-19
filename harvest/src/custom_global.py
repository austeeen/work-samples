"""
    custom_global.py

    this class to exposes methods to be used by "eval" keyword when using a filter.
    for security reasons we want to be as deliberate as possible when exposing "eval".

"""

import re
import json


class CustomGlobal:
    def __init__(self):
        self.__LOCALS_DICT__ = {
            'vp': "vp",
            'PRIVATE': "get_url(PRIVATE, ['PRIVATE'])",
            ... PRIVATE ...
        }

    @staticmethod
    def get_url(vp, views):
        return [next((entry['image_url'] for entry in vp['image_urls']
                     if entry['image_label'] == view), None) for view in views]

    def __get_eval_globals__(self):
        r = {func: getattr(self, func) for func in dir(self) if callable(getattr(self, func)) and
             not func.startswith("__")}
        r['__builtins__'] = None
        r['type'] = type
        return r

    def __get_str__(self):
        return "keywords:\n" + json.dumps(self.__LOCALS_DICT__, indent=2)

    def __set_locals__(self, eval_globals):
        for k, v in self.__LOCALS_DICT__.items():
            try:
                eval_globals[k] = eval(v, eval_globals)
            except KeyError:
                print(f"Custom Global -- warning -- {k}: {v} not in viewport PRIVATE: "
                      f"{eval_globals['PRIVATE']['PRIVATE']}")
                eval_globals[k] = ""
            except TypeError:
                raise KeywordError(self, v, eval_globals)

    def __eval__(self, filter_statement, vp, eval_globals=None):
        eval_globals = self.__get_eval_globals__() if not eval_globals else eval_globals
        eval_globals['vp'] = vp
        self.__set_locals__(eval_globals)
        try:
            return eval(filter_statement, eval_globals)
        except TypeError:
            raise KeywordError(self, filter_statement, eval_globals)


class FilterGlobal(CustomGlobal):
    def __init__(self):
        CustomGlobal.__init__(self)
        self.__LOCALS_DICT__.update({
            'PRIVATE': "PRIVATE",
            'PRIVATE': "get_url(PRIVATE, ['PRIVATE'])",
            ... PRIVATE ...

        })


class KeywordError(Exception):
    def __init__(self, globals_obj, line, eval_globals):
        Exception.__init__(self, self._build_msg(globals_obj, line, eval_globals))

    @staticmethod
    def _build_msg(globals_obj, line, eval_globals):
        words = re.sub(r'([^\w])', ' ', line).split()
        unrec = []
        types = []
        [types.append((e, eval("type({})".format(e), eval_globals)))
         if e in globals_obj.__LOCALS_DICT__ else unrec.append(e) for e in words]
        return f"ERROR: {words} contains an unrecognized keyword or operator or \"{line}\" is an " \
               f"invalid python statement.\n" \
               f"UNRECOGNIZED KEYWORDS: {unrec}\n" \
               f"TYPES: {types}\n" \
               f"use --key-words cmd line option for a list of available keywords."
