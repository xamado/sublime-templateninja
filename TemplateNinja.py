import sublime
import sublime_plugin
import os.path
import re

from xml.etree import ElementTree # part of python distribution
from elementtree import SimpleXMLTreeBuilder # part of your codebase
ElementTree.XMLTreeBuilder = SimpleXMLTreeBuilder.TreeBuilder

class TemplateNinjaNewFileCommand(sublime_plugin.WindowCommand):
	plugin_name = 'TemplateNinja'
	debugOutput = ''

	def run(self):
		self.directories = None
		self.selected_directory = None

		self.formats = None

		self.debugOutput = ''

		self.show_directory_selection()

	def show_directory_selection(self):
		project_folder = self.get_project_folder()

		options = []
		directories = []

		# Create the regex for excluded directories
		patterns = [pat.replace('|', '\\') for pat in self.get_setting('folder_exclude_patterns')]
		patterns = '|'.join(patterns)
		self.excluded = re.compile(patterns)

		# Add the root directory as first option
		directories.append(project_folder)
		options.append([ "Root", project_folder])

		for root, dirs, files in os.walk(project_folder):
			for d in dirs:
				relative_path = os.path.join(root, d)[len(project_folder)+1:]
				if self.excluded != None and not self.excluded.search(relative_path):
					absolute_path = root + "/" + d
					directories.append(absolute_path)
					options.append([ relative_path, absolute_path ])

		# Add the special option for User's package path
		packages_path = sublime.packages_path() + "/User"
		directories.append(packages_path)
		options.append([ "Sublime User Package", packages_path ])

		self.directories = directories
		self.window.show_quick_panel(options, self.on_directory_selected, sublime.MONOSPACE_FONT)

	def on_directory_selected(self, id):
		self.selected_directory = self.directories[id]
		self.show_filename_entry()

	def show_filename_entry(self):
		self.window.show_input_panel("File name", "", self.on_file_name_entered, None, None)

	def on_file_name_entered(self, filename):
		# If the file already exists we need to ask for another name
		path = self.selected_directory + "/" + filename
		if os.path.exists(path):
			self.output("File already exists")
			self.show_filename_entry()
			return

		self.selected_path = path

		# First create the file, if the user escapes the template selection we want
		# him to be left on his nice and empty file
		self.create_file(path)

		# Now we ca show the template selection
		self.show_template_selection(filename)

	def show_template_selection(self, filename):
		# Grab the new view
		view = self.window.active_view()

		# Determine scope from file extension (TODO: Find a better way)
		filename, fileext = os.path.splitext(filename)
		#scope = self.get_scope_from_extension(fileext)
		#if scope == None:
		#	self.output("Couldn't find a template for this file type")
		#	return

		# Find templates for this file extension
		templates = self.find_templates_for_scope(fileext)

		self.output("Found " + str(len(templates)) + " templates")

		if len(templates) == 0:
			return

		self.templates = templates

		options = []
		for t in self.templates:
			description = t.find("description").text

			options.append([ description, fileext ])

		self.window.show_quick_panel(options, self.on_template_selected, sublime.MONOSPACE_FONT)

	def create_file(self, path):

		# Create the file and open the view
		open(path, 'w')
		self.window.open_file(path)


	def on_template_selected(self, id):
		template = self.templates[id]

		self.output("Selected " + template.find("description").text)
		self.insert_template(template.find("content").text)



	# def get_scope_from_extension(self, extension):
	# 	formats = self.get_setting("formats")
	# 	if formats == None:
	# 		return None

	# 	for format in formats:
	# 		if "."+format.get('extension') == extension:
	# 			return format.get('scope')

	def get_template_files(self, search_path):
		templates = []

		for root, dirnames, filenames in os.walk(search_path):
			for filename in filenames:
				if filename.endswith(".sublime-template"):
					templates.append(root + "/" + filename)

		return templates

	def find_templates_for_scope(self, extension):
		templates = []
		search_path = sublime.packages_path()

		extension = extension[1:]

		files = self.get_template_files(search_path)
		for f in files:

			# To properly handle the case when creating a new template using the
			# plugin, we need to skip the file if it's the one we are creating!
			if f == self.selected_path:
				continue

			# TODO: Can't figure out how to import ParseError
			#try:
			template = ElementTree.parse(open(f))

			node = template.find("extensions")
			if node == None:
				continue

			extensions = node.text.split(',')

			if extension in extensions:
				content = template.find("content").text
				templates.append(template)
			#except:
			#	self.output("Failed to parse: " + f)
			#	continue

		return templates

	def insert_template(self, template):
		view = self.window.active_view()

		if not view.is_loading():
			self.output("Inserting snippet")
			view.run_command("insert_snippet", { 'contents': template })
			return
		else:
			sublime.set_timeout(lambda: self.insert_template(template), 100)


	'''
	Some helpers
	'''
	def get_project_folder(self):
		if self.window:
			folders = self.window.folders()
	    	for folder in folders:
	    		return folder

	def output(self, value):
		self.debugOutput += value + '\n'

		panel_name = "SuperNewFile"
		panel = self.window.get_output_panel(panel_name)
		panel.set_read_only(False)
		panel.set_syntax_file('Packages/Text/Plain text.tmLanguage')
		edit = panel.begin_edit()
		panel.insert(edit, panel.size(), self.debugOutput)
		panel.end_edit(edit)
		panel.set_read_only(True)
		self.window.run_command("show_panel", {"panel": "output." + panel_name})

	def get_setting(self, key):
		settings = None
		view = self.window.active_view()

		if view:
		    settings = self.window.active_view().settings()

		if settings and settings.has(self.plugin_name) and key in settings.get(self.plugin_name):
		    # Get project-specific setting
		    results = settings.get(self.plugin_name)[key]
		else:
		    # Get user-specific or default setting
		    settings = sublime.load_settings(self.plugin_name + '.sublime-settings')
		    results = settings.get(key)

		if results == None:
			self.output("Setting " + key + " not found")

		return results