import os
import sys
import sentencepiece as spm
import random
import re
random.seed(12)

def train_spm():
    # Constants you may want to modify.
    save_path_prefix = 'vocabulary_10l'
    vocab_size = 64_000
    input_file_path = '/data/GitHubMining/spm_train_data_10l.txt'
    # Set up reserved tokens.
    SPACE_TOKEN = '▁'  # Note: not a regular underscore, but the SPM unicode symbol for a space
    TAB_TOKEN = chr(1)  # Assign rarely used ASCII chars for tabs and newlines. Can also pick rare unicode characters.
    NEWLINE_TOKEN = chr(2)
    # Reserve 1-24 spaces and 1-6 tabs.
    reserved_spaces = tuple(SPACE_TOKEN * i for i in range(1, 25))
    reserved_tabs = tuple(TAB_TOKEN * i for i in range(1, 7))
    # Add EOD and Pad token.
    # NOTE: You should add your proposed code/test file separator here too! There is no need to make sure it appears in the data here, however.
    reserved = ','.join(('<|endoftext|>', '<|padding|>', '<|codetestpair|>', *reserved_spaces, *reserved_tabs, NEWLINE_TOKEN))

    # Train command. Requires a generator of lines, which you may read from a file. Do *not* sanitize whitespace in said lines; we don't need to yet.
    spm.SentencePieceTrainer.train(
            input=input_file_path,
            #sentence_iterator=lines,
            model_prefix=save_path_prefix,
            vocab_size=vocab_size,
            character_coverage=0.9999,
            user_defined_symbols=reserved,
            split_by_whitespace=True,
            split_by_unicode_script=True,
            split_by_number=False,
            split_digits=True,  # Encouraged by the PaLM paper.
            max_sentencepiece_length=64,
            add_dummy_prefix=False,
            remove_extra_whitespaces=False,
            bos_id=-1,
            eos_id=1,
            pad_id=2,
            eos_piece='<|endoftext|>',
            pad_piece='<|padding|>',
            train_extremely_large_corpus=True)


if __name__ == '__main__':
    train_spm()