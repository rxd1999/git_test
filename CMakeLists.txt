cmake_minimum_required(VERSION 3.16)
project(test)
include_directories(
    ./lib
)
add_subdirectory(lib)
add_library(test1 main.cpp)
add_executable(test main.cpp)
target_link_libraries(
    test
    lib
)