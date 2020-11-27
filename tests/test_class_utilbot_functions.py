#! python3
# test_class_utilbot_functions.py

import difflib
import json
import os
import re
import unittest

class TestOnMessage(unittest.TestCase):
    def test_introductions_regex(self):
        samples = {
            '*introduction': True, '*help': True}
        regex = re.compile(r'^\*(introduction|help$)')
        results = []
        for sample in samples:
            results.append(
                bool(regex.search(sample)) == samples[sample])
        self.assertTrue(all(results))

    def test_members_regex(self):
        samples = {
            '*member_name': True, '*member_nickname': True}
        regex = re.compile(r'^\*(member_name|member_nickname)')
        results = []
        for sample in samples:
            results.append(
                bool(regex.search(sample)) == samples[sample])
        self.assertTrue(all(results))

    def test_game_codes_regex(self):
        samples = {
            'ABCDEF': True, 'abcdef': True, '123456': False, 'abc': False,
            'abcdefghi': False}
        regex = re.compile(r'^[A-Za-z]{6}$')
        results = []
        for sample in samples:
            results.append(
                bool(regex.search(sample)) == samples[sample])
        self.assertTrue(all(results))

class TestCommandIntroduction(unittest.TestCase):
    def test_regex(self):
        samples = {
            '*introduction': False, '*introduction Name': False,
            '*introduction FirstLast': False, '*introduction First Last': True,
            '*introduction FLast': False, '*introduction FirstL': False,
            '*introduction F Last': False, '*introduction First L': False,
            '*introduction First M Last': False,
            '*introduction First Middle Last': False}
        regex = re.compile(r'^\*introduction(\s[A-Z][a-z]+){2}$')
        results = []
        for sample in samples:
            results.append(
                bool(regex.search(sample)) == samples[sample])
        self.assertTrue(all(results))

    def test_file_update(self):
        sample = {
            'First0 Last0': 'First0Last0', 'First1 Last2': 'First1Last1',
            'First2 Last2': 'First2Last2', 'First3 Last3': 'First3Last3'}
        with open('SAMPLE_members.txt', 'w') as jsonfile:
            data = json.dump(sample, jsonfile)
        sample['First0 Last0'] = 'Last0First0'
        sample['First4 Last4'] = 'First4Last4'

        with open('SAMPLE_members.txt', 'r') as jsonfile:
            data = json.load(jsonfile)
        with open('SAMPLE_members.txt', 'w+') as jsonfile:
            data['First0 Last0'] = 'Last0First0'
            data['First4 Last4'] = 'First4Last4'
            json.dump(data, jsonfile)

        with open('SAMPLE_members.txt', 'r') as jsonfile:
            data = json.load(jsonfile)
        os.remove('SAMPLE_members.txt')
        self.assertEqual(sample, data)

class TestCommandMemberName(unittest.TestCase):
    def test_regex(self):
        samples = {
            '*member_name Plain': True, '*member_name Plain#1234': True,
            '*member_name Num1': True, '*member_name Num1#1234': True,
            '*member_name Symbol!': True, '*member_name Symbol!#1234': True,
            '*member_name QWERTYUIOPASDFGHJKLZXCVBNM1234567890': False,
            '*member_name QWERTYUIOPASDFGHJKLZXCVBNM1234567890#1234': False,
            '*member_name': False, '*member_name H': False}
        regex = re.compile(r'^\*member_name\s(.{2,32})(#\d{4})?$')
        results = []
        for sample in samples:
            results.append(
                bool(regex.search(sample)) == samples[sample])
        self.assertTrue(all(results))

class TestCommandMemberNickname(unittest.TestCase):
    def test_regex(self):
        samples = {
            '*member_nickname': False, '*member_nickname Name': False,
            '*member_nickname FirstLast': False,
            '*member_nickname First Last': True,
            '*member_nickname FLast': False,
            '*member_nickname FirstL': False,
            '*member_nickname F Last': False,
            '*member_nickname First L': False,
            '*member_nickname First M Last': False,
            '*member_nickname First Middle Last': False}
        regex = re.compile(r'^\*member_nickname(\s[A-Z][a-z]+){2}$')
        results = []
        for sample in samples:
            results.append(
                bool(regex.search(sample)) == samples[sample])
        self.assertTrue(all(results))

if __name__ == '__main__':
    unittest.main()