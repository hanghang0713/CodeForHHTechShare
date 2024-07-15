#pragma once

#include <string>

#include "spdlog/spdlog.h"

#include "src/common/filesystem.h"  // IWYU pragma: keep

//////////////////////////////////////////////////////////////////////
///                                                                 //
// 平台相关的函数定义，实现在 src/common/{windows,linux}/log.cpp 中 //
///                                                                 //
//////////////////////////////////////////////////////////////////////

/**
 * 由每个exe的main.cpp实现，用于区分log.txt的目录
 */
std::string GetExeName();

/**
 * 返回日志文件路径
 */
fs::path GetLogDir();

/**
 * 初始化日志系统
 */
spdlog::logger* GetDefaultLogger();

/**
 * 打印第一眼不需要看到的日志
 * 这里的日志用来辅助定位问题
 */
spdlog::logger* GetTraceLogger();

////////////////////////////////////////////
//                                        //
// 以下的宏，把日志打印到默认的日志存储区 //
//                                        //
////////////////////////////////////////////

#define LOGI(F, ...) SPDLOG_LOGGER_CALL(GetDefaultLogger(), spdlog::level::info, FMT_STRING(F), ##__VA_ARGS__)
#define LOGW(F, ...) SPDLOG_LOGGER_CALL(GetDefaultLogger(), spdlog::level::warn, FMT_STRING(F), ##__VA_ARGS__)
#define LOGE(F, ...) SPDLOG_LOGGER_CALL(GetDefaultLogger(), spdlog::level::err, FMT_STRING(F), ##__VA_ARGS__)
#define LOGC(F, ...) SPDLOG_LOGGER_CALL(GetDefaultLogger(), spdlog::level::critical, FMT_STRING(F), ##__VA_ARGS__)
#define LOGD(F, ...) SPDLOG_LOGGER_CALL(GetDefaultLogger(), spdlog::level::debug, FMT_STRING(F), ##__VA_ARGS__)
#define LOGT(F, ...) SPDLOG_LOGGER_CALL(GetTraceLogger(), spdlog::level::trace, FMT_STRING(F), ##__VA_ARGS__)
