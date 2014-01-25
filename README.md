CSS Formatting for Sublime Text 2
===================


Description
-----------

CSS Format is a CSS formatting plugin for Sublime Text 2, you can convert CSS code to Compact、Expand format, or compress CSS. CSS Format is just only a formatter, do not supports grammar check and auto correct feature.

**Example:**

* Compact format:

        body{background-color:#fff;color:#333;font-size:12px;}
        a{color:#06f;}
        a:hover{color:#09c;}

* Expand format:

        body {
            background-color:#fff;
            color:#333;
            font-size:12px;
        }
        a {
            color:#06f;
        }
        a:hover {
            color:#09c;
        }

* Compress:

        body{background-color:#fff;color:#333;font-size:12px;}a{color:#06f;}a:hover{color:#09c;}


Installation
------------

**OPTION 1 - with Package Control *(recommended)* **

The easiest way to install this package is through Package Control.

1. Install [Package Control](https://sublime.wbond.net/installation), follow instructions on the website.

2. Open command panel: `Ctrl+Shift+P` (Linux/Windows) or `Cmd+Shift+P` (OS X) and select **Package Control: Install Package**.

3. When packages list appears, type `CSS Format` and select it.


**OPTION 2 - with Git**

Clone the repository in your Sublime Text "Packages" directory:

    git clone git://https://github.com/mutian/CSS-Format.git Jade-Build

You can find your "Packages" inside the following directories:

* OS X:
    `~/Library/Application Support/Sublime Text 2/Packages/`

* Windows:
    `%APPDATA%/Sublime Text 2/Packages/`

* Linux:
    `~/.Sublime Text 2/Packages/`


**OPTION 3 - without Git**

Download the latest source zip from [Github](https://github.com/mutian/CSS-Format) and extract it into a new folder named `Jade Build` in your Sublime Text "Packages" folder.


Usage
-----

Keyboard shortcuts:

* Windows & Linux:

    * `Ctrl+Alt+[` : Convert to compact format
    * `Ctrl+Alt+]` : Convert to expand format
    * `Ctrl+Alt+\` : Compress CSS

* Mac:

    * `Ctrl+Cmd+[` : Convert to compact format
    * `Ctrl+Cmd+]` : Convert to expand format
    * `Ctrl+Cmd+\` : Compress CSS


Author
------

Created by **Mutian** ([http://mutian.info](http://mutian.info/)).

For more info, you can send email to me: mutian(a)me.com!


Acknowledgements
----------------

Thanks to the **RIA Team** of [Weibo.com](http://weibo.com/) .
