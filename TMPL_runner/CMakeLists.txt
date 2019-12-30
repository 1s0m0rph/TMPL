cmake_minimum_required(VERSION 3.15)
project(TMPL_runner)

set(CMAKE_CXX_STANDARD 14)

add_executable(TMPL_runner main.cpp TM.cpp TM.h FileReader.cpp FileReader.h)