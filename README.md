# TemplateNinja for Sublime Text 2


This package enables you to create new files based on a pre-defined template file.

Although the same can be achieved by creating a new file and using a snippet, sometimes this just won't work since the buffer is empty and still has no valid scope, for example when creating an empty PHP file the default scope is html, and thus any snippets that have a scope of source.php won't show up until you properly enclose a region with <?php ?>, which get's tedious quickly.

Using TemplateNinja you can just create a new file and directly choose from a valid template per your project settings and the file's extension.

Additionally TemplateNinja includes a directory browser using the Command Palette for quick fuzzy directory selection, for example to create a new file in Abc/MyProject/Code/Controller/ you can just type Controller and hit enter instead of having to type the full path to the file or selecting the folder from the sidebar (if you even use it).

## Installation

### Package Control (TODO: Still not published)

Installing the package with Package Control is quick and easy, and you most likely are familiar with the procedure, but if not:

Bring up the Command Palette (Command+Shift+p on OS X, Control+Shift+p on Linux/Windows).
Select "Package Control: Install Package" (it'll take a few seconds)
Select TemplateNinja when the list appears.

### Clone from Github

    git clone http://github.com/xamado/sublime-templateninja

## Usage

To use TemplateNinja either bring up the Command Palette and select TemplateNinja: Create New File or press the configured keybinding (defaults to ctrl+shift+n)

1. In the quick panel that pops up type the name of the folder you want to put your file in, or at least part of it until you find it, and select it
2. Now you will get an input on the bottom side of the window to type the file name, hit enter
3. Another quick panel will now popup showing you the list of possible templates associated with your project and file, select one
4. Now your file will be created and the template inserted, you can set each attribute as with normal templates by typing and pressing tab to move to the next one

## Excluding directories

The plugin supports excluding a list of directories from the directory list, you can override this setting either in your User preferences, or in the project file (my preferred method)

    "settings": {
      	"TemplateNinja": {
    			"folder_exclude_patterns": [ ".git", ".svn", "vendor", "app/cache" ]
    		}
    }
    
## Keybindings

The plugin by default installs a keybinding, but in case it doesn't work for you or if you want to change it, here's the definition that is required

    [
      { "keys": ["ctrl+super+n"], "command": "template_ninja_new_file"}
    ]

## Creating Templates

Templates are basically snippet files, with different extra data, but it's pretty easy to convert a snippet you might already have laying around to be used as a template. 

To use them, simply create the template and add it to your User package, TemplateNinja will load all files with the extension sublime-template from the packages directory automatically. Fill in the <extensions> tag with a comma separate list of extensions you want this template to apply to (don't include the dots) and <description> with a user-readable short description of what the template is.

Here's an example of the included PHP Class template:

    <template>
        <content><![CDATA[<?php
    
    class ${1:$name} ${2:extends ${3:SomeClass}} 
    {
        function __construct()
        {
    		  $0
        }
    }
    
    ?>
    ]]></content>
        <extensions>php</extensions>
        <description>PHP Class</description>
    </template>

## Contributing

I can't possibly make default templates for all the languages out there, specially if it's for a language I don't typically use, so feel free to create your templates and share them back, just fork and submit a PR :)

## Thanks

Thanks to all the plugin authors out there for making plugins that both make my life with Sublime Text 2 easier and are also a great learning resource for developing Sublime plugins, and learning Python since this is like my second time using it, and the previous one was 10 years ago
