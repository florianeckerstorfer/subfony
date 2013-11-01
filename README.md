Subfony
=======

Subfony provides useful integrations for Symfony2 developers in Sublime Text. Developed by [Florian Eckerstorfer](http://florianeckerstorfer.com) in Vienna.


Commands
--------

This list shows the commands supported by Subfony and the corresponding name in Symfony.

- Subfony: Assetic Dump → `assetic:dump`
- Sbufony: Assets Install → `assets:install`
- Subfony: Cache Clear → `cache:clear`
- Subfony: Cache Warm up → `cache:warmup`
- Subfony: Doctrine Create Database → `doctrine:database:create`
- Subfony: Doctrine Drop Database → `doctrine:database:drop --force`
- Subfony: Doctrine Create Schema → `doctrine:schema:create`
- Subfony: Doctrine Drop Schema → `doctrine:schema:drop --force`
- Subfony: Doctrine Update Schema → `doctrine:schema:update --force`
- Subfony: Generate Bundle → `generate:bundle`
- Subfony: Generate Controller → `generate:controller`
- Subfony: Generate Doctrine CRUD → `generate:doctrine:crud`
- Subfony: Generate Doctrine Entites → `generate:doctrine:entities`
- Subfony: Generate Doctrine Entity → `generate:doctrine:entity`
- Subfony: Generate Doctrine Form → `generate:doctrine:form`
- Subfony: Update Translation → `translation:update`
- Subfony: Lint Twig → `twig:lint`

Configuration
-------------

    {
        // Path to the PHP executable
        "subfony_php_bin": "/usr/bin/php",

        // Path to the Symfony2 console executable (from the Symfony2 root directory)
        "subfony_console_bin": "app/console",

        // Directory in the Symfony2 root directory to store bundles in
        "subfony_src_dir": "src",

        // Whether to run assets:install command with --symlink option
        "subfony_assets_install_symlink": false,

        // Format of configuration files (php, xml, yml or annotation)
        "subfony_bundle_format": "annotation",

        // Whether to run generate:bundle with --structure option
        "subfony_bundle_structure": false,

        // Format of routes (php, xml, yml or annotation)
        "subfony_route_format": "annotation",

        // Format of templates (php or twig)
        "subfony_template_format": "twig",

        // Format of entities (php, xml, yml or annotation)
        "subfony_entity_format": "annotation",

        // Whether to run generate:doctrine:entity with the --with-repository option
        "subfony_entity_with_repository": false,

        // Whether to run generate:doctrine:crud with the --with-write option
        "subfony_crud_with_write": true,

        // Format of translations (php, xlf, po, mo, yml, ts, csv, ini and res)
        "subfony_translation_format": "yml"
    }





License
-------

See [LICENSE](https://github.com/florianeckerstorfer/subfony/blob/master/LICENSE).
