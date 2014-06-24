# -*- coding: utf-8 -*-
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import abc
import six
import logging

from st2client.formatters import doc


LOG = logging.getLogger(__name__)


@six.add_metaclass(abc.ABCMeta)
class Branch(object):
    """Represents a branch of related commands in the command tree."""

    def __init__(self, name, description, subparsers, parent_parser=None):
        self.name = name
        self.description = description
        self.parent_parser = parent_parser
        self.parser = subparsers.add_parser(self.name,
                                            description=self.description,
                                            help=self.description,
                                            add_help=False)
        self.commands = dict()


@six.add_metaclass(abc.ABCMeta)
class Command(object):
    """Represents a commandlet in the command tree."""

    def __init__(self, name, description, subparsers, parent_parser=None):
        self.name = name
        self.description = description
        self.parent_parser = parent_parser
        self.parser = subparsers.add_parser(self.name,
                                            description=self.description,
                                            help=self.description,
                                            add_help=False)
        self.parser.set_defaults(func=self.run)

    @abc.abstractmethod
    def run(self, args):
        """
        This method is invoked when the corresponding command is executed
        from the command line.
        """
        raise NotImplementedError

    def format_output(self, subject, formatter, *args, **kwargs):
        json = kwargs.get('json', False)
        func = doc.Json.format if json else formatter.format
        return func(subject, *args, **kwargs)

    def print_output(self, subject, formatter, *args, **kwargs):
        output = self.format_output(subject, formatter, *args, **kwargs)
        print output
        print
