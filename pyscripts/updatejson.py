import requests
import json
import sys
sys.path.append('utilities')

#Use the subjects url to write the json response to subjects.json
subjects_url = "https://sis.rutgers.edu/oldsoc/subjects.json?semester=92020&campus=NB&level=U"
with open('apidata/subjects.json', 'w') as f:
    f.write(requests.get(subjects_url).text)

#After updating subjects.json, import the subject list
from getsubjects import subject_list

#Update classes
with open('apidata/classes.json', 'w') as f:
    subject_to_courses = {}

    #Go through each subject, access the classes using the code, map subject to its courses
    for subject in subject_list:
        code = subject['code']
        courses_url = f'http://sis.rutgers.edu/oldsoc/courses.json?subject={code}&semester=92020&campus=NB&level=U'
        courses = json.loads(requests.get(courses_url).text)
        
        subject_to_courses[subject['description']] = courses

    #Dump the mapping of subjects to courses in classes file
    json.dump(subject_to_courses, f)


#Create mapping from index to section and class info
with open('apidata/indextoclass.json', 'w') as f:
    index_to_class = {}

    #Go through each subject
    for subject in subject_list:
        #Each course in the subject
        for course in subject_to_courses[subject['description']]:
            #Each section in the course
            for section in course['sections']:

                #Map its index to info like subject, name, section, course, instructors
                index_to_class[section['index']] = {
                    'subject':subject['description'],
                    'name':course['title'],
                    'section':section['number'],
                    'course':f'01:{subject["code"]}:{course["courseNumber"]}',
                    'instructors':'; '.join([x['name'] for x in section['instructors']])
                }
    
    #Dump the dict into indextoclass
    json.dump(index_to_class, f)
