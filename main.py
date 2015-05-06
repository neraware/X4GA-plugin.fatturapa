#!/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         main.py
# Author:       marcel
# Created:      2013/07/03
# Copyright:    Astra S.r.l.
# ------------------------------------------------------------------------------

if __name__ == '__main__':
    import Env
    Env.LoadPlugin('fatturapa')
    import x4ga
    x4ga.Main()