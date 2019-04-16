# coding: utf-8
# you can use this script to generate urls of all topic action videos,
# then you can download them with uget software on ubuntu

# !/usr/bin/python
# -*- coding: utf-8 -*-

if __name__ == "__main__":
    with open("ins.action.topics") as f:
    	lines = f.readlines()
    	for line in lines:
    		file = line.split(" ")[1][:-1] + ".mp4"
    		remote = 'https://www-nlpir.nist.gov/projects/tv2019/active/INS/topics/actions.examples/' +  file
    		print(remote)


