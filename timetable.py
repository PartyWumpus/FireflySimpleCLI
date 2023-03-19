import json
import requests
from datetime import datetime, timedelta
import sys

app_id = 'SimpleFireflyCLI'

secret = 'tsgT9UVHKlcIlbAPjqq5_Q8yx8wLlGGEBzojCTROLyv3Oz3ZXecW6Nvz3mWZkSB2I1'
pupil_guid = "GUID:GUID"
url = 'https://school.fireflycloud.net'
jsonfile = None
#jsonfile = "/optional/path/for/a/cache.json"

# this is based on the end times for each lesson
time_names = {}
"""
time_names = {
    "09:00": "Registration", "10:05": "Period 1", "11:10": "Period 2", "12:30": "Period 3", "13:40": "Lunchtime",
    "13:55": "Registration 2", "14:55": "Period 4", "16:00": "Period 5"}
"""

# uses escape codes for colors
lesson_colors = {}
"""
lesson_colors = {
    "Sports": "\033[35m", "FM": "\033[34m", "Stats/Mechanics": "\033[34m", "Pure": "\033[34m",
    "Physics": "\033[36m", "Computing": "\033[31m", "Electronics": "\033[33m", "PSHE": "\033[35m"
}
"""

# I have one lesson called "FM" for maths, so I have to find out which lesson
# it actually is based on the teacher. You may not need this, so you can just remove this variable
# and the `if subject == "FM"` bit below in print_lessons
maths_teachers = {"Mrs J Jameson": "Stats/Mechanics", "Mr P Parker": "Pure", "Mr O Octavius": "Pure"}

def write_json(data, date):
    with open(jsonfile,'r+') as file:
        file_data = json.load(file)
        file_data["data"][date] =data
        file.seek(0)
        json.dump(file_data, file, indent = 4)

def update_cache(): # this is very ineffecient :)
    today = datetime.strptime(datetime.today().strftime("%Y-%m-%d"), "%Y-%m-%d")
    for i in range(0,14):
        get_timetable(today + timedelta(days=i), today + timedelta(i+1))


def get_timetable(start_datetime, end_datetime):
    event_start = start_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
    event_end = end_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
    if jsonfile != None: # load the cache
        with open(jsonfile) as file:
            data = json.load(file)
            try:
                return data["data"][event_start]
            except KeyError:
                pass

    query = f"""
    {{
        events(start: "{event_start}", for_guid: "{pupil_guid}", end: "{event_end}") {{
            end, location, start, subject, description, guid, attendees {{
                role, principal {{
                    guid, name 
                }}
            }}
        }}
    }}
    """
    x = requests.post(
        url + f"/_api/1.0/graphql?ffauth_device_id={app_id}&ffauth_secret={secret}",
        data={'data': query},
        headers={'Content-Type': 'application/x-www-form-urlencoded'})
    if x.status_code == 200:
        if jsonfile != None: # write to the cache
            write_json(x.json(), event_start)
        return x.json()
    else:
        raise Exception(f"Unexpected status code returned: {x.status_code}")


def check_token():
    x = requests.get(url + f"/Login/api/verifytoken?ffauth_device_id={app_id}&ffauth_secret={secret}")
    data = json.loads(x.content)
    if not data['valid']:
        raise Exception("API response says token is invalid")
    return True


def print_tasks(done):
    # find all open tasks
    task_json = {
        "archiveStatus": "All",
        "completionStatus": f"{done}",
        "ownerType": "OnlySetters",
        "page": 0,
        "pageSize": 100,
        "sortingCriteria": [
            {
                "column": "DueDate",
                "order": "Descending"
            }
        ]
    }  # data used for task query
    x = requests.post(
        url + f"/api/v2/taskListing/view/student/tasks/all/filterBy?ffauth_device_id={app_id}&ffauth_secret={secret}",
        json=task_json)
    data = json.loads(x.content)
    for task in data['items']:
        print()
        print(f"{task['title']}")
        print(f"from {task['setter']['name']}")

        due_date = datetime.strptime(task['dueDate'], "%Y-%m-%d")
        now_date = datetime.strptime(datetime.today().strftime("%Y-%m-%d"), "%Y-%m-%d")
        delta = due_date - now_date
        if delta.days == -1:
            print(f"due {task['dueDate']} (\033[31myesterday\033[0m)")
        elif delta.days == 0:
            print(f"due {task['dueDate']} (\033[33mtoday!\033[0m)")
        elif delta.days == 1:
            print(f"due {task['dueDate']} (\033[33mtomorrow!\033[0m)")
        elif delta.days > 1:
            print(f"due {task['dueDate']} (in {delta.days} days)")
        elif delta.days < 0:
            print(f"due {task['dueDate']} (\033[31m{abs(delta.days)} days ago\033[0m)")



def print_timetable(date):
    now = datetime.now()
    today = datetime.strptime(now.strftime("%Y-%m-%d"), "%Y-%m-%d")

    timetable = get_timetable(date, date + timedelta(days=1))
    if len(timetable['data']['events']) == 0:
        print("Timetable is empty")
    displayedTime = False
    for event in timetable['data']['events']:
        time_name = datetime.strptime(event['end'], "%Y-%m-%dT%H:%M:%SZ").strftime("%H:%M")
        if time_name in time_names:
            time_name = time_names[time_name]

        location = event['location']
        if location == "":
            location = event['subject']
        color_code = ""
        if event['subject'] in lesson_colors:
            color_code = lesson_colors[event['subject']]
        if datetime.strptime(event['end'], "%Y-%m-%dT%H:%M:%SZ") > now and not displayedTime and date == today:
            displayedTime = True
            print(f"-- {now.strftime('%H:%M')} --")
        print(f"{time_name}:{color_code} {location} \033[0m")

def print_colors():
    for lesson in lesson_colors:
        print(f"{lesson_colors[lesson]}{lesson} \033[0m")

def print_lessons(date):
    timetable = get_timetable(date, date + timedelta(days=1))

    lessons = set()
    for event in timetable['data']['events']:
        subject = event['subject']
        if subject == "FM":
            teacher = event['attendees'][0]['principal']['name']
            try:
                lessons.add(maths_teachers[teacher])
            except KeyError:
                lessons.add(subject)
        else:
            lessons.add(subject)
    if "Registration" in lessons:
        lessons.remove("Registration")
    if len(lessons) == 0:
        print("Timetable is empty")
    for lesson in lessons:
        if lesson in lesson_colors:
            print(f"{lesson_colors[lesson]}{lesson}\033[0m")
        else:
            print(lesson)


### MAIN ###


arg1 = None
arg2 = None
try:
    arg1 = str(sys.argv[1])
    arg2 = str(sys.argv[2])
except IndexError:
    pass

date = datetime.strptime(datetime.today().strftime("%Y-%m-%d"), "%Y-%m-%d")
done = "Todo"

match arg2:
    case "todo":
        done = "Todo"
    case "done":
        done = "DoneOrArchived"
    case "both":
        done = "AllIncludingArchived"
    case "today":
        date = datetime.strptime(datetime.today().strftime("%Y-%m-%d"), "%Y-%m-%d")
    case "tomorrow":
        date = datetime.strptime(datetime.today().strftime("%Y-%m-%d"), "%Y-%m-%d") + timedelta(days=1)
    case None:
        pass
    case _:
        date = datetime.strptime(arg2, "%d/%m/%Y")

match arg1:
    case "lessons":
        print_lessons(date)
        quit()
    case "timetable":
        try:
            if jsonfile != None:
                update_cache()
        except ConnectionError:
            print("(cache failed to update)")
        print_timetable(date)
        quit()
    case "tasks":
        print_tasks(done)
        quit()
    case "colors":
        print_colors()
        quit()
    case "help":  # makes it so there isn't an error message when user asks for help
        pass
    case None:
        print(f"please choose an option")
    case _:
        print(f"{sys.argv[1:]} is not a valid option")

print("""
arg 1        -- which command is run --
lessons      returns a list of lessons
timetable    returns when and where the lessons are
tasks        returns a list of all not yet done homework
colors       returns the colours for each lesson

arg 2        -- date to check (lessons/timetable) --
today        shows lessons for today [DEFAULT]
tomorrow     shows values from tomorrow
dd/mm/yyyy   exact date

arg 2        -- task status (tasks) --
todo         shows tasks that aren't done [DEFAULT]
done         shows tasks that are done
both         shows all tasks
""")
