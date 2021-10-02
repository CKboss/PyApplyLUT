project("CPPLUT")

cmake_minimum_required(VERSION 3.21)

add_compile_options(/openmp)

set(EIGEN_DIR "D:/Developments/eigen-3.4.0/")
include_directories(${EIGEN_DIR})

include_directories(./cpp)

set(PyBind11_DIR "D:/Developments/pybind11-2.7.1/")
include_directories("D:/Developments/pybind11-2.7.1/include")
add_subdirectory(${PyBind11_DIR} build)

pybind11_add_module(ApplyLUT cpp/ApplyLUT.cpp)