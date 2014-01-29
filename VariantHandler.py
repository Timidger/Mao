# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 13:15:40 2012

@author: Preston
"""
import json, os
from Variant import Variant

class VariantHandler(object):
    """Handles the variant saving/loading"""
    def __init__(self, variants = None, directory = None,
                 file_extension = '.json'):
        if directory is None:
            self.directory = os.getcwd() + '{0}Variants{0}'.format(os.sep)
            if not os.path.exists(self.directory):
                self.directory = os.getcwd()
        if variants is None:
            self.variants = []
        else:
            self.variants = list(variants)
        self.file_extension = file_extension

    def change_directory(self, path):
        if os.path.exists(path):
            self.directory = path

    def add_variant(self, variant):
        """Adds the variant to the list of variants if it is not already a
        part of the list"""
        if isinstance(variant, Variant) and variant not in self.variants:
            self.variants.append(variant)
        elif variant in self.variants:
            return 'Variant already loaded!'

    def remove_variant(self, variant):
        """Removes the variant from the list of variants, but retains the
        file"""
        if variant in self.variants and isinstance(variant, Variant):
            self.variants.remove(variant)
        elif variant not in self.variant:
            return 'Variant not loaded'

    def save_variant(self, variant, directory = None):
        """Saves a variant to directory, defaulting to Variant folder"""
        assert isinstance(variant, Variant)
        if not directory:
            directory = self.directory
        if os.path.exists(directory):
            with open(directory + variant.name + self.file_extension, 'w') as (
            v_file):
                v_file.write(json.dumps(variant))
        else:
            raise IOError ('Not a valid path')

    def load_variant(self, variant, directory = None):
        """Loads a variant from a directory, which defaults to the Variant
        folder in the execution directory, and puts it in the VH list"""
        assert type(variant) == str
        if not variant.endswith(self.file_extension):
            variant = variant + self.file_extension
        if not directory:
            directory = self.directory
        if variant in self.get_variant_files(directory):
            with open(directory + variant, 'r') as txtfile:
                self.add_variant(json.load(txtfile))
        else:
            raise IOError ("Couldn't find file")

    def delete_variant(self, variant, directory = None):
        """Deletes the file from the directory"""
        assert type(variant) == str
        if not variant.endswith(self.file_extension):
            variant = variant + self.file_extension
        if not directory:
            directory = self.directory
        if os.path.exists(directory + variant):
            os.remove(directory + variant)

    def get_variant_files(self, directory):
        """Returns all the files ending with the Handler's file_extension in
        the given directory"""
        if os.path.exists(directory):
            return list(
            txt_file for txt_file in os.listdir(directory) if (
            txt_file.endswith(self.file_extension)))
