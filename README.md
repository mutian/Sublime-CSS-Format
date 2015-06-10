CSS Formatter for Sublime Text
==============================


Description
-----------

CSS Format is a CSS formatting plugin for Sublime Text, you can convert CSS/SASS/SCSS/LESS code to Expanded, Compact or Compressed format. CSS Format is just only a formatter, do not supports grammar check and auto correct feature.

**Example:**

* Expanded:

    ```css
    body {
        background: #fff;
        font: 12px/2em Arial, Helvetica, sans-serif;
    }
    ol, ul, li {
        margin: 0;
        padding: 0;
    }
    a {
        color: rgba(65, 131, 196, 0.8);
    }
    ```

* Expanded (Break Selectors):

    ```css
    body {
        background: #fff;
        font: 12px/2em Arial, Helvetica, sans-serif;
    }

    ol,
    ul,
    li {
        margin: 0;
        padding: 0;
    }
    
    a {
        color: rgba(65, 131, 196, 0.8);
    }
    ```

* Compact:

    ```css
    body { background: #fff; font: 12px/2em Arial, Helvetica, sans-serif; }
    ol, ul, li { margin: 0; padding: 0; }
    a { color: rgba(65, 131, 196, 0.8); }
    ```

* Compact (No Spaces):

    ```css
    body{background:#fff;font:12px/2em Arial,Helvetica,sans-serif;}
    ol,ul,li{margin:0;padding:0;}
    a{color:rgba(65,131,196,0.8);}
    ```

* Compact (Break Selectors):

    ```css
    body { background: #fff; font: 12px/2em Arial, Helvetica, sans-serif; }
    ol,
    ul,
    li { margin: 0; padding: 0; }
    a { color: rgba(65, 131, 196, 0.8); }
    ```

* Compact (Break Selectors, No Spaces):

    ```css
    body{background:#fff;font:12px/2em Arial,Helvetica,sans-serif;}
    ol,
    ul,
    li{margin:0;padding:0;}
    a{color:rgba(65,131,196,0.8);}
    ```

* Compressed:

    ```css
    body{background:#fff;font:12px/2em Arial,Helvetica,sans-serif}ol,ul,li{margin:0;padding:0}a{color:rgba(65,131,196,0.8)}
    ```


Installation
------------

**OPTION 1 - with Package Control (recommended)**

The easiest way to install this package is through Package Control.

1. Install [Package Control](https://sublime.wbond.net/installation), follow instructions on the website.

2. Open command panel: `Ctrl+Shift+P` (Linux/Windows) or `Cmd+Shift+P` (OS X) and select **Package Control: Install Package**.

3. When packages list appears, type `CSS Format` and select it.


**OPTION 2 - with Git**

Clone the repository in your Sublime Text "Packages" directory:

    git clone git://github.com/mutian/Sublime-CSS-Format.git "CSS Format"

You can find your "Packages" inside the following directories:

* OS X:
    `~/Library/Application Support/Sublime Text 2/Packages/`

* Windows:
    `%APPDATA%/Sublime Text 2/Packages/`

* Linux:
    `~/.Sublime Text 2/Packages/`


**OPTION 3 - without Git**

Download the latest source zip from [Github](https://github.com/mutian/Sublime-CSS-Format) and extract it into a new folder named `CSS Format` in your Sublime Text "Packages" folder.


Usage
-----

Select the code, or place cursor in the document, and execute commands in one of the following ways:

* Context Menu: **CSS Format**.

* Edit Menu: **Edit &gt; CSS Format**.

* Command Panel: Open command panel: `Ctrl+Shift+P` (Linux/Windows) or `Cmd+Shift+P` (OS X) and select **Format CSS: XXX**.


Shortcuts
---------

By default, CSS Format provides no keyboard shortcuts to avoid conflicts, but you can read the included `Example.sublime-keymaps` file to get an idea how to set up your own.


Configuration
-------------

There are a number of configuration options available to customize the behavior on save. For the latest information on what options are available, select the menu item **Preferences &gt; Package Settings &gt; CSS Format &gt; Settings - Default**.

**DO NOT** edit the default settings. Your changes will be lost when CSS Format is updated. ALWAYS edit the user settings by selecting **Preferences &gt; Package Settings &gt; CSS Format &gt; Settings - User**.

* indentation: Format indentation, you can set it to `"  "`. By default, this is set to `"\t"`

* format_on_save: Set to `true` to trigger format on save. By default, this is set to `false`.

* format_on_save_action: Format action. You can refer to **Settings - Default**. By default, this is set to `"expand"`.

* format_on_save_filter: CSS Format matches the name of the file being saved against this regular expression to determine if a build should be triggered. By default, the setting has a value of `"\\.(css|sass|scss|less)$"`.


Author
------

Created by **Mutian** ([http://mutian.info](http://mutian.info/)).

For more info, you can send email to me: mutian(a)me.com!


Acknowledgements
----------------

For Chinese information, please visit [http://mutian.info/tech/1508](http://mutian.info/tech/1508).
