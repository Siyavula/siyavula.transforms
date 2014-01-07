from base import *

def latex2pdf(iLatex, iIncludedFiles={}, iPasses=1, iLatexPath='', iLatexBinary='pdflatex', iLatexCommand=None):
    """
    Inputs:

      iLatex - The LaTeX code to compile.

      iIncludedFiles - Dictionary mapping paths to binary data or
        streams. These files may be linked to from the LaTeX
        source. Paths may contain sub-directories. Each key is of type
        string and each value is either of type string or a class that
        supports a read() method.

      iPasses - The number of times to run pdflatex.

      iLatexPath - The directory containing LaTeX executables. This should
        contain pdflatex (or iLatexBinary, if specified).

      iLatexBinary - The name of the binary to call for running LaTeX.
        Note that this is not a full path, but only the name of the binary.

      iLatexCommand - The full path to the binary to use for compiling
        the LaTeX code. If specified, this overrides both iLatexPath
        and iLatexBinary.

    Outputs:

    Path to the PDF.
    """
    import os, tempfile
    tempDir = tempfile.mkdtemp()
    latexFilename = 'document.tex'
    pdfFilename = 'document.pdf'
    latexPath = os.path.join(tempDir, latexFilename)
    pdfPath = os.path.join(tempDir, pdfFilename)
    with open(latexPath, 'wt') as fp:
        fp.write(iLatex.encode('utf-8'))
    for path, pathFile in iIncludedFiles.iteritems():
        try:
            os.makedirs(os.path.join(tempDir, os.path.dirname(path)))
        except OSError:
            # Catch exception if path already exists
            pass
        contents = pathFile if isinstance(pathFile, basestring) else pathFile.read()
        with open(os.path.join(tempDir, path), 'wb') as fp:
            fp.write(contents)
    if iLatexCommand is not None:
        latexCommand = iLatexCommand
    else:
        latexCommand = os.path.join(iLatexPath, iLatexBinary)
    for i in range(iPasses):
        errorLog, temp = execute([latexCommand, "-halt-on-error", latexFilename], cwd=tempDir)
        try:
            open(pdfPath, "rb").close()
        except IOError:
            raise LatexPictureError("LaTeX failed to compile on pass %i."%i, errorLog)
    return pdfPath
