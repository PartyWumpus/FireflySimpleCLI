# FireflySimpleCLI
A simple (unofficial) CLI interface for the Firefly schools platform

Most of this tool was built using the info from the [unofficial API wiki](https://github.com/JoshHeng/FireflyAPI/wiki) by [JoshHeng](https://github.com/JoshHeng)

## Setup
0. Make sure python is installed on your system
1. Modify the `url` variable so it points to your school's website (something like https://school.fireflycloud.net)
1. Go to [https://school.fireflycloud.net/Login/api/gettoken?ffauth_device_id=SimpleFireflyCLI&ffauth_secret=&device_id=SimpleFireflyCLI&app_id=SimpleFireflyCLI](https://school.fireflycloud.net/Login/api/gettoken?ffauth_device_id=SimpleFireflyCLI&ffauth_secret=&device_id=SimpleFireflyCLI&app_id=SimpleFireflyCLI) on a browser where you're logged in to firefly. This will create your API secret and return a page that looks something like this:![image](https://user-images.githubusercontent.com/48649272/226177026-2d7a6a3b-1b54-471c-8ef5-996d27af189b.png)

1. Stay on that page and copy the secret field (something like `tsgT9UVHKlcIlbAPjqq5_Q8yx8wLlGGEBzojCTROLyv3Oz3ZXecW6Nvz3mWZkSB2I1`) into the `secret` variable
1. Then, copy the GUID into the `pupil_guid` variable.

At this point, it should just about work, but will need further tweaking to get all the features.
![image](https://user-images.githubusercontent.com/48649272/226179234-c010fc39-dac8-44be-94a7-7c7675dd0f1e.png)

## Further tweaking

+ Set `jsonfile` to a file location on your computer to enable caching, although it'll only be helpful if you're on a device that may not be connected to wifi, like a phone using Termux (my main usecase)
+ Set `time_names` to the times of each of your lessons, so they can be labelled instead of just using the time.
+ Set `lesson_colors` to some different colours for each of your lessons so you can more easily tell which lessons you have at a glance. The colours are set using ANSI escape codes, [this page by Haoyi](https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html#colors) should help explain how to use them.
+ Use the `maths_teachers` variable as an example on how to make it work if you have a single lesson with multiple teachers, and each teacher teaches a different part of the course.
+ Run `alias "timetable"="python3 path/to/timetable.py"` so you can just run `timetable` instead

Doing all of these will make it look much nicer, but none are mandatory:

![image](https://user-images.githubusercontent.com/48649272/226179257-836db9db-5dca-47c1-aabb-ef5babdecf80.png)


## Usage

There are 5 commands:
### `timetable.py lessons`
Tells you which lessons you have (parameters are `today`, `tomorrow` or the date as `dd/mm/yyyy`)

![image](https://user-images.githubusercontent.com/48649272/226179278-35d1c540-5456-4140-b88c-b37cdeba5697.png)
### `timetable.py timetable`
Tells you what rooms you need to go to (parameters are `today`, `tomorrow` or the date as `dd/mm/yyyy`)

![image](https://user-images.githubusercontent.com/48649272/226178898-11b8ba10-08db-4ee0-8cca-aec9e65b6be8.png)
### `timetable.py tasks`
Gives you a list of all your tasks (parameters are `todo`, `done` or `both`)

![image](https://user-images.githubusercontent.com/48649272/226179314-65a575f4-3880-436c-8754-1b542275c7e9.png)
### `timetable.py colors`
Lists off all the lessons you have given custom colours to

![image](https://user-images.githubusercontent.com/48649272/226179340-4769cf08-f73f-407d-b5c1-085b16260b21.png)
### `timetable.py help`
Gives a help prompt explaining the same information as is available here
