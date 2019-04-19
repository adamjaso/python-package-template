#!/usr/bin/env python3
import os
import sys
import six
import yaml
import shutil
from jinja2 import Template

if six.PY3:
    raw_input = input

here_dir = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))
basename = os.path.basename(os.path.realpath(os.path.abspath(__file__)))
root_prefix = os.path.splitdrive(sys.executable)[0] or '/'


def get_path(default_dirname, filename):
    if filename.startswith(root_prefix):
        return filename
    return os.path.join(default_dirname, filename)


def main():
    import argparse

    args = argparse.ArgumentParser()
    args.add_argument('-d', '--destination', dest='dest_dir', required=True)
    args.add_argument('-c', '--config', dest='config', default=None)
    args.add_argument('-n', '--name', dest='name', required=True)
    args.add_argument('-t', '--title', dest='title', required=True)
    args.add_argument('-p', '--path', dest='path', default='')
    args.add_argument('--license', dest='license', default='')
    args.add_argument('--license-title', dest='license_title', default='')
    args.add_argument('--author', dest='author')
    args.add_argument('--email', dest='email')
    args.add_argument('--description', dest='description', default='')
    args.add_argument('--url', dest='url', default='')
    args = args.parse_args()

    config = {k: '' for k in ['name', 'title', 'path', 'author', 'email',
                              'description', 'url', 'license', 'license_title',
                              ]}
    if args.config:
        config_file = os.path.abspath(args.config)
        with open(config_file) as f:
            _config = yaml.load(f)
            config.update(_config)

    if args.license:
        config['license'] = os.path.abspath(args.license)
    elif config.get('license'):
        config_dirname = os.path.dirname(config_file)
        config['license'] = os.path.join(config_dirname, config['license'])

    config['name'] = args.name
    config['path'] = args.path or args.name
    if args.description:
        config['description'] = args.description
    if args.author:
        config['author'] = args.author
    if args.title:
        config['title'] = args.title
    if args.url or 'url' not in config:
        config['url'] = args.url
    if args.license_title:
        config['license_title'] = args.license_title

    dest_dir = os.path.abspath(args.dest_dir)

    if os.path.isdir(dest_dir):
        if dest_dir == os.getcwd():
            return
        if 'y' == raw_input('Destination directory "{0}" exists? (Y/n) '
                            .format(dest_dir)).strip().lower():
            shutil.rmtree(dest_dir)
        else:
            print('Aborting...')
            return

    template_dir = os.path.join(here_dir, 'template')
    shutil.copytree(template_dir, dest_dir)

    # rename the package
    package_name1 = os.path.join(dest_dir, 'package')
    package_name2 = os.path.join(dest_dir, config['path'])
    package_name2_dirname = os.path.dirname(package_name2)
    if not os.path.isdir(package_name2_dirname):
        os.makedirs(package_name2_dirname)
        with open(os.path.join(package_name2_dirname, '__init__.py'), 'w') as f:
            f.write('')
    os.rename(package_name1, package_name2)

    # .gitignore
    gitignore = os.path.join(here_dir, '.gitignore')
    output_file = os.path.join(dest_dir, '.gitignore')
    shutil.copy(gitignore, output_file)

    # setup.py
    template_file = os.path.join(here_dir, 'setup.py.j2')
    output_file = os.path.join(dest_dir, 'setup.py')
    render_template_file(template_file, output_file, **config)

    # README.md
    template_file = os.path.join(here_dir, 'README.md.j2')
    output_file = os.path.join(dest_dir, 'README.md')
    render_template_file(template_file, output_file, **config)

    # LICENSE
    if config['license']:
        output_file = os.path.join(dest_dir, 'LICENSE')
        render_template_file(config['license'], output_file, **config)


def render_template_file(template_file, output_file, **context):
    with open(template_file) as f:
        template = f.read()
    with open(output_file, 'w') as f:
        data = Template(template).render(context)
        f.write(data)


if '__main__' == __name__:
    main()

