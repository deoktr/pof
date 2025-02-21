# POF, a free and open source Python obfuscation framework.
# Copyright (C) 2022 - 2025  POF Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from .argv import ArgvEvasion
from .cpu.cpu_count import CPUCountEvasion
from .fs.directory_exist import DirectoryExistEvasion
from .fs.directory_list_exist import DirectoryListExistEvasion
from .fs.directory_list_missing import DirectoryListMissingEvasion
from .fs.directory_missing import DirectoryMissingEvasion
from .fs.exec_method import ExecMethodEvasion
from .fs.executable_path import ExecPathEvasion
from .fs.file_exist import FileExistEvasion
from .fs.file_list_exist import FileListExistEvasion
from .fs.file_list_missing import FileListMissingEvasion
from .fs.file_missing import FileMissingEvasion
from .fs.tmp import LinuxTmpCountEvasion, TmpCountEvasion, WinTmpCountEvasion
from .hardware.ram_count import LinuxRAMCountEvasion
from .hooks.debugger import DebuggerEvasion
from .hooks.tracemalloc import TracemallocEvasion
from .human.prompt import WinPromptEvasion
from .multi import MultiEvasion
from .os.domain import DomainEvasion
from .os.hostname import HostnameEvasion
from .os.uid import LinuxUIDEvasion
from .os.username import UsernameEvasion
from .processes.proc_count import LinuxProcCountEvasion
from .time.expire import ExpireEvasion
from .time.uptime import LinuxUptimeEvasion
from .time.utc import UTCEvasion

__all__ = [
    "ArgvEvasion",
    "CPUCountEvasion",
    "DebuggerEvasion",
    "DirectoryExistEvasion",
    "DirectoryListExistEvasion",
    "DirectoryListMissingEvasion",
    "DirectoryMissingEvasion",
    "DomainEvasion",
    "ExecMethodEvasion",
    "ExecPathEvasion",
    "ExpireEvasion",
    "FileExistEvasion",
    "FileListExistEvasion",
    "FileListMissingEvasion",
    "FileMissingEvasion",
    "HostnameEvasion",
    "LinuxProcCountEvasion",
    "LinuxRAMCountEvasion",
    "LinuxTmpCountEvasion",
    "LinuxUIDEvasion",
    "LinuxUptimeEvasion",
    "MultiEvasion",
    "TmpCountEvasion",
    "TracemallocEvasion",
    "UTCEvasion",
    "UsernameEvasion",
    "WinPromptEvasion",
    "WinTmpCountEvasion",
]
