# Copyright 2018 Mickael Gaillard
# Licensed under the Apache License, Version 2.0


from colcon_bazel.task.bazel.test import BazelTestTask
from colcon_core.logging import colcon_logger
from colcon_core.plugin_system import satisfies_version
from colcon_core.task import TaskExtensionPoint

logger = colcon_logger.getChild(__name__)


class RosBazelTestTask(TaskExtensionPoint):
    """Test ROS bazel packages."""

    def __init__(self):  # noqa: D107
        super().__init__()
        satisfies_version(TaskExtensionPoint.EXTENSION_POINT_VERSION, '^1.0')

    def add_arguments(self, *, parser):  # noqa: D102
        pass
#        parser.add_argument(
#            '--bazeltest-args',
#            nargs='*', metavar='*', type=str.lstrip,
#            help='Pass arguments to Bazel projects. '
#            'Arguments matching other options must be prefixed by a space,\n'
#            'e.g. --bazeltest-args " --help"')
#        parser.add_argument(
#            '--ros-bazel-task',
#            help='Run a specific task instead of the default task')

    async def test(self, *, additional_hooks=None):  # noqa: D102
        args = self.context.args
        logger.info(
            "Testing ROS package in '{args.path}' with build type "
            "'ros.bazel'".format_map(locals()))

        # reuse bazel test task
        extension = BazelTestTask()

        extension.set_context(context=self.context)

        return await extension.test()
