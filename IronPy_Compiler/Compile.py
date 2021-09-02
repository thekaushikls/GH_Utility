#!/usr/binenv python2.7
# -*- coding: utf-8 -*-

# - - - - - - - - IN-BUILT IMPORTS

import clr
import os
import shutil

# - - - - - - - - METHODS

class IronPyCompiler:

    @staticmethod
    def CollectFiles(Folderpath):

        FileCollection = []
        IgnoreList = [__file__, '__init__.py']

        if os.path.isdir(Folderpath):
            for file in os.listdir(Folderpath):
                absPath = os.path.join(Folderpath, file)
                # Ignore currentfile / compiler file and non .py files
                if absPath not in IgnoreList and file.endswith('.py') and not file.startswith('_'):
                    FileCollection.append(absPath)
                # Recursive if subfolder is detected
                elif os.path.isdir(absPath):
                    FileCollection += IronPyCompiler.CollectFiles(absPath)

        return FileCollection

    @staticmethod
    def Build(FileName, CopyTarget = '', Type = 'Build'):

        FolderName = os.path.dirname(__file__)
        ExportLocation = os.path.join(FolderName, Type)
        if not os.path.exists(ExportLocation): os.makedirs(ExportLocation)
        BuildTarget = os.path.join(ExportLocation, FileName)

        # Get list of all .py files
        ProgramFiles = IronPyCompiler.CollectFiles(FolderName)

        # CLR Compile
        clr.CompileModules(BuildTarget, *ProgramFiles)

        # Copy compiled file to Target
        if CopyTarget:
            shutil.copy2(BuildTarget, CopyTarget)

# - - - - - - - - RUNSCRIPT
    
if __name__ == '__main__':
    IronPyCompiler.Build(r"MyAwesomeLibrary.dll")
