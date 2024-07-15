#pragma once

#ifdef _WIN32

#include <filesystem>

namespace fs = std::filesystem;

inline std::string PathToString(const fs::path& path) {
    return path.u8string();
}

#else

// LINUX 系统上 filesystem 没有实现 create_directories
#include "boost/filesystem.hpp"
namespace fs = boost::filesystem;

inline std::string PathToString(const fs::path& path) {
    return path.string();
}

#endif
