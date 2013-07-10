class LatexPictureError(Exception):
    def __init__(self, message, errorLog):
        Exception.__init__(self, message)
        self.errorLog = errorLog

def execute(args):
    import subprocess
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    return stdout, stderr
