#!/usr/bin/env python

from distutils.core import setup

setup(
	name='pyclut',
	version='0.2',
	description='pyclutter widgets library',
	author='Eric Colleu',
	author_email='eric.colleu@gmail.com',
	url='http://code.google.com/p/pyclutter-widgets/',
	packages=[
		'pyclut',
		'pyclut.basics',
		'pyclut.controls',
		'pyclut.effects',
		'pyclut.effects.transitions',
		'pyclut.menus',
	],
)



