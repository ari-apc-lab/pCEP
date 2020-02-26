## Description

pCEP-sim is a visualization of trajectories, trajectory prediction and object collision for the CLASS project. 

It has been developed on Windows (works on 7 and 10) in Visual Studio (2017 and 2019). The current version definetely works on Windows 10 with Visual Studio 2019.

It has a (big) dependency with the IO2D library and you must also install CMake. 

[comment]: # (It also presents a dependency with the [fusion-ukf project](https://github.com/mithi/fusion-ukf).)

Recommended installation (tried and tested):

0. Install Visual Studio: https://visualstudio.microsoft.com/vs/ (select Community 2019, the free version)

1. Follow the installation instructions of this demo:
	https://github.com/cpp-io2d/P0267_RefImpl

	This will install the graphics library needed, together with various samples. 
	In particular, note the Requirements in the readme:

	...
	It also requires vcpkg for installing dependencies - this is described more fully here: Dependency installation instructions.txt.
	...

	I recommend you follow the instructions to install vcpkg and all the dependencies mentioned there (https://raw.githubusercontent.com/mikebmcl/P0267_RefImpl/D0267R7/P0267_RefImpl/P0267_RefImpl/win32/Dependency%20installation%20instructions.txt).

2. Install CMake and generate a Visual Studio Solution for io2d:

	1. Install CMake: https://cmake.org/download/
	2. Generate a Visual Studio solution file for your version of Visual Studio. In order for CMake to find packages installed using vcpkg, pass the vcpkg.cmake file found in $VCPGK_LOCATION/scripts/buildsystems to CMake using the -DCMAKE_TOOLCHAIN_FILE flag. By default CMake will target a x86 architecture, and this will create errors in the linker if we are in a x64 machine. To solve this, pass the following flags to CMake:
	```
	cmake -G "Visual Studio 16 2019" -A "x64" -DVCPKG_TARGET_TRIPLET=x64-windows -DCMAKE_TOOLCHAIN_FILE=$VCPKG_LOCATION/scripts/buildsystems/vcpkg.cmake
	```

3. Load, build and run the solution in Visual Studio.

	Load the io2d solution (mine is here: "C:\dev\CLASS\P0267_RefImpl\Debug\io2d.sln"). I suggest you run the cpu_load project (in case you're not familiar with VS: right click and "Set as Startup Project" and then press F5 to run it) to see if everything worked and then run rocks_in_space and play a bit with a well deserved coffee break. Just make sure your boss isn't watching.

4. Ok, now that the graphics system is working, get this pcep-sim code from the CLASS gitlab and load the solution file pCEP-sim.sln. Right-Click on the project and make sure the folders 

* $P0267REFIMPL\P0267_RefImpl\P0267_RefImpl\cairo\win32
* $P0267REFIMPL\P0267_RefImpl\P0267_RefImpl\cairo
* $P0267REFIMPL\P0267_RefImpl\P0267_RefImpl 

are configured in the "Additional Include Directories" section

	* spiros todo: need to make sure there are no hardcoded paths (except for the io2d stuff) before pushing the code

[comment]: # (, as well as the $FUSION-UKF/src directory)
	
	

## License

Apache 2.0

By downloading this software, the downloader agrees with the specified terms and conditions of the License Agreement and the particularities of the license provided.
