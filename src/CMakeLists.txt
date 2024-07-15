set(EXCUTABLE_NAME ${PROJECT_NAME} CACHE INTERNAL "")

# 这几个库在 APP 和测试用例中都会用到，在这里做 CACHE
# 避免两个模块之间的 CMake 文件出现重复
set(LIBRARY_NAME ${EXCUTABLE_NAME}-lib CACHE INTERNAL "")

set(PLATFORM_LIBS Setupapi CACHE INTERNAL "")

# ############
# LIBRARY  #
# ############
add_library(${LIBRARY_NAME} STATIC

)

target_sources(${LIBRARY_NAME} PRIVATE
    ./common/log.cpp
)

# ############
# EXCUTABLE #
# ############
add_executable(${EXCUTABLE_NAME}
    ./main.cpp
)

set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} /Zi")
set(CMAKE_EXE_LINKER_FLAGS_RELEASE "${CMAKE_EXE_LINKER_FLAGS_RELEASE} /DEBUG /OPT:REF /OPT:ICF")

target_link_libraries(${EXCUTABLE_NAME} ${PLATFORM_LIBS} ${LIBRARY_NAME} ${CONAN_LIBS})

install(TARGETS ${EXCUTABLE_NAME}
    RUNTIME DESTINATION bin
    ARCHIVE DESTINATION lib)
