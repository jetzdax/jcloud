import logging
import os.path
import yaml
import jinja2.exceptions
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from jcloud.errors import ParamError
from jcloud.cloud import JCloudService

logger = logging.getLogger(__package__)

class JCloudCore(object):

    Commands = [
        dict(command="render", help="Render the CFN template"),
        dict(command="create", help="Create the stack using the CFN template"),
        dict(command="update", help="Update an existing stack"),
        dict(command="delete", help="Delete the stack"),
    ]

    @classmethod
    def help(cls, prop):
        if prop == "command":
            return [cmd['command'] for cmd in cls.Commands]
        if prop == "help":
            return ["{command}: {help}".format(**cmd) for cmd in cls.Commands]
        return ""

    def __init__(self, args, **kwargs):
        """ Construct a JCloudCore object.

        :param args: a Namespace object that is produced from argparse (see cmdline.py)
        :param kwargs: additional optional settings
        """
        self._args = args
        self._config = None
        self._cloud_service = JCloudService(args)
        self._params = {}

    def _load_config(self):
        if os.path.isfile(self._args.config):
            # Load config
            self._config = yaml.safe_load(open(self._args.config))

    def get_config(self, key, default=None):
        return self._config.get(key, default) if self._config else default

    def _get_param_file(self, param):
        param_dir = self.get_config('params-dir', '')
        param_file = os.path.join(param_dir, param)
        if os.path.isfile(param_file):
            return param_file
        elif not param.endswith('.yaml'):
            # Try it with the yaml extension.
            param_file = os.path.join(param_dir, "{}.yaml".format(param))
            if os.path.isfile(param_file):
                return param_file
        return None  # does not exist

    def _load_params(self):
        # Load parameters files
        self._params = {}
        params_list = self.get_config("common-params", [])
        if self._args.params:
            params_list += self._args.params.split(',')
        for param in params_list:
            param_file = self._get_param_file(param)
            if not param_file:
                raise ParamError("Unable to load the parameters file '{}' or '{}.yaml'".format(param, param))
            params = yaml.safe_load(open(param_file))
            self._params.update(params)

    def _get_input_file(self):
        if not os.path.isfile(self._args.input):
            raise ParamError("Unable to find input file '{}'".format(self._args.input))
        return self._args.input

    def _render_jinja2(self):
        env = Environment(
            loader=FileSystemLoader('.'),
            undefined=StrictUndefined,  # or use undefined=Undefined to allow
            )
        input_template = env.get_template(self._get_input_file())
        return input_template.render(**self._params)

    def execute(self):
        self._load_config()
        self._load_params()
        # Execute the function by the same name as the command.
        getattr(self, "execute_" + self._args.execute)()

    def execute_render(self):
        print(self._render_jinja2())

    def execute_create(self):
        self._cloud_service.create_cloud()

    def execute_update(self):
        self._cloud_service.update_cloud()

    def execute_delete(self):
        self._cloud_service.delete_cloud()
