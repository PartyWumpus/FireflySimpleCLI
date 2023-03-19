# FireflySimpleCLI
A simple (unoffical) CLI interface for the Firefly schools platform

Most of this tool was built using the info from the [unoffical API wiki](https://github.com/JoshHeng/FireflyAPI/wiki) by [JoshHeng](https://github.com/JoshHeng)

## To get it working, you'll need to:
1. Modify the `url` variable so it points to your school's website (something like https://school.fireflycloud.net)
1. Go to [https://school.fireflycloud.net/Login/api/gettoken?ffauth_device_id=SimpleFireflyCLI&ffauth_secret=&device_id=SimpleFireflyCLI&app_id=SimpleFireflyCLI](https://school.fireflycloud.net/Login/api/gettoken?ffauth_device_id=SimpleFireflyCLI&ffauth_secret=&device_id=SimpleFireflyCLI&app_id=SimpleFireflyCLI) on a browser where you're logged in to firefly. This will create your API secret and return a page that looks something like this:![image](https://user-images.githubusercontent.com/48649272/226177026-2d7a6a3b-1b54-471c-8ef5-996d27af189b.png)

1. Stay on that page and copy the secret field (something like `tsgT9UVHKlcIlbAPjqq5_Q8yx8wLlGGEBzojCTROLyv3Oz3ZXecW6Nvz3mWZkSB2I1`) into the `secret` variable
1. Then, copy the GUID into the `pupil_guid` variable.

At this point, it should just about work, but will need further tweaking to get all the features.

1. a
1. a
