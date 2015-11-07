import datetime
import sys
import threading
import traceback
import time


class CurrentStat(object):
    """
    Non-interactively print stack traces of all running threads without
    interrupting current execution.
    """
    def __init__(self, count=3, interval=1, out=sys.stderr):
        self.out = out
        self.count = count
        self.interval = interval

    def _time_stmp(self):
        return datetime.datetime.now().strftime("%d.%b %Y %H:%M:%S:%f")

    def print_stack(self):
        """
        Print a single pass of the stack for each running thread
        """
        for threadId, stack in sys._current_frames().items():
            self.out.write("\n# ThreadID: %s\n" % threadId)
            for filename, lineno, name, line in traceback.extract_stack(stack):
                self.out.write('File: "%s", line %d, in %s\n' % (filename, lineno, name))
                self.out.write("\t%s\n" % line.strip())
        self.out.flush()
        return

    def mprint_stack(self, none=None):
        """
        Print multiple stacks of all running threads at "interval", for number of
        iterations specified by "count"
        """
        for _ in range(self.count):
            self.print_stack()
            time.sleep(self.interval)
        return

    def mtprint_stack(self):
        """
        Same as mprint_stack but run as a seprate thread
        """
        th = threading.Thread(target=self.mprint_stack, args=(self,))
        th.start()
        return

    def print_stat(self):
        threads = threading.enumerate()
        threads_by_ident = dict((t.ident, t) for t in threads)
        for ident, frame in sys._current_frames().items():
            t = threads_by_ident.get(ident)
            self.out.write('%s %s in %s ' % (self._time_stmp(), t.name, frame.f_code.co_name))
            self.out.write('at line %s of %s\n' % (frame.f_lineno, frame.f_code.co_filename))
        self.out.flush()
        return

    def mprint_stat(self):
        for _ in range(self.count):
            self.print_stat()
            time.sleep(self.interval)
        return


if __name__ == "__main__":
    help(__name__)
