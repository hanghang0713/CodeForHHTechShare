if(WIN32)
    set(MINI_VERSION 3.15.0)
else()
    set(MINI_VERSION 3.13.0)
endif()

cmake_minimum_required(VERSION ${MINI_VERSION})
project(CodeForHHTechShare)

# conan
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

# include header
include_directories(${PROJECT_SOURCE_DIR})

# c++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# setup version
if(NOT "$ENV{CODE_FOR_HHTECHSHARE_VERSION}" STREQUAL "")
    add_compile_definitions(CODE_FOR_HHTECHSHARE_VERSION="$ENV{CODE_FOR_HHTECHSHARE_VERSION}")
    message("=== Version Defined as $ENV{CODE_FOR_HHTECHSHARE_VERSION} ===")
else()
    add_compile_definitions(CODE_FOR_HHTECHSHARE_VERSION="U.0.0.0.0")
endif()

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug ... FORCE)
endif()

if(CMAKE_BUILD_TYPE STREQUAL "Release")
    message("=== Release Build ===")
else()
    message("=== Debug Build ===")
    add_compile_definitions(SERVICE_DEBUG)
endif()

add_compile_options("$<$<C_COMPILER_ID:MSVC>:/utf-8>")
add_compile_options("$<$<CXX_COMPILER_ID:MSVC>:/utf-8>")
add_definitions(-D_WIN32_WINNT=0x0601)
add_definitions(-D_CRT_SECURE_NO_WARNINGS)
add_definitions(-D_SILENCE_ALL_CXX17_DEPRECATION_WARNINGS)

add_definitions(-DBOOST_SYSTEM_USE_UTF8) # 使用 UTF-8 编码

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /bigobj")
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} /ignore:4099")
set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")

set(CMAKE_INSTALL_PREFIX ${PROJECT_SOURCE_DIR}/out)

option(STATIC_CHECK "Static Check" OFF)

if(STATIC_CHECK)
    message("--: enable clang-tidy")
    set(CMAKE_CXX_CLANG_TIDY clang-tidy -checks=-*,readability-*)
endif()

add_subdirectory(./src)

if(BUILD_TESTS)
    add_subdirectory(./tests)
endif()

