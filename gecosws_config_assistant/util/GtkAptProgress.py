import apt
import apt_pkg
import time
import os
import gi
gi.require_version("Gtk", "3.0")
try:
    old_version=True
    gi.require_version("Vte", "2.90")
except:
    old_version=False
    gi.require_version("Vte", "2.91")
from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import GLib
from gi.repository import Gdk
from gi.repository import Pango
from gi.repository import Vte

from apt.progress.base import InstallProgress, OpProgress, AcquireProgress
from gettext import gettext as _


__all__ = ['GAcquireProgress', 'GInstallProgress', 'GOpProgress',
           'GtkAptProgress']

def mksig(params=(), run=GObject.SIGNAL_RUN_FIRST, rettype=GObject.TYPE_NONE):
    """Simplified Create a GObject signal.

    This allows us to write signals easier, because we just need to define the
    type of the parameters (in most cases).

    ``params`` is a tuple which defines the types of the arguments.
    """
    return (run, rettype, params)


class GOpProgress(GObject.GObject, OpProgress):
    """Operation progress with GObject signals.

    Signals:

        * status-changed(str: operation, int: percent)
        * status-started()  - Not Implemented yet
        * status-finished()

    """

    __gsignals__ = {"status-changed": mksig((str, int)),
                    "status-started": mksig(),
                    "status-finished": mksig()}

    def __init__(self):
        self._context = GLib.main_context_default()
        super(GOpProgress, self).__init__()

    def update(self, percent=None):
        """Called to update the percentage done"""
        OpProgress.update(self, percent)
        self.emit("status-changed", self.op, self.percent)
        while self._context.pending():
            self._context.iteration()

    def done(self):
        """Called when all operation have finished."""
        OpProgress.done(self)
        self.emit("status-finished")


class GInstallProgress(GObject.GObject, InstallProgress):
    """Installation progress with GObject signals.

    Signals:

        * status-changed(str: status, int: percent)
        * status-started()
        * status-finished()
        * status-timeout()
        * status-error()
        * status-conffile()

    """
    # Seconds until a maintainer script will be regarded as hanging
    INSTALL_TIMEOUT = 5 * 60

    __gsignals__ = {"status-changed": mksig((str, int)),
                    "status-started": mksig(),
                    "status-timeout": mksig(),
                    "status-error": mksig(),
                    "status-conffile": mksig(),
                    "status-finished": mksig()}

    def __init__(self, term):
        InstallProgress.__init__(self)
        self.finished = False
        self.apt_status = -1
        self.time_last_update = time.time()
        self.term = term
        if old_version:
            self.term.connect("child-exited", self.child_exited)
        else:
            self.term.connect("child-exited", self.child_exited_2)
        self.env = ["VTE_PTY_KEEP_FD=%s" % self.writefd,
                    "DEBIAN_FRONTEND=gnome",
                    "APT_LISTCHANGES_FRONTEND=Gtk"]
        self._context = GLib.main_context_default()
        super(GInstallProgress, self).__init__()

    def child_exited(self, term):
        """Called when a child process exits"""
        self.apt_status = term.get_child_exit_status()
        self.finished = True

    def child_exited_2(self, term, status):
        self.apt_status = status
        self.finished = True

    def error(self, pkg, errormsg):
        """Called when an error happens.

        Emits: status-error()
        """
        self.emit("status-error")

    def conffile(self, current, new):
        """Called during conffile.

        Emits: status-conffile()
        """
        self.emit("status-conffile")

    def start_update(self):
        """Called when the update starts.

        Emits: status-started()
        """
        self.emit("status-started")

    def run(self, obj):
        """Run."""
        self.finished = False
        return InstallProgress.run(self, obj)

    def finish_update(self):
        """Called when the update finished.

        Emits: status-finished()
        """
        self.emit("status-finished")

    def processing(self, pkg, stage):
        """Called when entering a new stage in dpkg."""
        # We have no percentage or alike, send -1 to let the bar pulse.
        self.emit("status-changed", ("Installing %s...") % pkg, -1)

    def status_change(self, pkg, percent, status):
        """Called when the status changed.

        Emits: status-changed(status, percent)
        """
        self.time_last_update = time.time()
        self.emit("status-changed", status, percent)

    def update_interface(self):
        """Called periodically to update the interface.

        Emits: status-timeout() [When a timeout happens]
        """
        InstallProgress.update_interface(self)
        while self._context.pending():
            self._context.iteration()
        if self.time_last_update + self.INSTALL_TIMEOUT < time.time():
            self.emit("status-timeout")

    def fork(self):
        """Fork the process."""
        #return self.term.forkpty(envv=self.env)

        if old_version:
            pty = Vte.Pty.new(Vte.PtyFlags.DEFAULT)
            self.term.set_pty_object(pty)
        else:
            pty = Vte.Pty.new_sync(Vte.PtyFlags.DEFAULT)
            self.term.set_pty(pty)
        pid = os.fork()
        if pid == 0:
            # *grumpf* workaround bug in vte here (gnome bug #588871)
            for env in self.env:
                (key, value) = env.split("=")
                os.environ[key] = value
            # MUST be called
            pty.child_setup()
            # FIXME: close all fds expect for self.writefd
        else:
            if old_version:
                self.term.set_pty_object(pty)
            else:
                self.term.set_pty(pty)
            self.term.watch_child(pid)

        return pid

    def wait_child(self):
        """Wait for the child process to exit."""
        while not self.finished:
            self.update_interface()
            time.sleep(0.02)
        return self.apt_status

GDpkgInstallProgress = GInstallProgress


class GAcquireProgress(GObject.GObject, AcquireProgress):
    """A Fetch Progress with GObject signals.

    Signals:

        * status-changed(str: description, int: percent)
        * status-started()
        * status-finished()

    DEPRECATED.
    """

    __gsignals__ = {"status-changed": mksig((str, int)),
                    "status-started": mksig(),
                    "status-finished": mksig()}

    def __init__(self):
        AcquireProgress.__init__(self)
        self._continue = True
        self._context = GLib.main_context_default()
        super(GAcquireProgress, self).__init__()

    def start(self):
        AcquireProgress.start(self)
        self.emit("status-started")

    def stop(self):
        AcquireProgress.stop(self)
        self.emit("status-finished")

    def cancel(self):
        self._continue = False

    def pulse(self, owner):
        AcquireProgress.pulse(self, owner)
        current_item = self.current_items + 1
        if current_item > self.total_items:
            current_item = self.total_items
        if self.current_cps > 0:
            text = (_("Downloading file %(current)li of %(total)li with "
                      "%(speed)s/s") %
                      {"current": current_item,
                       "total": self.total_items,
                       "speed": apt_pkg.size_to_str(self.current_cps)})
        else:
            text = (_("Downloading file %(current)li of %(total)li") %
                      {"current": current_item,
                       "total": self.total_items})

        percent = (((self.current_bytes + self.current_items) * 100.0) /
                        float(self.total_bytes + self.total_items))
        self.emit("status-changed", text, percent)
        while self._context.pending():
            self._context.iteration()
        return self._continue


class GtkAptProgress(Gtk.VBox):
    """Graphical progress for installation/fetch/operations.

    This widget provides a progress bar, a terminal and a status bar for
    showing the progress of package manipulation tasks.
    """

    def __init__(self):
        Gtk.VBox.__init__(self)
        self.set_spacing(6)
        # Setup some child widgets
        self._expander = Gtk.Expander.new(_("Details"))
        self._terminal = Vte.Terminal()
        if old_version:
            self._terminal.set_font_from_string("monospace 10")
        self._expander.add(self._terminal)
        self._progressbar = Gtk.ProgressBar()
        # Setup the always italic status label
        self._label = Gtk.Label()
        #attr_list = pango.AttrList()
        #attr_list.insert(pango.AttrStyle(pango.STYLE_ITALIC, 0, -1))
        #self._label.set_attributes(attr_list)
        self._label.set_ellipsize(Pango.EllipsizeMode.END)
        self._label.set_alignment(0, 0)
        # add child widgets
        self.pack_start(self._progressbar, False, False, 0)
        self.pack_start(self._label, False, False, 0)
        self.pack_start(self._expander, False, False, 0)
        # Setup the internal progress handlers
        self._progress_open = GOpProgress()
        self._progress_open.connect("status-changed", self._on_status_changed)
        self._progress_open.connect("status-started", self._on_status_started)
        self._progress_open.connect("status-finished",
                                    self._on_status_finished)
        self._progress_acquire = GAcquireProgress()
        self._progress_acquire.connect("status-changed",
                                       self._on_status_changed)
        self._progress_acquire.connect("status-started",
                                       self._on_status_started)
        self._progress_acquire.connect("status-finished",
                                     self._on_status_finished)

        self._progress_fetch = None
        self._progress_install = GInstallProgress(self._terminal)
        self._progress_install.connect("status-changed",
                                       self._on_status_changed)
        self._progress_install.connect("status-started",
                                       self._on_status_started)
        self._progress_install.connect("status-finished",
                                     self._on_status_finished)
        self._progress_install.connect("status-timeout",
                                     self._on_status_timeout)
        self._progress_install.connect("status-error",
                                     self._on_status_timeout)
        self._progress_install.connect("status-conffile",
                                     self._on_status_timeout)

    def clear(self):
        """Reset all status information."""
        self._label.set_label("")
        self._progressbar.set_fraction(0)
        self._expander.set_expanded(False)

    @property
    def open(self):
        """Return the cache opening progress handler."""
        return self._progress_open

    @property
    def install(self):
        """Return the install progress handler."""
        return self._progress_install

    @property
    def dpkg_install(self):
        """Return the install progress handler for dpkg."""
        return self._progress_install

    @property
    def acquire(self):
        """Return the acquire progress handler."""
        return self._progress_acquire

    def _on_status_started(self, progress):
        """Called when something starts."""
        self._on_status_changed(progress, _("Starting..."), 0)
        while Gtk.events_pending():
            Gtk.main_iteration()

    def _on_status_finished(self, progress):
        """Called when something finished."""
        self._on_status_changed(progress, _("Complete"), 100)
        while Gtk.events_pending():
            Gtk.main_iteration()

    def _on_status_changed(self, progress, status, percent):
        """Called when the status changed."""
        self._label.set_text(status)
        if percent is None or percent == -1:
            self._progressbar.pulse()
        else:
            self._progressbar.set_fraction(percent / 100.0)
        while Gtk.events_pending():
            Gtk.main_iteration()

    def _on_status_timeout(self, progress):
        """Called when timeout happens."""
        self._expander.set_expanded(True)
        while Gtk.events_pending():
            Gtk.main_iteration()

    def cancel_download(self):
        """Cancel a currently running download."""
        self._progress_fetch.cancel()

    def show_terminal(self, expanded=False):
        """Show the expander for the terminal.

        Show an expander with a terminal widget which provides a way
        to interact with dpkg
        """
        self._expander.show()
        self._terminal.show()
        self._expander.set_expanded(expanded)
        while Gtk.events_pending():
            Gtk.main_iteration()

    def hide_terminal(self):
        """Hide the expander with the terminal widget."""
        self._expander.hide()
        while Gtk.events_pending():
            Gtk.main_iteration()

    def show(self):
        """Show the Box"""
        Gtk.HBox.show(self)
        self._label.show()
        self._progressbar.show()
        while Gtk.events_pending():
            Gtk.main_iteration()


