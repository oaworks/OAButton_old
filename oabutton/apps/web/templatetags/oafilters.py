# -*- coding: utf-8 -*-

import pyjade


@pyjade.register_filter('label_with_classes')
def label_with_classes(value, arg):
    return value.label_tag(attrs={'class': arg})
