cmake_minimum_required(VERSION 3.22)

project(
    VulkanBootstrap
    LANGUAGES CXX
    DESCRIPTION "A Vulkan utility library to ease the initialization steps in Vulkan"
    VERSION "1.4.313.0")

option(VK_BOOTSTRAP_POSITION_INDEPENDENT_CODE "Default value is the value of BUILD_SHARED_LIBS" ${BUILD_SHARED_LIBS})

message(STATUS "BUILD_SHARED_LIBS=${BUILD_SHARED_LIBS}")
message(STATUS "VK_BOOTSTRAP_DISABLE_WARNINGS=${VK_BOOTSTRAP_DISABLE_WARNINGS}")
message(STATUS "VK_BOOTSTRAP_WERROR=${VK_BOOTSTRAP_WERROR}")
message(STATUS "VK_BOOTSTRAP_TEST=${VK_BOOTSTRAP_TEST}")
message(STATUS "VK_BOOTSTRAP_INSTALL=${VK_BOOTSTRAP_INSTALL}")
message(STATUS "VK_BOOTSTRAP_POSITION_INDEPENDENT_CODE=${VK_BOOTSTRAP_POSITION_INDEPENDENT_CODE}")

find_package(VulkanHeaders CONFIG)

set(vk-bootstrap-library-type STATIC)
if(BUILD_SHARED_LIBS)
    set(vk-bootstrap-library-type SHARED)
endif()

add_library(
    vk-bootstrap
    ${vk-bootstrap-library-type}
        src/VkBootstrap.cpp
        src/VkBootstrap.h
        src/VkBootstrapDispatch.h
        )

target_compile_features(vk-bootstrap PUBLIC cxx_std_17)

target_include_directories(
    vk-bootstrap
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/src>
        $<INSTALL_INTERFACE:include>
        )

target_link_libraries(
    vk-bootstrap
        PUBLIC
            Vulkan::Headers
        PRIVATE
            ${CMAKE_DL_LIBS})


set_target_properties(
    vk-bootstrap
    PROPERTIES
        POSITION_INDEPENDENT_CODE ${VK_BOOTSTRAP_POSITION_INDEPENDENT_CODE})

# Installation rules
include(GNUInstallDirs)

# Install the library archive
install(
    TARGETS vk-bootstrap
    EXPORT vk-bootstrap-config
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
    )

# Install header files
install(
    DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/src/
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
    FILES_MATCHING PATTERN "*.hpp" PATTERN "*.h"
    )
