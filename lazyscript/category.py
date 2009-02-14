class Category(object):

    def __init__(self, name, scripts_builder):
        """
        category data object

        @param str name category name.
        @param obj ScriptsBuilder a builder that can make scripts instace.
        """
        self.name = name
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
