#!/usr/bin/env python
# -*- encoding=utf8 -*-
# @author '2009 Hsin Yi Chen (陳信屹) <ossug.hychen@gmail.com>'

# i18n name mapping.
_i18n_name = {}
_i18n_name['zhTW'] = {
    'Productivity':'辦公軟體',
    'Multimedia':'多媒體',
    'Game':'遊戲',
    'Networking':'網路',
    'Graphic':'圖像處理',
    'Entertain':'娛樂', 
    'Localization':'本地化',
    'Customize':'客制化'
    }


class Category(object):

    def __init__(self, name, scripts_builder):
        """
        category data object

        @param str name category name.
        @param obj ScriptsBuilder a builder that can make scripts instace.
        """
        self.lang = 'zhTW'
        self.name = _i18n_name[self.lang][name]
        self._entries = []
        self._items = {}
        self._scripts_builder = scripts_builder

    def _lazyinit_scripts(self):
        "lazy initialize Script instance."
        if not self._items:
            self._scripts_builder.entries = self._entries
            self._items = self._scripts_builder.make_scripts()

    def add_entry(self, entry):
        "add entry information from scripts.list."
        self._entries.append(entry)


    def items(self):
        """get scripts."""
        self._lazyinit_scripts()
        return self._items.values()

    def get(self, obj_id):
        self._lazyinit_scripts()
        return self._items.get(obj_id)
