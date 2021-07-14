# -*- coding: utf-8 -*-

import replace_vc

# def callback(a, b):
#     print('Sum = {0}'.format(a+b))

def main(callback=None):
    print('Add any two digits.')
    if callback != None:
        callback(1, 2)

main(replace_vc.callback)