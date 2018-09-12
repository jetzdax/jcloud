import logging

logger = logging.getLogger(__package__)

class JCloudService(object):

    def __init__(self, args, **kwargs):
        """ Construct a JCloudService object.

        :param args: a Namespace object that is produced from argparse (see cmdline.py)
        :param kwargs: additional optional settings
        """
        self._args = args

    def create_cloud(self):
        print("CREATE CLOUD!!!")

    def update_cloud(self):
        print("UPDATE CLOUD!!!")

    def delete_cloud(self):
        print("DELETE CLOUD!!!")
