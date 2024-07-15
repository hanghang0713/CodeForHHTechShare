set(TEST_EXCUTABLE_NAME ${PROJECT_NAME}Test)

add_executable(${TEST_EXCUTABLE_NAME}
    ./test_main.cpp
    ./basic/test_unique_ptr.cpp
)

# PLATFORM_LIBS 和 LIBRARY_NAME 定义在 src/CMakeLists.txt 中
target_link_libraries(${TEST_EXCUTABLE_NAME} ${PLATFORM_LIBS} ${LIBRARY_NAME} ${CONAN_LIBS})


if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    install(TARGETS ${TEST_EXCUTABLE_NAME}
        RUNTIME DESTINATION bin
        ARCHIVE DESTINATION lib)
endif()
