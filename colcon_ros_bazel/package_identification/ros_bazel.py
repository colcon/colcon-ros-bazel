# Copyright 2018 Mickael Gaillard
# Licensed under the Apache License, Version 2.0


import copy

from colcon_core.package_identification \
    import PackageIdentificationExtensionPoint
from colcon_core.plugin_system import satisfies_version
from colcon_bazel.package_identification.bazel import extract_data
from colcon_ros.package_identification.ros import RosPackageIdentification


class RosBazelPackageIdentification(PackageIdentificationExtensionPoint):
    """
    Identify ROS bazel packages with `package.xml` and `BUILD.bazel` files.
    """

    # the priority needs to be higher than the ROS extensions identifying
    # packages using the build systems supported by ROS bazel.
    PRIORITY = 160

    def __init__(self):  # noqa: D107
        super().__init__()
        satisfies_version(
            PackageIdentificationExtensionPoint.EXTENSION_POINT_VERSION,
            '^1.0')

    def identify(self, desc):  # noqa: D102
        if desc.type is not None and desc.type != 'ros.bazel':
            return

        # Preserving the state of the package descriptor so as not to overload
        # the build type is a "common", one like "cmake".
        tmp_desc = copy.deepcopy(desc)

        # Call ROS package identification extension.
        ros_extension = RosPackageIdentification()
        ros_extension.identify(tmp_desc)

        # Validate that is ROS bazel package.
        if tmp_desc.type != 'ros.bazel':
            return

        # Call bazel package identification extension
        # (for append bazel logic).
        data = extract_data(tmp_desc.path)

        # Validate that is bazel package logic.
        if data['name'] == None:
            return

        # Add dependencies.
        tmp_desc.dependencies['build'] |= data['depends']['build']
        tmp_desc.dependencies['run'] |= data['depends']['run']
        tmp_desc.dependencies['test'] |= data['depends']['test']

        # Update package descriptor instance (if has valid build type).
        desc.type = tmp_desc.type
        desc.name = tmp_desc.name
        desc.dependencies = tmp_desc.dependencies
        desc.hooks = tmp_desc.hooks
        desc.metadata = tmp_desc.metadata
