# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.15

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /home/Isomorph/Downloads/CLion-2019.3.2/clion-2019.3.2/bin/cmake/linux/bin/cmake

# The command to remove a file.
RM = /home/Isomorph/Downloads/CLion-2019.3.2/clion-2019.3.2/bin/cmake/linux/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/Isomorph/Documents/lab/TMPL/TMPL_runner

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/Isomorph/Documents/lab/TMPL/TMPL_runner/cmake-build-debug

# Include any dependencies generated for this target.
include CMakeFiles/TMPL_runner.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/TMPL_runner.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/TMPL_runner.dir/flags.make

CMakeFiles/TMPL_runner.dir/main.cpp.o: CMakeFiles/TMPL_runner.dir/flags.make
CMakeFiles/TMPL_runner.dir/main.cpp.o: ../main.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/Isomorph/Documents/lab/TMPL/TMPL_runner/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/TMPL_runner.dir/main.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/TMPL_runner.dir/main.cpp.o -c /home/Isomorph/Documents/lab/TMPL/TMPL_runner/main.cpp

CMakeFiles/TMPL_runner.dir/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/TMPL_runner.dir/main.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/Isomorph/Documents/lab/TMPL/TMPL_runner/main.cpp > CMakeFiles/TMPL_runner.dir/main.cpp.i

CMakeFiles/TMPL_runner.dir/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/TMPL_runner.dir/main.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/Isomorph/Documents/lab/TMPL/TMPL_runner/main.cpp -o CMakeFiles/TMPL_runner.dir/main.cpp.s

CMakeFiles/TMPL_runner.dir/TM.cpp.o: CMakeFiles/TMPL_runner.dir/flags.make
CMakeFiles/TMPL_runner.dir/TM.cpp.o: ../TM.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/Isomorph/Documents/lab/TMPL/TMPL_runner/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object CMakeFiles/TMPL_runner.dir/TM.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/TMPL_runner.dir/TM.cpp.o -c /home/Isomorph/Documents/lab/TMPL/TMPL_runner/TM.cpp

CMakeFiles/TMPL_runner.dir/TM.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/TMPL_runner.dir/TM.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/Isomorph/Documents/lab/TMPL/TMPL_runner/TM.cpp > CMakeFiles/TMPL_runner.dir/TM.cpp.i

CMakeFiles/TMPL_runner.dir/TM.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/TMPL_runner.dir/TM.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/Isomorph/Documents/lab/TMPL/TMPL_runner/TM.cpp -o CMakeFiles/TMPL_runner.dir/TM.cpp.s

CMakeFiles/TMPL_runner.dir/FileReader.cpp.o: CMakeFiles/TMPL_runner.dir/flags.make
CMakeFiles/TMPL_runner.dir/FileReader.cpp.o: ../FileReader.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/Isomorph/Documents/lab/TMPL/TMPL_runner/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building CXX object CMakeFiles/TMPL_runner.dir/FileReader.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/TMPL_runner.dir/FileReader.cpp.o -c /home/Isomorph/Documents/lab/TMPL/TMPL_runner/FileReader.cpp

CMakeFiles/TMPL_runner.dir/FileReader.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/TMPL_runner.dir/FileReader.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/Isomorph/Documents/lab/TMPL/TMPL_runner/FileReader.cpp > CMakeFiles/TMPL_runner.dir/FileReader.cpp.i

CMakeFiles/TMPL_runner.dir/FileReader.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/TMPL_runner.dir/FileReader.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/Isomorph/Documents/lab/TMPL/TMPL_runner/FileReader.cpp -o CMakeFiles/TMPL_runner.dir/FileReader.cpp.s

# Object files for target TMPL_runner
TMPL_runner_OBJECTS = \
"CMakeFiles/TMPL_runner.dir/main.cpp.o" \
"CMakeFiles/TMPL_runner.dir/TM.cpp.o" \
"CMakeFiles/TMPL_runner.dir/FileReader.cpp.o"

# External object files for target TMPL_runner
TMPL_runner_EXTERNAL_OBJECTS =

TMPL_runner: CMakeFiles/TMPL_runner.dir/main.cpp.o
TMPL_runner: CMakeFiles/TMPL_runner.dir/TM.cpp.o
TMPL_runner: CMakeFiles/TMPL_runner.dir/FileReader.cpp.o
TMPL_runner: CMakeFiles/TMPL_runner.dir/build.make
TMPL_runner: CMakeFiles/TMPL_runner.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/Isomorph/Documents/lab/TMPL/TMPL_runner/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Linking CXX executable TMPL_runner"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/TMPL_runner.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/TMPL_runner.dir/build: TMPL_runner

.PHONY : CMakeFiles/TMPL_runner.dir/build

CMakeFiles/TMPL_runner.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/TMPL_runner.dir/cmake_clean.cmake
.PHONY : CMakeFiles/TMPL_runner.dir/clean

CMakeFiles/TMPL_runner.dir/depend:
	cd /home/Isomorph/Documents/lab/TMPL/TMPL_runner/cmake-build-debug && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/Isomorph/Documents/lab/TMPL/TMPL_runner /home/Isomorph/Documents/lab/TMPL/TMPL_runner /home/Isomorph/Documents/lab/TMPL/TMPL_runner/cmake-build-debug /home/Isomorph/Documents/lab/TMPL/TMPL_runner/cmake-build-debug /home/Isomorph/Documents/lab/TMPL/TMPL_runner/cmake-build-debug/CMakeFiles/TMPL_runner.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/TMPL_runner.dir/depend

