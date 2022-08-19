cmake_minimum_required (VERSION 3.5)
project (Analyzer CXX)

set (${PROJECT_NAME}_VERSION_MAJOR 0)
set (${PROJECT_NAME}_VERSION_MINOR 1)
set (CMAKE_CXX_STANDARD 14)
set (CMAKE_CXX_FLAGS "-Wall -O3 -g ${CMAKE_CXX_FLAGS}")
set (CMAKE_CXX_FLAGS "-L../src/SD -I./SD -DNO_WINDOWS_PATH -DMAGICKCORE_HDRI_ENABLED=0 -DMAGICKCORE_QUANTUM_DEPTH=16 ${CMAKE_CXX_FLAGS}")

find_package (HIREDIS REQUIRED)
find_package (JPEG REQUIRED)

include(FindPkgConfig)

file(GLOB SOURCES "*.cpp")

add_executable(${PROJECT_NAME} ${SOURCES})
include_directories(${JPEG_INCLUDE_DIR})
target_link_libraries (${PROJECT_NAME} hiredis id_FlexRelease_linux_x64.so dl m ${JPEG_LIBRARIES})
