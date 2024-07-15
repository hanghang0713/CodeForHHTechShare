#include "src/common/log.h"

#include <chrono>

#include "src/common/config.h"

#include "spdlog/sinks/rotating_file_sink.h"

#define DEFAULT_LOGGER_NAME CODE_FOR_TECH_SHARE_SERVICE_NAME "-DEFAULT"
#define AGGREGATE_LOGGER_NAME CODE_FOR_TECH_SHARE_SERVICE_NAME "-AGGREGATE"
#define TRACE_LOGGER_NAME CODE_FOR_TECH_SHARE_SERVICE_NAME "-TRACE"

namespace {

using namespace std::chrono_literals;

std::shared_ptr<spdlog::logger> SetupDefaultLogger() {
    std::shared_ptr<spdlog::logger> logger = nullptr;

#ifdef SERVICE_DEBUG
    logger = spdlog::default_logger();
#else
    constexpr auto size = 1048576 * 5;  // 5M
    auto fname = GetLogDir() / "log.txt";
    logger = spdlog::rotating_logger_mt(DEFAULT_LOGGER_NAME, PathToString(fname), size, 3);
#endif

    logger->set_level(spdlog::level::info);
    logger->flush_on(spdlog::level::warn);
    logger->set_pattern("%^[%m-%d %T:%e][%L][%P:%-5t][%s:%#] %v%$");

    spdlog::flush_every(3s);

    return logger;
}

std::shared_ptr<spdlog::logger> SetupTraceLogger() {
    std::shared_ptr<spdlog::logger> logger = nullptr;

#ifdef SERVICE_DEBUG
    logger = spdlog::default_logger();
#else
    constexpr auto size = 1048576 * 5;  // 5M
    auto fname = GetLogDir() / "poll.txt";
    logger = spdlog::rotating_logger_mt(TRACE_LOGGER_NAME, PathToString(fname), size, 1);
#endif

    logger->set_level(spdlog::level::trace);
    logger->flush_on(spdlog::level::warn);
    logger->set_pattern("%^[%m-%d %T:%e][%L][%P:%-5t][%s:%#] %v%$");

    spdlog::flush_every(3s);

    return logger;
}

}  // namespace

spdlog::logger* GetDefaultLogger() {
    static auto default_logger = SetupDefaultLogger();

    static std::once_flag once;
    std::call_once(once, [] {
        spdlog::set_default_logger(default_logger);
        spdlog::flush_every(3s);
    });

    return default_logger.get();
}

#ifdef SERVICE_DEBUG

spdlog::logger* GetTraceLogger() {
    return GetDefaultLogger();
}

#else

spdlog::logger* GetTraceLogger() {
    static auto trace_logger = SetupTraceLogger();
    return trace_logger.get();
}

#endif

fs::path GetLogDir() {
    auto dir = fs::path(R"(C:\ProgramData\)") / CODE_FOR_TECH_SHARE_SERVICE_NAME / GetExeName();
    if (!fs::exists(dir)) {
        fs::create_directories(dir);
    }

    return dir;
}
