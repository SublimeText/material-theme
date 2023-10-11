"""Support command."""
import sublime
import sublime_plugin
import textwrap

__version__ = '4.1.5'
__pc_name__ = 'Material Theme'


def list2string(obj):
    """Convert list to string."""

    return '.'.join([str(x) for x in obj])


def format_version(module, attr, call=False):
    """Format the version."""

    try:
        if call:
            version = getattr(module, attr)()
        else:
            version = getattr(module, attr)
    except Exception as e:
        print(e)
        version = 'Version could not be acquired!'

    if not isinstance(version, str):
        version = list2string(version)
    return version


def is_installed_by_package_control():
    """Check if installed by package control."""

    settings = sublime.load_settings('Package Control.sublime-settings')
    return str(__pc_name__ in set(settings.get('installed_packages', [])))


class MtInfoCommand(sublime_plugin.ApplicationCommand):
    """Support info."""

    def run(self):
        """Run command."""

        info = {}

        info["platform"] = sublime.platform()
        info["version"] = sublime.version()
        info["arch"] = sublime.arch()
        info["bh_version"] = __version__
        info["pc_install"] = is_installed_by_package_control()
        try:
            import mdpopups
            info["mdpopups_version"] = format_version(mdpopups, 'version', call=True)
        except Exception:
            info["mdpopups_version"] = 'Version could not be acquired!'

        msg = textwrap.dedent(
            """\
            - Sublime Text:   %(version)s
            - Platform:   %(platform)s
            - Arch:   %(arch)s
            - Theme:   %(bh_version)s
            - Install via PC:   %(pc_install)s
            - Dependencies:
                * mdpopups:   %(mdpopups_version)s
            """ % info
        )

        view = sublime.active_window().active_view()

        def copy_and_hide(msg):
            sublime.set_clipboard(msg)
            view.hide_popup()

        view.show_popup(msg.replace('\n', '<br>') + '<br><a href="' + msg + '">Copy</a>', on_navigate = copy_and_hide, max_height = 340)
