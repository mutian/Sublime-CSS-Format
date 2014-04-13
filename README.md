CSS Format for Sublime Text
===========================


Description
-----------

CSS Format is a CSS formatting plugin for Sublime Text, you can convert CSS/SASS/SCSS/LESS code to Expanded, Compact or Compressed format. CSS Format is just only a formatter, do not supports grammar check and auto correct feature.

**Example:**

* Expanded:

        body {
            background: #fff;
            font: 12px/2em Arial, Helvetica, sans-serif;
        }
        a {
            color: rgba(65, 131, 196, 0.8);
        }
        ol, ul, li {
            margin: 0;
            padding: 0;
        }

* Expanded (Break Selectors):

        body {
            background: #fff;
            font: 12px/2em Arial, Helvetica, sans-serif;
        }
        a {
            color: rgba(65, 131, 196, 0.8);
        }
        ol,
        ul,
        li {
            margin: 0;
            padding: 0;
        }

* Compact:

        body { background: #fff; font: 12px/2em Arial, Helvetica, sans-serif; }
        a { color: rgba(65, 131, 196, 0.8); }
        ol, ul, li { margin: 0; padding: 0; }

* Compact (No Spaces):

        body{background:#fff;font:12px/2em Arial,Helvetica,sans-serif;}
        a{color:rgba(65,131,196,0.8);}
        ol,ul,li{margin:0;padding:0;}

* Compact (Break Selectors):

        body { background: #fff; font: 12px/2em Arial, Helvetica, sans-serif; }
        a { color: rgba(65, 131, 196, 0.8); }
        ol,
        ul,
        li { margin: 0; padding: 0; }

* Compact (Break Selectors, No Spaces):

        body{background:#fff;font:12px/2em Arial,Helvetica,sans-serif;}
        a{color:rgba(65,131,196,0.8);}
        ol,
        ul,
        li{margin:0;padding:0;}

* Compressed:

        body{background:#fff;font:12px/2em Arial,Helvetica,sans-serif}a{color:rgba(65,131,196,0.8)}ol,ul,li{margin:0;padding:0}


Installation
------------

**OPTION 1 - with Package Control (recommended)**

The easiest way to install this package is through Package Control.

1. Install [Package Control](https://sublime.wbond.net/installation), follow instructions on the website.

2. Open command panel: `Ctrl+Shift+P` (Linux/Windows) or `Cmd+Shift+P` (OS X) and select **Package Control: Install Package**.

3. When packages list appears, type `CSS Format` and select it.


**OPTION 2 - with Git**

Clone the repository in your Sublime Text "Packages" directory:

    git clone git://github.com/mutian/CSS-Format.git "CSS Format"

You can find your "Packages" inside the following directories:

* OS X:
    `~/Library/Application Support/Sublime Text 2/Packages/`

* Windows:
    `%APPDATA%/Sublime Text 2/Packages/`

* Linux:
    `~/.Sublime Text 2/Packages/`


**OPTION 3 - without Git**

Download the latest source zip from [Github](https://github.com/mutian/CSS-Format) and extract it into a new folder named `CSS Format` in your Sublime Text "Packages" folder.


Usage
-----

Select the code, or place cursor in the document, and execute commands in one of the following ways:

* Context Menu: **CSS Format**.

* Edit Menu: **Edit &gt; CSS Format**.

* Command Panel: Open command panel: `Ctrl+Shift+P` (Linux/Windows) or `Cmd+Shift+P` (OS X) and select **Format CSS: XXX**.


Shortcuts
---------

By default CSS Format provides no keyboard shortcuts to avoid conflicts, but you can view the included `Example.sublime-keymaps` file to get an idea how to set up your own.


Author
------

Created by **Mutian** ([http://mutian.info](http://mutian.info/)).

For more info, you can send email to me: mutian(a)me.com!


Acknowledgements
----------------

Thanks to the **RIA Team** of [Weibo.com](http://weibo.com/) .
