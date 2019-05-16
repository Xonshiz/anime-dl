#!/usr/bin/env python
# -*- coding: utf-8 -*-


def duplicate_remover(seq):
    # https://stackoverflow.com/a/480227
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]
