\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{CST_CryptoIntro}[2026/07/09 Cryptography Introduction Report Template]

\LoadClass[12pt, a4paper]{article}

% ========================================================================
% 核心包加载
% ========================================================================
\RequirePackage{fontspec}
\RequirePackage{xeCJK}
\RequirePackage{amsmath, amsfonts, amssymb}
\RequirePackage{geometry}
\RequirePackage{graphicx}
\RequirePackage{listings}
\RequirePackage{float}
\RequirePackage{url}
\RequirePackage[table]{xcolor}
\RequirePackage{booktabs}
\RequirePackage{fancyhdr}
\RequirePackage[many]{tcolorbox}
\RequirePackage{enumitem}
\RequirePackage{hyperref}
\RequirePackage{tabularx}

% ========================================================================
% 页面设置
% ========================================================================
\geometry{left=2.5cm, right=2.5cm, top=3cm, bottom=3cm, headheight=25pt}

% ========================================================================
% 字体设置
% ========================================================================
\setmainfont{Times New Roman}
\setCJKmainfont[AutoFakeBold=2]{SimSun}
\setCJKmonofont[AutoFakeBold=2]{SimSun}

% ========================================================================
% 颜色定义
% ========================================================================
\definecolor{macblue}{RGB}{0, 122, 255}
\definecolor{bglight}{RGB}{245, 245, 247}
\definecolor{darkgray}{RGB}{51, 51, 51}
\definecolor{warningred}{RGB}{255, 59, 48}

% ========================================================================
% 超链接设置
% ========================================================================
\hypersetup{
    colorlinks=true,
    linkcolor=macblue,
    urlcolor=macblue
}

% ========================================================================
% 页眉页脚设置
% ========================================================================
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\textcolor{macblue}{\textbf{\@headerLeft}}}
\fancyhead[R]{\textbf{\@headerRight}}
\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{0.8pt}
\renewcommand{\headrule}{\hbox to\headwidth{\color{macblue}\leaders\hrule height \headrulewidth\hfill}}

% ========================================================================
% 代码高亮设置 (listings)
% ========================================================================
\lstset{
    language=Python,
    basicstyle=\ttfamily\small,
    keywordstyle=\color{blue!60!black}\bfseries,
    commentstyle=\color{black!40}\itshape,
    stringstyle=\color{red!50!black},
    numbers=left,
    numberstyle=\tiny\color{black!35},
    stepnumber=1,
    numbersep=10pt,
    frame=single,
    framerule=0.4pt,
    rulecolor=\color{black!20},
    backgroundcolor=\color{gray!5},
    breaklines=true,
    breakatwhitespace=false,
    columns=fullflexible,
    keepspaces=true,
    tabsize=4,
    showstringspaces=false,
    extendedchars=true,
    captionpos=b,
    aboveskip=8pt,
    belowskip=6pt,
    xleftmargin=12pt,
    framexleftmargin=10pt,
}

% ========================================================================
% 彩色框环境 (tcolorbox)
% ========================================================================
\newtcolorbox{coreconcept}[1][]{
    colback=bglight,
    colframe=macblue,
    fonttitle=\bfseries\sffamily,
    title=#1,
    arc=3mm,
    boxrule=1.2pt,
    shadow={2mm}{-1.5mm}{0mm}{black!15},
    left=10pt, right=10pt, top=5pt, bottom=5pt,
    fontupper=\small,
    width=\linewidth,
    before skip=10pt,
    after skip=10pt
}

\newtcolorbox{warningbox}[1][]{
    colback=warningred!5,
    colframe=warningred,
    fonttitle=\bfseries\sffamily,
    title=#1,
    arc=3mm,
    boxrule=1.2pt,
    left=10pt, right=10pt, top=5pt, bottom=5pt
}

% ========================================================================
% 封面变量定义
% ========================================================================
\newcommand{\@headerLeft}{密码分析学}
\newcommand{\@headerRight}{实验报告}
\newcommand{\@reportCourse}{密码分析学实验报告}
\newcommand{\@reportLogo}{}
\newcommand{\@reportName}{}
\newcommand{\@reportID}{}
\newcommand{\@reportMajor}{}

% 封面变量设置命令
\newcommand{\headerLeft}[1]{\def\@headerLeft{#1}}
\newcommand{\headerRight}[1]{\def\@headerRight{#1}}
\newcommand{\reportCourse}[1]{\def\@reportCourse{#1}}
\newcommand{\reportLogo}[1]{\def\@reportLogo{#1}}
\newcommand{\reportName}[1]{\def\@reportName{#1}}
\newcommand{\reportID}[1]{\def\@reportID{#1}}
\newcommand{\reportMajor}[1]{\def\@reportMajor{#1}}

% ========================================================================
% 封面生成
% ========================================================================
\renewcommand{\maketitle}{
    \begin{titlepage}
        \thispagestyle{empty}
        \centering
        \vspace*{0cm}
        \ifx\@reportLogo\empty \else \includegraphics[width=0.5\textwidth]{\@reportLogo} \fi
        \par\vspace{1.5cm}
        {\bfseries\sffamily\Large \@reportCourse \par}
        \vspace{3cm}
        \renewcommand{\arraystretch}{2}
        \normalsize
        \begin{tabular}{c}
            姓名：\underline{\makebox[8cm][c]{\@reportName}} \\
            学号：\underline{\makebox[8cm][c]{\@reportID}} \\
            专业：\underline{\makebox[8cm][c]{\@reportMajor}} \\
            日期：\underline{\makebox[8cm][c]{\today}} \\
        \end{tabular}
        \vfill
    \end{titlepage}
}
