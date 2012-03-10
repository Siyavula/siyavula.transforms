pstricksTex = r'''
\documentclass[10pt]{report}
\renewcommand{\familydefault}{\sfdefault}
\usepackage{float} % for figures to appear where you want them
\usepackage{setspace}
\usepackage{graphicx}
\usepackage{changebar}
\usepackage{pst-all}
\usepackage{pst-eucl}        %Jo
\usepackage{pst-poly}        %Jo
\usepackage{xcolor}
\usepackage{multicol}
\usepackage{pst-3dplot}        %Jo
\usepackage{pst-solides3d}
%\usepackage{pst-diffraction}
\usepackage{pst-spectra}
\usepackage{pst-slpe}
\usepackage{pst-math}

%% ************* NB ************
%% The order in which pstricks packages are loaded
%% matters - so I copied the order from pst-all.sty
%% and then added the two additional packages at the end.
%% ************* End NB ************

%% ************* Packages ************
\usepackage{pst-circ}
\usepackage{pst-lens}
\usepackage{pst-optic}         %Jo
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
\def\deg{$^\circ$}
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

def pspicture2png(iPspictureElement, iReturnEps=False, iPageWidthPx=None, iDpi=150):
    """
    Inputs:

      iPspictureElement - etree.Element
      iReturnEps - whether to also return the intermediate EPS file
      iPageWidthPx - 
      iDpi - 

    Outputs:

    One or two paths, the first to the PNG, the second to the EPS.
    """
    global pstricksTex
    
    import os, tempfile
    tempDir = tempfile.mkdtemp()
    latexPath = os.path.join(tempDir, 'figure.tex')
    dviPath = os.path.join(tempDir, 'figure.dvi')
    psPath = os.path.join(tempDir, 'figure.ps')
    epsPath = os.path.join(tempDir, 'figure.epsi')
    pngPath = os.path.join(tempDir, 'figure.png')

    namespaces = {
        'style': 'http://siyavula.com/cnxml/style/0.1',
    }
    pspictureDom = etree.fromstring('<xml xmlns:style="' + namespaces['style'] + '">' + request.POST['code'] + '</xml>')[0]
    relativeWidth = pspictureDom.attrib.get('{'+namespaces['style']+'}width')
    code = pspictureDom.find('code').text
    if code is None:
        raise ValueError, "Code cannot be empty."
    with open(latexPath, 'wt') as fp:
        fp.write(pstricksTex.replace('__CODE__', code.strip()))
    os.system("latex -output-directory " + tempDir + " " + latexPath)
    try:
        open(dviPath,"rb")
    except IOError:
        raise IOError, "LaTeX failed to compile the image."
    os.system("dvips " + dviPath + " -o " + psPath)
    os.system("ps2epsi " + psPath + " " + epsPath)

    if (relativeWidth is not None) and (iPageWidthPx is not None):
        size = int(round(float(relativeWidth)*iPageWidthPx))
        os.system('convert -geometry %ix -density %i %s %s'%(size, 2*size, epsPath, pngPath))
    else:
        os.system('convert -density %i %s %s'%(iDpi, epsPath, pngPath))

    if iReturnEps:
        return pngPath, epsPath
    else:
        return pngPath
