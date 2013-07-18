from base import *

def latex2pdf(iLatex, iIncludedFiles={}, iPasses=1, iLatexPath=''):
    """
    Inputs:

      iLatex - The LaTeX code to compile.

      iIncludedFiles - Dictionary mapping paths to binary data. These
        files may be linked to from the LaTeX source. Paths may
        contain sub-directories.

      iPasses - The number of times to run pdflatex.

      iLatexPath - Path to location of LaTeX executables. This should
        contain pdflatex.

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
        with open(os.path.join(tempDir, path), 'wb') as fp:
            fp.write(pathFile.read())
    for i in range(iPasses):
        errorLog, temp = execute([os.path.join(iLatexPath, 'pdflatex'), "-halt-on-error", latexFilename], cwd=tempDir)
        try:
            open(pdfPath, "rb").close()
        except IOError:
            raise LatexPictureError("LaTeX failed to compile on pass %i."%i, errorLog)
    return pdfPath
