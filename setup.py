#!/usr/bin/env python3
import requests
import argparse
import os
import yaml
import logging
import sys


def load_yaml(yaml_file):
    with open(yaml_file, "r") as stream:
        return (yaml.safe_load(stream))


def write_user_config(module_name, sources):
    filename = 'user_config.tcl'
    with open(os.path.join('src', filename), 'w') as fh:
        fh.write("set ::env(DESIGN_NAME) {}\n".format(module_name))
        fh.write('set ::env(VERILOG_FILES) "\\\n')
        for line, source in enumerate(sources):
            fh.write("    $::env(DESIGN_DIR)/" + source)
            if line != len(sources) - 1:
                fh.write('\\\n')
        fh.write('"\n')


def get_project_source(yaml):
    # wokwi_id must be an int or 0
    try:
        wokwi_id = int(yaml['project']['wokwi_id'])
    except ValueError:
        logging.error("wokwi id must be an integer")
        exit(1)

    # it's a wokwi project
    if wokwi_id != 0:
        url = "https://wokwi.com/api/projects/{}/verilog".format(wokwi_id)
        logging.info("trying to download {}".format(url))
        r = requests.get(url)
        if r.status_code != 200:
            logging.warning("couldn't download {}".format(url))
            exit(1)

        # otherwise write it out
        filename = "user_module_{}.v".format(wokwi_id)
        with open(os.path.join('src', filename), 'wb') as fh:
            fh.write(r.content)
        return [filename, 'cells.v']

    # else it's HDL, so check source files
    else:
        if 'source_files' not in yaml['project']:
            logging.error("source files must be provided if wokiw_id is set to 0")
            exit(1)

        source_files = yaml['project']['source_files']
        if source_files is None:
            logging.error("must be more than 1 source file")
            exit(1)

        if len(source_files) == 0:
            logging.error("must be more than 1 source file")
            exit(1)

        if not 'top_module' not in yaml['project']:
            logging.error("must provide a top module name")
            exit(1)

        return source_files


# documentation
def check_docs(yaml):
    for key in ['author', 'title', 'description', 'how_it_works', 'how_to_test', 'language']:
        if key not in yaml['documentation']:
            logging.error("missing key {} in documentation".format(key))
            exit(1)
        if yaml['documentation'][key] == "":
            logging.error("missing value for {} in documentation".format(key))
            exit(1)


def get_top_module(yaml):
    wokwi_id = int(yaml['project']['wokwi_id'])
    if wokwi_id != 0:
        return "user_module_{}".format(wokwi_id)
    else:
        return yaml['project']['top_module']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="TT setup")

    parser.add_argument('--check-docs', help="check the documentation part of the yaml", action="store_const", const=True)
    parser.add_argument('--create-user-config', help="create the user_config.tcl file with top module and source files", action="store_const", const=True)
    parser.add_argument('--debug', help="debug logging", action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.INFO)
    parser.add_argument('--yaml', help="yaml file to load", default='info.yaml')

    args = parser.parse_args()
    # setup log
    log_format = logging.Formatter('%(asctime)s - %(module)-10s - %(levelname)-8s - %(message)s')
    # configure the client logging
    log = logging.getLogger('')
    # has to be set to debug as is the root logger
    log.setLevel(args.loglevel)

    # create console handler and set level to info
    ch = logging.StreamHandler(sys.stdout)
    # create formatter for console
    ch.setFormatter(log_format)
    log.addHandler(ch)

    if args.check_docs:
        logging.info("checking docs")
        config = load_yaml(args.yaml)
        check_docs(config)

    if args.create_user_config:
        logging.info("creating include file")
        config = load_yaml(args.yaml)
        source_files = get_project_source(config)
        top_module = get_top_module(config)
        write_user_config(top_module, source_files)
