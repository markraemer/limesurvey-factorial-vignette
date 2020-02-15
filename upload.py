import base64
from limesurveyrc2api.limesurvey import LimeSurvey

url = "https://livinginsmarthomes.limequery.com/admin/remotecontrol"
username = ""
password = ""

surveyID = ""

# Open a session.
api = LimeSurvey(url=url, username=username)
api.open(password=password)

# Get a list of surveys the admin can see, and print their IDs.
result = api.survey.list_surveys()
#for survey in result:
    #print(survey.get("sid"))

# check if any questions have been uploaded previously
# this will replace all previous uploads
result = api.list_groups(surveyID)
if ('status' not in result):
    print("deleting all groups")
    for group in result:
        api.delete_group(surveyID,group['gid'])
#
print("uploading data ...")
up_file = open("output/question-group.lsg","r")
data =  up_file.read()
encoded = base64.b64encode(data.encode())

api.import_group(surveyID,encoded.decode(),"lsg")

# dirty hack to overcome group ordering problem
api.delete_group(surveyID,api.add_group(surveyID,"dummy","dummy"))

print("... done")

# Close the session.
api.close()
