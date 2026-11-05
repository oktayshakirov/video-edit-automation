"""Let the suite run on a machine that is not the build Mac.

The engine names macOS system fonts by absolute path. On Linux they are
absent and every drawn frame raises before the check it belongs to can run. `core.fontshim` answers *missing* paths with
free stand-ins and passes existing ones through, so on the Mac nothing
changes. No test here asserts a typeface; see the shim's docstring for why a
render must never be shipped with it installed.
"""

from video_automation.core import fontshim

fontshim.install()
