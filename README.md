# TUW_semester_planning_app
A shiny app to help students of the TU Vienna plan their semester

Is planning the upcoming semester somehow worse than actually attending the classes?
Do you study at TU Wien?
I've got just the thing. It's only *slightly* more convenient than planning your timetable in Excel — and I'm sure it's super buggy. :)
The idea is simple: **in theory**, this should help you figure out which classes you can take without timetable overlaps.

## How it works
First, go to **TISS**, add all the classes you're considering to your favorites, and export your calendar as an `.ical` file.
Then:
1. Put the `.ical` file into the `/files` folder. Name it cal.ical to be sure it works.
2. Open the project folder in Visual Studio.
3. Open the `semester_planning_app` folder.
4. Open `calendar_app.py` in Visual Studio and **press the Play ▶ button** to run the app.
5. Copy the localhost link that appears and paste it into your browser of choice.
That's it.

## Using the app
You should see a classic timetable with all your classes.
On the right, there's a scrollable list of the classes. You can delete individual classes from the timetable to see what your semester could look like without them.
**Important:** deleting a class only affects the current app session. If you want it back, just reload/restart the app — the original `.ical` file is never changed.

So you can basically play around with your timetable until you figure out which classes you actually want to take.
Once you've decided, just go back to TISS and enroll in those classes.

## A few disclaimers
This is very much a **work in progress**.
* It's probably buggy.
* It hasn't been tested extensively.
* The room information comes from the professors' reserved rooms, which is apparently only ~80% accurate anyway.
* So don't blindly trust it — **check your actual TISS timetable before relying on anything.**

But in THEORY, it should make semester planning a little less painful.

Hope it helps guys! :)
