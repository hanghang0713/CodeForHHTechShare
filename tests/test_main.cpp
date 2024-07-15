#define CATCH_CONFIG_RUNNER

#include "catch2/catch.hpp"

#include "src/common/config.h"

std::string GetExeName() {
    return CODE_FOR_TECH_SHARE_SERVICE_NAME "Test";
}

int main(int argc, char* argv[]) {
    Catch::Session session;

    int returnCode = session.applyCommandLine(argc, argv);
    if (returnCode != 0) {
        return returnCode;
    }

    return session.run();
}
