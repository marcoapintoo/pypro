# What's pypro?

In a few terms, PyPro is a Python Project Organizer. The idea behind this library is 
to create a boilerplate for a common Python application, helping with the common activities related:

* Processing PyQt/PySide, Cython files to their equivalent interface with Python.
* Creating a boilerplate directory structure for a project.
* Handling conversion to standalone executables.

# Command line options

    PyPro | Pinto's Python Project Manager.
    
    Usage:
    
        pypro create <name> from <author>
        pypro requirements add <name> [<version>]
        pypro requirements import all
        pypro update [qt | cython]
        pypro debug 
        pypro show [problems | version | dependencies]  
        pypro pack [linux|windows]
        pypro release <version>
        pypro publish [git | pypi]


# Tasks made by PyPro

From my [little] experience: my point is we spend so much time in secondary terms.

## 1. File processing

If you are worked with PyQt/PySide or with Cython, you know that running an application is not easy like:
   
    python application.py
   
No! Before do this, we need to execute other commands. By example:

    pyside-qrc common_resource.qrc
    cython cython_script.pyx
    gcc -o cython_script cython_script.c
    ...
    pyside application.py

PyPro tries to automatize this actions, detecting and executing the correspondent compiler/converter to each file.
In the first case:

    ./pypro update qt       #At creating the project, PyPro asked which library we use: Qt or PySide.
    ./pypro update cython
    

## 2. Project skeleton

Who was trying to start a Python project knowing it will be grow and grow? Many of us, I think.
Well, I found a little trouble: if a select a bad structure, I will need to fix it, maybe not now,
but I will need to change in a moment, and this will be not comfortable
when the project are evolve into an undebuggable monster.  

PyPro propose a base structure, that can be useful to a generic purpose project:

    root-project/
        build/
        project_name/
        dist/       Executable binaries in testing process.
        docs/       Project documentation
        lib/        Libraries external to the project.
        release/    Executable binaries ready to release as stable versions.
        share/      External resources (not code) we well need in the project.
            help/       Project help files (if we add some to the users)
        test/       Testing and example scripts will be here.
        README.md   Obviously, a starting help for other developers.
        TODO.md     Task to do. In my case, many unfinished... XD
        LICENSE     Distribution license.
        __init__.py Main script to be called if the project is used as library
        
Lib directory is a little special. We copy the Python libraries here,
if we do not want to install other libraries in the computer, 
or we need to use some of them, but modified or debugged and we
do not want to break other applications (this is my common case: the advantage of Open Source!).

Share path is other special case. Think: we code an application we know will be packed into a binary file,
but this program sometimes will need to open a file that won't be embedded in the executable.
Where this files need to be in the project? That are not code, there's no reason to mix them with the common code.
PyPro suggest to put them in a separate folder called "shared", in the testing/releasing time, 
that will be copied next to the application.

### Licensing

And a little words about license file, why do we need it? We are coding "open source"
(I hope that, I really want to hope that), and the result of our work could be shared with others.
There is a lot of kind of licenses. But If I want to create a real project, I need to define what
kind of freedom with my project I allow to do. This file is destined to establish that. In a general
case, I'm inclined to MIT license. What is telling this little archive with this license?

* If someone wants to use your code, he/she is allowed to do.
* If someone wants to use your code in CLOSED source projects, that is allowed.
* If someone wants to distribute your code in their project with out noticing you, that is allowed.

By default, PyPro uses MIT license, and it put the appropriate file in your code. You could modify if you want,
but in many cases, I think that will not be necessary.

## 3. Packing applications

PyPro distributes installer scripts for py2exe and PyInstaller.
I decided to use both, because some troubles of PyInstaller with PySide.
Then, temporally I prefer to use py2exe in Windows environments and PyInstaller
in linux. Also, because Windows users commonly want to see a single executable
with a few .dll's, over a huge quantity of files with a little .exe, I do not
what they think there, but that is the current situation.


# Additional notes

## And... Why does PyPro need to be an independent project?

Well, good question.
And the answer is not short. I used PyPro from a year ago embedded as a distribution method with my projects - 
If someone thinks Python cannot be used for commercial projects, he/she is wrong.
But, I think now is an appropiate moment to release my code, separating from my projects and publishing as open source.
I want to increase their functionality, and this implies to do more work over.
 
 
Also, if at least another developer thinks it is useful in their work, I will be happy.

## System requirements
 
You do not need to download the whole project, specially if you are using Windows.
You could download only the binary executable.  

PyPro is cross-platform. But, to save disk space, it uses symbolic links in the target operating system.
Then, PyPro currently does not work in Windows XP and previous.


