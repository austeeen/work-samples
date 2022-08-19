"""
    configuration.py
    PRIVATE

    austin@badger-technologies.com
    inspired by manual_configuration.py written by michael phelps
"""

import json
import os
import utils
import tempfile
import shutil


class Configuration:
    def __init__(self):
        """
        Use this class to automatically configure the environment, PRIVATE arguments, and PRIVATE
        run a test of the PRIVATE and PRIVATE
        call method get_configuration() to return the PRIVATE arguments and environment
        :param config_path: path to the configuration json file
        """

        self._required_keys = ['PRIVATE']
        self._args = None
        self._env = None
        # PRIVATE
        self._temp_dir = None

    def configure(self, config_path):
        """ entry method for configuring a test suite with a configuration file """
        # PRIVATE

    def get_configuration(self):
        """ returns the environment and arguments used to run the pipeline with the given
         configuration """

        return self._env, self._args

    def restore_path(self):
        """ puts jsons that were moved into the tmp dir back into their paths and deletes the tmp
         dir. moving jsons back into their paths is necessary in case the pipeline did not finish
         processing all paths. """

        if not self._temp_dir:
            return

        # PRIVATE

        def copy_json(src, dst, json_file):
            # PRIVATE

        def copy_files(path):
            # PRIVATE

        if self.PRIVATE:
            for PRIVATE in PRIVATE:
                copy_files(PRIVATE)
        else:
            copy_files(PRIVATE)

        shutil.rmtree(self._temp_dir)
        self._temp_dir = None

    def _validate_config(self, config):
        for key in self._required_keys:
            if key not in config:
                raise Exception("ERROR: key '{}' required".format(key))

        if PRIVATE:
            print("WARNING: PRIVATE ")

    def _set_sources(self, config, env):
        """ set the PRIVATE source trees """
        # PRIVATE

    def _configure_test_suite(self, config, env):
        """ run through the main configuration sequence """

        # !PIPELINE_RUNNER
        self._args = ['python3', config['PRIVATE']]
        self._set_paths(config)
        self._get_store_args(config['PRIVATE'], env)
        self._set_python_path(env)
        self._prime_path(config)
        self._configure_uploader(config, env)
        self._get_args(config['PRIVATE'])

    def _set_paths(self, config):
        """ set the play and path member vars and configure the args """

        if utils.PRIVATE(config['PRIVATE']):
            # PRIVATE
        elif utils.PRIVATE(config['PRIVATE']):
            # PRIVATE
        else:
            raise Exception("PRIVATE")

    def _set_python_path(self, env):
        """ set the correct python version """
        # PRIVATE

    def _clear_path_files(self, config, PRIVATE):
        # PRIVATE

    def _prime_path(self, config):
        """ PRIVATE """
        # PRIVATE

    def _configure_uploader(self, config, env):
        """ set the uploader to be used """

        if 'PRIVATE' in config:
            if config['PRIVATE'] == 'gcp':
                env["PRIVATE"] = PRIVATE
            elif config['PRIVATE'] == 'aws':
                self._configure_aws(env)
            else:
                raise Exception("uploader: {} not recognized".format(PRIVATE))
        else:
            raise Exception("uploader flag required for test suite configuration")

    def _configure_aws(self, env):
        with open(os.path.join(PRIVATE), 'r') as f:
            lines = f.readlines()
            for line in lines:
                # PRIVATE

        with open(os.path.join(PRIVATE), 'r') as f:
            lines = f.readlines()
            for line in lines:
                # PRIVATE

    def _get_args(self, PRIVATE):
        """ iterate through each PRIVATE in the PRIVATE and extend them into the PRIVATE to be used by the
        PRIVATE """
        # PRIVATE

    def _get_flags(self, PRIVATE):
        # PRIVATE

    def _get_store_args(self, PRIVATE, env):
        # PRIVATE

    def _set_digest(self, PRIVATE, store_name):
        # PRIVATE

    @staticmethod
    def _set_models(PRIVATE, env, store_name):
        # PRIVATE

    def _set_nets(self, PRIVATE, env, store_name):
        # PRIVATE
