"""

generates questions groups for max two factors per vignette

-> question groups need to be pasted into a full survey file

"""
import json, os, glob


questions = ""
for file in glob.glob("output/**/questions-M*"):
    text = open(file,"r", encoding='utf-8')
    questions = questions + text.read()

subquestions = ""
for file in glob.glob("output/**/questions-sub-*"):
    text = open(file,"r", encoding='utf-8')
    subquestions = subquestions + text.read()

answers = ""
for file in glob.glob("output/**/questions-answer*"):
    text = open(file,"r", encoding='utf-8')
    answers = answers + text.read()

groups = ""
for file in glob.glob("output/**/groups*"):
    text = open(file,"r", encoding='utf-8')
    groups = groups + text.read()

# generate survey file
file = open("limesurvey/question-group.xml")
template = file.read()

out = template.replace("{% groups %}",groups)
out = out.replace("{% questions %}", questions)
out = out.replace("{% subquestions %}",subquestions)
out = out.replace("{% answers %}",answers)

out_file = open("output/question-group.lsg","wb")
out_file.write(out.encode('UTF-8'))
out_file.close()
