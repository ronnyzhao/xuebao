"""
please visit https://github.com/niutool/xuebao
for more detail
"""

import logging

class Brain(object):
    def __init__(self, config):
        """
        Instantiates a new Brain object, which cross-references user
        input with a list of modules. Note that the order of brain.modules
        matters, as the Brain will return the first module
        that accepts a given input.
        """

        self._plugins = []
        self._logger = logging.getLogger(__name__)
        self._config = config

    def add_plugin(self, plugin):
        self._plugins.append(plugin)
        self._plugins = sorted(
            self._plugins, key=lambda p: p.get_priority(), reverse=True)

    def get_plugins(self):
        return self._plugins

    def get_standard_phrases(self):
        return []

    def get_plugin_phrases(self):
        """
        Gets phrases from all plugins.

        Returns:
            A list of phrases from all plugins.
        """
        phrases = []

        for plugin in self._plugins:
            phrases.extend(plugin.get_phrases())

        return sorted(list(set(phrases)))

    def get_all_phrases(self):
        """
        Gets a combined list consisting of standard phrases and plugin phrases.

        Returns:
            A list of phrases.
        """
        return self.get_standard_phrases() + self.get_plugin_phrases()

    def query(self, texts):
        """
        Passes user input to the appropriate module, testing it against
        each candidate module's isValid function.

        Arguments:
        text -- user input, typically speech, to be parsed by a module

        Returns:
            A tuple containing a text and the module that can handle it
        """
        for plugin in self._plugins:
            for text in texts:
                if plugin.is_valid(text):
                    self._logger.debug("'%s' is a valid phrase for module " +
                                       "'%s'", text, plugin.info.name)
                    return (plugin, text)
        self._logger.debug("No module was able to handle any of these " +
                           "phrases: %r", texts)
        return (None, None)

