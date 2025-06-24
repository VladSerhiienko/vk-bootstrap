from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout

class VkBootstrapConan(ConanFile):
    name = "vk-bootstrap"
    version = "1.4.313.0"
    description = "Vulkan bootstraping library."
    license = "MIT"
    topics = ("vulkan", "bootstrap", "setup")
    homepage = "https://github.com/charles-lunarg/vk-bootstrap"
    url = "https://github.com/conan-io/conan-center-index"

    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeToolchain", "CMakeDeps", "AutotoolsToolchain", "PkgConfigDeps", "XcodeDeps"

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
        "install": False,
    }
   
    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def layout(self):
        cmake_layout(self)

    def requirements(self):
        self.requires(f"vulkan-headers/{self.version}")

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["BUILD_SHARED_LIBS"] = self.options.shared
        tc.variables["VK_BOOTSTRAP_INSTALL"] = self.options.install
        tc.variables["VK_BOOTSTRAP_TEST"] = self.options.test
        tc.variables["VK_BOOTSTRAP_WERROR"] = self.options.werror
        tc.variables["VK_BOOTSTRAP_DISABLE_WARNINGS"] = self.options.disable_warnings
        tc.variables["VK_BOOTSTRAP_POSITION_INDEPENDENT_CODE"] = self.options.fPIC
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()
