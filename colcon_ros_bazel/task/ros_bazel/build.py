# Copyright 2018 Mickael Gaillard
# Licensed under the Apache License, Version 2.0


from colcon_bazel.task.bazel.build import BazelBuildTask
from colcon_core.logging import colcon_logger
from colcon_core.plugin_system import satisfies_version
from colcon_core.task import TaskExtensionPoint

logger = colcon_logger.getChild(__name__)


class RosBazelBuildTask(TaskExtensionPoint):
    """Build ROS bazel packages."""

    def __init__(self):  # noqa: D107
        super().__init__()
        satisfies_version(TaskExtensionPoint.EXTENSION_POINT_VERSION, '^1.0')

    def add_arguments(self, *, parser):  # noqa: D102
        pass
#        parser.add_argument(
#            '--bazel-args',
#            nargs='*', metavar='*', type=str.lstrip,
#            help='Pass arguments to Bazel projects. '
#            'Arguments matching other options must be prefixed by a space,\n'
#            'e.g. --bazel-args " --help"')
#        parser.add_argument(
#            '--bazel-task',
#            help='Run a specific task instead of the default task')

    async def build(  # noqa: D102
        self, *, additional_hooks=None, skip_hook_creation=False
    ):
        args = self.context.args
        logger.info(
            "Building ROS package in '{args.path}' with build type 'ros.bazel'"
            .format_map(locals()))

        # reuse bazel build task with additional logic.
        extension = BazelBuildTask()
        extension.set_context(context=self.context)

        return await extension.build()
