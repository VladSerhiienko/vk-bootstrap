import os
from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout
from conan.tools.files import copy

class VkBootstrapConan(ConanFile):
    name = "vk-bootstrap"
    version = "1.4.313.0"
    description = "Vulkan bootstraping library."
    license = "MIT"
    topics = ("vulkan", "bootstrap", "setup")
    homepage = "https://github.com/charles-lunarg/vk-bootstrap"
    url = "https://github.com/conan-io/conan-center-index"

    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeToolchain", "CMakeDeps"
    exports_sources = "CMakeLists.txt", "*.h", "*.cpp", "LICENSE.txt"

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
        cmake.install()

    def layout(self):
        cmake_layout(self)

    def requirements(self):
        self.requires(f"vulkan-headers/{self.version}")

    def build_requirements(self):
        self.tool_requires("cmake/4.0.3")

    def package(self):
        # self.output.info(f"source_folder: {self.source_folder}")
        # self.output.info(f"build_folder: {self.build_folder}")
        # self.output.info(f"package_folder: {self.package_folder}")
        copy(self, "LICENSE", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        copy(self, pattern="*.h", src=self.source_folder, dst=os.path.join(self.package_folder, "include"))
        copy(self, pattern="*.a", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        copy(self, pattern="*.so", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        copy(self, pattern="*.lib", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        copy(self, pattern="*.dll", src=self.build_folder, dst=os.path.join(self.package_folder, "bin"), keep_path=False)
        copy(self, pattern="*.dylib", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)

    def package_info(self):
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.bindirs = ["bin"]
        self.cpp_info.libs = ["vk-bootstrap"]
