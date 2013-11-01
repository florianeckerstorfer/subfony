import sublime
import sublime_plugin
import os
import re


class Pref:
    @staticmethod
    def load():
        settings = sublime.load_settings('subfony.sublime-settings')

        Pref.php_bin                = settings.get('subfony_php_bin')
        Pref.console_bin            = settings.get('subfony_console_bin')
        Pref.app_kernel             = settings.get('subfony_app_kernel')
        Pref.src_dir                = settings.get('subfony_src_dir')
        Pref.assets_install_symlink = settings.get('subfony_assets_install_symlink')
        Pref.bundle_format          = settings.get('subfony_bundle_format')
        Pref.bundle_structure       = settings.get('subfony_bundle_structure')
        Pref.route_format           = settings.get('subfony_route_format')
        Pref.template_format        = settings.get('subfony_template_format')
        Pref.entity_format          = settings.get('subfony_entity_format')
        Pref.entity_with_repository = settings.get('subfony_entity_with_repository')
        Pref.crud_with_write        = settings.get('subfony_crud_with_write')
        Pref.translation_format     = settings.get('subfony_translation_format')


st_version = 2
if sublime.version() == '' or int(sublime.version()) > 3000:
    st_version = 3

if st_version == 2:
    Pref.load()


def plugin_loaded():
    Pref.load()


class SubfonyBase(sublime_plugin.WindowCommand):
    def display_results(self):
        display = ShowInPanel(self.window)
        display.display_results()

    def window(self):
        return self.view.window()

    def run_shell_command(self, command, working_dir):
        if not command:
            return False

        if working_dir == '/' or working_dir == '':
            sublime.status_message('You\'re not in a Symfony2 application.')
            return

        self.view.window().run_command("exec", {
            "cmd": command,
            "shell": False,
            "working_dir": working_dir,
            "file_regex": ""
        })
        self.display_results()
        return True

    def find_symfony2_dir(self):
        if not self.view or not self.view.file_name():
            sublime.status_message('A file must be open. Sorry.')
            return
        cwd = os.path.dirname(self.view.file_name())
        while not os.path.exists(cwd + '/' + Pref.app_kernel) and cwd != '/' and cwd != '':
            cwd = os.path.dirname(cwd)

        return cwd

    def build_cmd(self, cmd):
        cmd.insert(0, Pref.php_bin)
        cmd.insert(1, Pref.console_bin)
        cmd.append('--no-interaction')

        return cmd


class SubfonyInputBase(SubfonyBase):
    def run(self):
        self.window.show_input_panel(self.INPUT_PANEL_CAPTION, '', self.on_done, None, None)
        self.view = self.window.active_view()


class SubfonyAsseticDumpCommand(SubfonyBase):
    def run(self):
        self.view = self.window.active_view()

        cmd = ['assetic:dump']
        self.run_shell_command(self.build_cmd(cmd), self.find_symfony2_dir())


class SubfonyAssetsInstallCommand(SubfonyBase):
    def run(self):
        self.view = self.window.active_view()

        cmd = ['assets:install']
        if Pref.assets_install_symlink == True:
            cmd.append('--symlink')

        self.run_shell_command(self.build_cmd(cmd), self.find_symfony2_dir())


class SubfonyCacheClearCommand(SubfonyBase):
    def run(self):
        self.view = self.window.active_view()

        cmd = ['cache:clear']
        self.run_shell_command(self.build_cmd(cmd), self.find_symfony2_dir())


class SubfonyCacheWarmupCommand(SubfonyBase):
    def run(self):
        self.view = self.window.active_view()

        cmd = ['cache:warmup']
        self.run_shell_command(self.build_cmd(cmd), self.find_symfony2_dir())


class SubfonyDoctrineDatabaseCreateCommand(SubfonyBase):
    def run(self):
        self.view = self.window.active_view()

        cmd = ['doctrine:database:create']
        self.run_shell_command(self.build_cmd(cmd), self.find_symfony2_dir())


class SubfonyDoctrineDatabaseDropCommand(SubfonyBase):
    def run(self):
        self.view = self.window.active_view()

        cmd = ['doctrine:database:drop', '--force']
        self.run_shell_command(self.build_cmd(cmd), self.find_symfony2_dir())


class SubfonyDoctrineSchemaCreateCommand(SubfonyBase):
    def run(self):
        self.view = self.window.active_view()

        cmd = ['doctrine:schema:create']
        self.run_shell_command(self.build_cmd(cmd), self.find_symfony2_dir())


class SubfonyDoctrineSchemaDropCommand(SubfonyBase):
    def run(self):
        self.view = self.window.active_view()

        cmd = ['doctrine:schema:drop', '--force']
        self.run_shell_command(self.build_cmd(cmd), self.find_symfony2_dir())


class SubfonyDoctrineSchemaUpdateCommand(SubfonyBase):
    def run(self):
        self.view = self.window.active_view()

        cmd = ['doctrine:schema:update', '--force']
        self.run_shell_command(self.build_cmd(cmd), self.find_symfony2_dir())


class SubfonyGenerateBundleCommand(SubfonyInputBase):
    INPUT_PANEL_CAPTION = 'Namespace:'

    def on_done(self, text):
        cmd = ['generate:bundle', '--dir=' + Pref.src_dir, '--namespace=' + text, '--format=' + Pref.bundle_format]
        if Pref.bundle_structure:
            cmd.append('--structure')

        self.run_shell_command(self.build_cmd(cmd), self.find_symfony2_dir())


class SubfonyGenerateControllerCommand(SubfonyInputBase):
    INPUT_PANEL_CAPTION = 'Controller:'

    def on_done(self, text):
        cmd = ['generate:controller', '--controller=' + text, '--route-format' + Pref.route_format, '--template-format' + Pref.template_format]
        self.run_shell_command(self.build_cmd(cmd), self.find_symfony2_dir())


class SubfonyGenerateDoctrineCrudCommand(SubfonyInputBase):
    INPUT_PANEL_CAPTION = 'Entity:'

    def on_done(self, text):
        cmd = ['generate:doctrine:crud', '--entity=' + text]
        if Pref.crud_with_write:
            cmd.append('--with-write')
        self.run_shell_command(self.build_cmd(cmd), self.find_symfony2_dir())


class SubfonyGenerateDoctrineEntitiesCommand(SubfonyInputBase):
    INPUT_PANEL_CAPTION = 'Name (Bundle, Namespace or Class):'

    def on_done(self, text):
        cmd = ['generate:doctrine:entities', text]
        self.run_shell_command(self.build_cmd(cmd), self.find_symfony2_dir())


class SubfonyGenerateDoctrineEntityCommand(SubfonyInputBase):
    INPUT_PANEL_CAPTION = 'Entity:'

    def on_done(self, text):
        cmd = ['generate:doctrine:entity', '--entity='+text, '--format='+Pref.entity_format]
        if Pref.entity_with_repository:
            cmd.append('--with-repository')
        self.run_shell_command(self.build_cmd(cmd), self.find_symfony2_dir())


class SubfonyGenerateDoctrineFormCommand(SubfonyInputBase):
    INPUT_PANEL_CAPTION = 'Entity:'

    def on_done(self, text):
        cmd = ['generate:doctrine:form', text]
        self.run_shell_command(self.build_cmd(cmd), self.find_symfony2_dir())


class SubfonyTranslationUpdateCommand(SubfonyInputBase):
    INPUT_PANEL_CAPTION = 'Bundle:'

    def on_done(self, text):
        self.text = text
        self.window.show_input_panel('Locale:', 'en', self.on_locale_done, None, None)

    def on_locale_done(self, locale):
        cmd = ['translation:update', locale, self.text, '--force', '--output-format'+Pref.translation_format]
        self.run_shell_command(self.build_cmd(cmd), self.find_symfony2_dir())


class SubfonyTwigLintCommand(SubfonyBase):
    def run(self):
        self.view = self.window.active_view()
        file_name = self.view.file_name()
        if re.search('\.twig$', file_name):
            cmd = ['twig:lint', file_name]
            self.run_shell_command(self.build_cmd(cmd), self.find_symfony2_dir())
        else:
            sublime.status_message('Not a Twig file: ' + file_name)


class ShowInPanel:

    def __init__(self, window):
        self.window = window

    def display_results(self):
        self.panel = self.window.get_output_panel("exec")
        self.window.run_command("show_panel", {"panel": "output.exec"})
