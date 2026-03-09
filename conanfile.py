import os
from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout
from conan.tools.files import copy

class VkBootstrapConan(ConanFile):
    name = "vk-bootstrap"
    version = "1.4.344"
    description = "Vulkan bootstraping library."
    license = "MIT"
    topics = ("vulkan", "bootstrap", "setup")
    homepage = "https://github.com/charles-lunarg/vk-bootstrap"
    url = "https://github.com/conan-io/conan-center-index"

    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeToolchain", "CMakeDeps"
    exports_sources = "CMakeLists.txt", "src/*", "gen/*", "LICENSE.txt"

    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "test": [True, False],
        "werror": [True, False],
        "disable_warnings": [True, False],
        "install": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "test": False,
        "werror": False,
        "disable_warnings": False,
        "install": True,
    }

    def requirements(self):
        self.requires("vulkan-headers/1.4.344")

    def build_requirements(self):
        self.tool_requires("cmake/4.0.3")

    def layout(self):
        cmake_layout(self)
   
    def build(self):
        cmake = CMake(self)
        cmake.configure(
            variables={
                "BUILD_SHARED_LIBS": self.options.shared,
                "VK_BOOTSTRAP_INSTALL": self.options.install,
                "VK_BOOTSTRAP_TEST": self.options.test,
                "VK_BOOTSTRAP_WERROR": self.options.werror,
                "VK_BOOTSTRAP_DISABLE_WARNINGS": self.options.disable_warnings,
                "VK_BOOTSTRAP_POSITION_INDEPENDENT_CODE": self.options.get_safe("fPIC", True),
            }
        )
        cmake.build()

    def package(self):
        copy(self, "LICENSE", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["vk-bootstrap"]
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libdirs = ["lib"]
