"""

generates questions groups for max two factors per vignette

-> question groups need to be pasted into a full survey file

"""
import json, os,shutil
from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    loader=PackageLoader('limesurvey', ''),
    autoescape=select_autoescape(['html', 'xml'])
)

# list all questions here
#data = {"1-1","1-2","1-3","2-1","2-2","3-1","3-2","3-3","3-4","4-0"}
data = ["03","05","10","15","17","18","25","30","50","55","60","65","70"]
#data = {"4-0"}



likert5 =  [{"answer" : "strongly disagree",
        "type" : "T"},
        {"answer" : "disagree",
        "type" : "T"},
        {"answer" : "neither agree nor disagree",
        "type" : "T"},
        {"answer" : "agree",
        "type" : "T"},
        {"answer" : "strongly agree",
        "type" : "T"}]

likert5like =  [{"answer" : "very unlikely",
        "type" : "T"},
        {"answer" : "unlikely",
        "type" : "T"},
        {"answer" : "don't know",
        "type" : "T"},
        {"answer" : "likely",
        "type" : "T"},
        {"answer" : "very likely",
        "type" : "T"}]

likert5important =  [{"answer" : "totally unimportant",
        "type" : "T"},
        {"answer" : "unimportant",
        "type" : "T"},
        {"answer" : "neither important nor unimportant",
        "type" : "T"},
        {"answer" : "important",
        "type" : "T"},
        {"answer" : "very important",
        "type" : "T"}]




goffset = 0
qoffset = 0
count=0
people_sqx = ''
people_sqy = []




for s in data:
    with open('data/'+s+'.json', encoding='utf8') as f:
        data = json.load(f)
    print(s)

    directory = "output/"+s
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)

    # store situation text temporarily
    temp_file = open("limesurvey/temp","w",encoding='utf-8')
    temp_file.write(data["situation"])
    temp_file.close()

    ### generate question groups - header
    template = env.get_template('question-group-head.xml')

    ##
    if 'relevance' not in data:
        relevance = ""
    elif data['relevance'] == 'people':
        relevance = " and ("
        for idx in range(0, len(people_sqy)):
            relevance = relevance + "regexMatch(\"/(?!^$|\\s+)/\", people_%s_%s.NAOK)" % (people_sqy[idx], people_sqx)
            if idx != len(people_sqy)-1:
                relevance = relevance + ' or '
            else:
                relevance = relevance + ')'
    else:
        relevance = data['relevance']


    out = template.render(factor1=data['factor1'], factor2=data['factor2'],
                          group_name=data['name'],goffset=goffset,relevance=relevance)

    out_file = open(directory+"/groups.lsg","w",encoding='utf-8')
    out_file.write(out)
    out_file.close()
    ### end generate header

    # generate for each groups
    count_groups = len(data['factor1']) * len(data['factor2'])

    for gnum in range(1, count_groups + 1):
        # counter
        goffset = goffset + 1
        tqtype = ""
        # for each question
        #   generate question
        #   sub questions
        #   answers

        for qnum in range(1, len(data['questions']) + 1):
            # counter
            qoffset = qoffset + 1
            question = data['questions'][qnum - 1]['question']
            qtype = data['questions'][qnum - 1]['qtype']

            # continue writing question
            # generate JS if necessary
            if qtype[0] == 'X':
                tqtype = qtype
                qtype = tqtype[1]



            if 'code' not in data['questions'][qnum - 1]:
                code = "0"
            else:
                code = data['questions'][qnum - 1]['code']

            qid = qoffset
            gid = goffset


            # start generating for subquestions
            if 'subquestions' in data['questions'][qnum - 1]:
                subquestions = data['questions'][qnum - 1]['subquestions']

                dd_data = {}

                # populate with people Parameters (previously collected)
                if tqtype == 'XF':
                    subquestions = []
                    for idx in range(0, len(people_sqy)):
                        subquestions.append({})
                        subquestions[idx]['type'] = 'F'
                        subquestions[idx]['subquestion'] = '{people_%s_%s}' % (people_sqy[idx], people_sqx)


                for sqnum in range(1, len(subquestions) + 1):
                    # counter and data
                    qoffset = qoffset + 1
                    tqid = qoffset
                    sqtype = subquestions[sqnum - 1]['type']
                    sqtitle = "SQ" + str(tqid)
                    text = subquestions[sqnum - 1]['subquestion']

                    if 'scale' not in subquestions[sqnum - 1]:
                        scale = "0"
                    else:
                        scale = subquestions[sqnum - 1]['scale']
                        # special case for access to names
                        #TODO need to make sure 4-0 is generated before 4-1!
                        if tqtype == 'X;':
                            if scale == '1' and text == 'nickname':
                                people_sqx = sqtitle
                            elif scale == '0':
                                people_sqy.append(sqtitle)

                    template = env.get_template('question-group-body-sub.xml')

                    # X; qtype - treat array with dropdown
                    if sqtype == 'TD':
                        sqtype = 'T'
                        dd_data[sqnum]={'id':sqtitle,'options':subquestions[sqnum - 1]['options']}

                    out = template.render(qid=tqid,pqid=qid,gid=gid,code=sqtitle,
                                          sqtype=sqtype,sqtitle=sqtitle,text=text,scale=scale).encode('utf-8')

                    out_file = open(directory + "/questions-sub-"+str(gid)+"-"+str(tqid)+ ".lsg", "wb")
                    out_file.write(out)
                    out_file.close()

            # start generating sub type answers
            if 'answers' in data['questions'][qnum - 1]:

                answers = data['questions'][qnum - 1]['answers']

                ## customisation ##
                # use likert scale with 5 options
                if isinstance(answers, str) and answers.startswith('likert'):
                    answers = locals()[answers]

                ## customisation ##
                # populate with people Parameters (previously collected)
                if tqtype == 'X!':
                    answers = []
                    for idx in range(0, len(people_sqy)):
                        answers.append({})
                        answers[idx]['value'] = idx
                        answers[idx]['answer'] = '{people_%s_%s}' % (people_sqy[idx], people_sqx)

                    ## adding options for 3rd parties getting involved in household configuration
                    answers.append({})
                    answers[len(answers)-1]['value'] = len(answers)-1
                    answers[len(answers)-1]['answer'] = 'a friend'
                    answers.append({})
                    answers[len(answers)-1]['value'] = len(answers)-1
                    answers[len(answers)-1]['answer'] = 'a colleague'
                    answers.append({})
                    answers[len(answers)-1]['value'] = len(answers)-1
                    answers[len(answers)-1]['answer'] = 'a neighbour'
                    answers.append({})
                    answers[len(answers)-1]['value'] = len(answers)-1
                    answers[len(answers)-1]['answer'] = 'a contractor'

                for sqnum in range(1, len(answers) + 1):
                    # counter and data
                    qoffset = qoffset + 1
                    tqid = qoffset
                    sqtitle = "A" + str(tqid)
                    value = sqnum
                    text = answers[sqnum - 1]['answer']

                    if 'scale' not in answers[sqnum - 1]:
                        scale = "0"
                    else:
                        scale = answers[sqnum - 1]['scale']

                    template = env.get_template('question-group-body-answer.xml')

                    out = template.render(pqid=qid,code=sqtitle,text=text,scale=scale,value=value).encode('utf-8')

                    out_file = open(directory + "/questions-answer-"+str(gid)+"-"+str(tqid)+ ".lsg", "wb")
                    out_file.write(out)
                    out_file.close()

            # generate questions - body

            template = env.get_template('question-group-body.xml')
            out_body = template.render(question=question,gid=gid,qid=qid,
                                  count_groups=count_groups,qtype=qtype,code=code)

            if tqtype == 'X;':
                # generate and append to question
                template = env.get_template('people.js')
                out = template.render(data=dd_data)
                out_body = out_body.replace("{{code}}",out)
                qtype = 'XX'

            out_file = open(directory + "/questions-M"+str(gid)+" "+str(qid)+".lsg","w",encoding='utf-8')
            out_file.write(out_body)
            out_file.close()
