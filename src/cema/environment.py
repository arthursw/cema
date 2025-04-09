import subprocess
import sys
from pathlib import Path
from importlib import import_module
from abc import abstractmethod
from typing import Any, TYPE_CHECKING
from types import ModuleType
import inspect

from cema._internal.command_generator import Commands
from cema._internal.dependency_manager import Dependencies

if TYPE_CHECKING:
    from cema.environment_manager import EnvironmentManager


class Environment:
    modules: dict[str, ModuleType] = {}

    def __init__(self, name: str | None, environmentManager: "EnvironmentManager") -> None:
        self.name = name
        self.environmentManager = environmentManager

    def _isModFunction(self, mod, func):
        """Checks that func is a function defined in module mod"""
        return inspect.isfunction(func) and inspect.getmodule(func) == mod

    def _listFunctions(self, mod):
        """Returns the list of functions defined in module mod"""
        return [func.__name__ for func in mod.__dict__.values() if self._isModFunction(mod, func)]

    def _importModule(self, modulePath: Path | str):
        """Imports the given module (if necessary) and adds it to the module map."""
        modulePath = Path(modulePath)
        module = modulePath.stem
        if module not in self.modules:
            sys.path.append(str(modulePath.parent))
            self.modules[module] = import_module(module)
        return self.modules[module]

    def importModule(self, modulePath: Path | str) -> Any:
        """Imports the given module (if necessary) and returns a fake module object
        that contains the same methods of the module which will be executed within the environment."""
        module = self._importModule(modulePath)

        class FakeModule:
            pass

        for f in self._listFunctions(module):

            def fakeFunction(*args, _cema_imported_function=f, **kwargs):
                return self.execute(modulePath, _cema_imported_function, args, kwargs)

            setattr(FakeModule, f, fakeFunction)
        return FakeModule

    def install(self, dependencies: Dependencies, additionalInstallCommands: Commands = {}) -> list[str]:
        """Installs dependencies.
        See :meth:`EnvironmentManager.create` for more details on the ``dependencies`` and ``additionalInstallCommands`` parameters.

        Args:
                dependencies: Dependencies to install.
                additionalInstallCommands: Platform-specific commands during installation.
        Returns:
                Output lines of the installation commands.
        """
        return self.environmentManager.install(self.name, dependencies, additionalInstallCommands)

    @abstractmethod
    def launch(self, additionalActivateCommands: Commands = {}, logOutputInThread: bool = True) -> None:
        """See :meth:`InternalEnvironment.launch` and :meth:`ExternalEnvironment.launch`"""
        pass

    def executeCommands(
        self, commands: Commands, additionalActivateCommands: Commands = {}, popenKwargs: dict[str, Any] = {}
    ) -> subprocess.Popen:
        """Executes the given commands in this environment.

        Args:
                commands: The commands to execute in the environment.
                additionalActivateCommands: Platform-specific activation commands.
                popenKwargs: Keyword arguments for subprocess.Popen(). See :meth:`CommandExecutor.executeCommands`.

        Returns:
                The launched process.
        """
        return self.environmentManager.executeCommands(self.name, commands, additionalActivateCommands, popenKwargs)

    @abstractmethod
    def execute(self, modulePath: str | Path, function: str, args: tuple = (), kwargs: dict[str, Any] = {}) -> Any:
        """Execute the given function in the given module. See :meth:`ExternalEnvironment.execute` and :meth:`InternalEnvironment.execute`"""
        pass

    def _exit(self) -> None:
        """Exit the environment, important in ExternalEnvironment"""
        pass

    def launched(self) -> bool:
        """Check if the environment is launched, important in ExternalEnvironment"""
        return True

    def exit(self) -> None:
        """Exit the environment"""
        self._exit()
        self.environmentManager._removeEnvironment(self)
