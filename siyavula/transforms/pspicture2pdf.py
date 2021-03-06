pstricksTex = r'''
\documentclass[10pt]{report}
\renewcommand{\familydefault}{\sfdefault}
\usepackage{float} % for figures to appear where you want them
\usepackage{setspace}
\usepackage{xcolor}
\usepackage{graphicx}
\usepackage{changebar}

\usepackage{pst-all}
\usepackage{pst-eucl}
\usepackage{pst-poly}
\usepackage{pst-math}
\usepackage{pstricks-add}

%\usepackage{pst-spectra}
%\usepackage{pst-slpe}
%\usepackage{pst-3dplot}
%\usepackage{pst-diffraction}
%\usepackage{pst-lens}
%\usepackage{pst-optic}
%\usepackage{pst-solides3d}
%\usepackage{pst-node}
%\usepackage{pst-labo}

__PACKAGES__

%% ************* NB ************
%% The order in which pstricks packages are loaded
%% matters - so I copied the order from pst-all.sty
%% and then added the two additional packages at the end.
%% ************* End NB ************

%% ************* Packages ************
\usepackage{pst-circ}
\usepackage{pstricks-add}         %Jo
\usepackage{pst-labo}         %Jo
\usepackage{subfigure}
\usepackage{multirow}
\usepackage{amsmath}
\usepackage{tabularx}
\usepackage{lscape}
\usepackage{fancyhdr}
\usepackage{wasysym}
\usepackage{url}
\usepackage{amsmath, amsthm, amsfonts, amssymb}
\usepackage{eurosym}
\usepackage{array}
\usepackage{enumitem}
\sffamily

%\usepackage{mdframed}

\newcommand{\ohm}{\ensuremath{\Omega}}
\newcommand{\eohm}{\,\Omega}
\newcommand{\eN}{\,\rm{N}}                %m in text
\newcommand{\emm}{\,\rm{m}}                %m in text
\newcommand{\ep}{\,\ekg \cdot \mbox{\ms}}                %m/s in text
\newcommand{\es}{\,\text{s}}                %s in equation
\newcommand{\ekg}{\,\text{kg}}                %kg in equation
\newcommand{\eJ}{\,\text{J}}                %J in equation
\newcommand{\eA}{\,\text{A}}                %A in equation
\newcommand{\eV}{\,\text{V}}                %J in equation
\newcommand{\eW}{\,\text{W}}                %W in equation
\newcommand{\ms}{$\text{m}\cdot\text{s}^{-1}$}                %m/s in text
\newcommand{\mss}{$\text{m}\cdot\text{s}^{-2}$}                %m/s in text
\newcommand{\ems}{\,\text{m} \cdot \text{s}^{-1}}            %m/s in equation
\newcommand{\emss}{\,\text{m} \cdot \text{s}^{-2}}            %m/s in equation
\newcommand{\px}{$x$}                % position x, in text
\newcommand{\py}{$y$}                % position y, in text
\newcommand{\edx}{\Delta x}        % displacement dx, in text
\newcommand{\dx}{$\edx$}            % displacement dx, in text
\newcommand{\edy}{\Delta y}            % displacement dy, in text
\newcommand{\dy}{$\edy$}            % displacement dy, in text
\newcommand{\edt}{\Delta t}            % delta time dt, in text
\newcommand{\dt}{$\edt$}            % delta time dt, in text
\newcommand{\vel}{$v$}                % velocity
\newcommand{\kph}{km$\cdot$hr$^{-1}$}    %km/h in text
\newcommand{\momen}{\vec{p}}            %momentum
\newcommand{\kener}{KE}                            %kinetic energy
\newcommand{\poten}{PE}                            %kinetic energy
\newcommand{\degree}{^{\circ}}
\newcommand{\ie}{{\em i.e.~}}
\newcommand{\eg}{{\em e.g.~}}
\newcommand{\cf}{{\em c.f.~}}
\newcommand{\resp}{{\em resp.~}}
\newcommand{\etc}{{\em etc.~}}
\newcommand{\nb}{{\em n.b.~}}
\newcommand{\eJSI}{{\,\text{kg} \cdot \text{m}^{2} \cdot \text{s}^{-2}}}
\def\deg{$^{\circ}$}
\newcommand{\ud}{\mathrm{d}}

% Arrow for objects and images
%\newpsobject{oi}{psline}{arrowsize=6pt, arrowlength=1.5, arrowinset=0, linewidth=2pt}
%\psset{lensHeight=3,lensColor=lightgray}
%\newpsobject{PrincipalAxis}{psline}{linewidth=0.5pt,linecolor=gray}

%\include{DefinitionsV0-5}
\pagestyle{empty}
\begin{document}
\begin{pspicture}__CODE__
\end{pspicture}
\end{document}
'''

tikzTex = r'''
\documentclass[10pt]{report}
\renewcommand{\familydefault}{\sfdefault}

\usepackage{tikz, ifthen}
\usetikzlibrary{arrows,shapes,backgrounds,patterns,decorations.pathreplacing,decorations.pathmorphing,decorations.markings,shadows,shapes.misc,calc,positioning,intersections}
__PACKAGES__

\usepackage{setspace}
\usepackage{graphicx}
\usepackage{changebar}
\usepackage{xcolor}

%% ************* Packages ************
\usepackage{amsmath}
\usepackage{wasysym}
\usepackage{amsmath, amsthm, amsfonts, amssymb}
\usepackage{eurosym}
\sffamily

\pagestyle{empty}
\begin{document}
\begin{tikzpicture}__CODE__
\end{tikzpicture}
\end{document}
'''

def execute(args):
    import subprocess
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    return stdout, stderr

class LatexPictureError(Exception):
    pass

def pstikz2pdf(iPictureElement, iLatex, iReturnEps=False, iPageWidthPx=None, iDpi=150, iIncludedFiles={}):
    """
    Inputs:

      iPspictureElement - etree.Element

      iReturnEps - whether to also return the intermediate EPS file

      iPageWidthPx - page width in pixels, used to scale the
        style:width attribute in the element.

      iDpi - Will be used only if the width of the figure relative to
        the page width was not set (or the page width in pixels was not
        passed as an argument).

      iIncludedFiles - Dictionary mapping paths to binary data or
        streams. These files may be linked to from the LaTeX
        source. Paths may contain sub-directories. Each key is of type
        string and each value is either of type string or a class that
        supports a read() method.

    Outputs:

    One or two paths, the first to the PNG, the second to the EPS.
    """
    import os, tempfile
    from lxml import etree

    tempDir = tempfile.mkdtemp()
    latexPath = os.path.join(tempDir, 'figure.tex')
    dviPath = os.path.join(tempDir, 'figure.dvi')
    psPath = os.path.join(tempDir, 'figure.ps')
    epsPath = os.path.join(tempDir, 'figure.epsi')
    pdfPath = os.path.join(tempDir, 'figure.pdf')

    namespaces = {
        'style': 'http://siyavula.com/cnxml/style/0.1',
    }
    relativeWidth = iPictureElement.attrib.get('{'+namespaces['style']+'}width')
    packages = ''
    for packageNode in iPictureElement.xpath('.//usepackage'):
        packages += r'\usepackage{' + packageNode.text.strip() + '}\n'
    code = iPictureElement.find('code').text
    if code is None:
        raise ValueError, "Code cannot be empty."
    with open(latexPath, 'wt') as fp:
        fp.write(iLatex.replace('__PACKAGES__', packages).replace('__CODE__', code.strip()))

    for path, pathFile in iIncludedFiles.iteritems():
        try:
            os.makedirs(os.path.join(tempDir, os.path.dirname(path)))
        except OSError:
            # Catch exception if path already exists
            pass
        contents = pathFile if isinstance(pathFile, basestring) else pathFile.read()
        with open(os.path.join(tempDir, path), 'wb') as fp:
            fp.write(contents)

    errorLog, temp = execute(["latex", "-halt-on-error", "-output-directory", tempDir, latexPath])
    try:
        open(dviPath,"rb")
    except IOError:
        print errorLog
        raise LatexPictureError, "LaTeX failed to compile the image."
    execute(["dvips", dviPath, "-o", psPath])
    execute(["ps2epsi", psPath, epsPath])

    if (relativeWidth is not None) and (iPageWidthPx is not None):
        size = int(round(float(relativeWidth)*iPageWidthPx))
        execute(['convert', '-geometry', '%ix'%size, '-density', '%i'%(2*size), epsPath, pdfPath])
    else:
        execute(['convert', '-density', '%i'%iDpi, epsPath, pdfPath])

    if iReturnEps:
        return pdfPath, epsPath
    else:
        return pdfPath

def tikzpicture2pdf(iTikzpictureElement, *args, **kwargs):
    return pstikz2pdf(iTikzpictureElement, tikzTex, *args, **kwargs)

def pspicture2pdf(iPspictureElement, *args, **kwargs):
    return pstikz2pdf(iPspictureElement, pstricksTex, *args, **kwargs)
