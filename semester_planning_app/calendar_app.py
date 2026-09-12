
# semester management 4 TU Vienna

import random


COLORS = [
    "#FF6B6B", "#4ECDC4", "#FFD93D",
    "#6C5CE7", "#00B894", "#E17055",
    "#0984E3", "#FD79A8", "#FDCB6E"
]

class Course():
    def __init__(self, summary):
        nr, name = summary.split(" ", 1)
        self.nr = nr
        self.name = name
        self.lectures = []
        self.color = random.choice(COLORS)
        
    def add_lecture(self,lecture):
        self.lectures.append(lecture)

    def display(self):
        print(self.nr + " "+ self.name)
        print(" "*5+ "consisting of "+str(len(self.lectures))+" individual lectures ")
        
class Lecture():
    def __init__(self, location, dstart, dend):
        self.loc = location
        self.start = dstart
        self.end = dend

class Semester():
    def __init__(self, winter_sumer, year):
        self.winter_summer = winter_sumer
        self.year = year
        self.courses = []
    def add_course(self, course):
        self.courses.append(course)
    def print(self):
        return self.winter_summer+str(self.year)[-2:]


def get_semester(dt):

    m = dt.month
    y = dt.year

    if 9 <= m <= 12:
        return ("winter", y)

    elif 1 <= m <= 2:
        return ("winter", y-1)

    elif 3 <= m <= 7:
        return ("summer", y)

    else:
        return None   # August ignored



course_list = []
semester_list = []


from ics import Calendar, Event
from datetime import datetime

with open("files/cal.ics", 'r') as file:
    ics_text = file.read()

c = Calendar(ics_text)

for event in c.events:

    # skip holidays
    if "holiday" in event.name.lower() or "ferien" in event.name.lower():
        continue

    sem = get_semester(event.begin)

    if sem is None:
        continue

    sem_type, sem_year = sem

    # find or create semester
    for semester in semester_list:
        if semester.winter_summer == sem_type and semester.year == sem_year:
            break
    else:
        semester = Semester(sem_type, sem_year)
        semester_list.append(semester)

    # now existing course logic INSIDE semester
    for course in semester.courses:
        if event.name[:7] == course.nr:
            lec = Lecture(event.location, event.begin, event.end)
            course.add_lecture(lec)
            break
    else:
        new_course = Course(event.name)
        lec = Lecture(event.location, event.begin, event.end)
        new_course.add_lecture(lec)
        new_course.nr = event.name[:7]
        semester.add_course(new_course)


# print("finished read in")
# for course in course_list:
#     course.display()
# for semester in semester_list:
#     semester.print()


# display all found events in an interactive window
# button to delete previous semester and next semester
# display all classes in a list on the right of the interactive calendar
# give each class a delete option via button 

import plotly_express as px 
from dash import Dash, html, Output, Input, ALL, callback_context, dcc
import dash_fullcalendar as dfc

# --------------------------
# Convert Semesters → Events
# --------------------------

def get_events():
    events = []
    for sem in semester_list:
        for course in sem.courses:
            for lec in course.lectures:

                events.append({
                    "title": course.name,
                    "start": lec.start.isoformat(),
                    "end": lec.end.isoformat(),
                    "backgroundColor": course.color,
                    "borderColor": course.color
                })

    return events



def make_course_boxes():
    boxes = []
    for i, sem in enumerate(semester_list):
        for j, course in enumerate(sem.courses):

            # Only show courses with at least 1 lecture
            if len(course.lectures) == 0:
                continue

            box = html.Div([
                html.Div(course.nr, style={"fontWeight": "bold"}),
                html.Div(course.name),
                html.Div(f"{sem.winter_summer.capitalize()} Semester"),
                html.Div(f"{len(course.lectures)} Lectures"),

                # Delete button for this course
                html.Button(
                    "🗑 Delete Lectures",
                    id={"type": "course-delete", "semester": i, "course": j},
                    n_clicks=0,
                    style={"marginTop": "8px", "padding": "4px 8px"}
                )
            ],
            style={
                "backgroundColor": course.color,
                "padding": "10px",
                "borderRadius": "10px",
                "marginBottom": "10px",
                "color": "white"
            })

            boxes.append(box)
    return boxes

# --------------------------
# App Layout
# --------------------------

app = Dash(__name__)

app.layout = html.Div([

    # Calendar + Download container
    html.Div([

        # Calendar
        dfc.FullCalendar(
            id='calendar',
            initialView='timeGridWeek',
            editable=True,
            selectable=True,
            events=get_events()
        ),

        # Download button (bottom left)
        html.Div([
            html.Button(
                "⬇ Download Updated iCal",
                id="download-ical-btn",
                n_clicks=0,
                style={
                    "padding": "8px 14px",
                    "borderRadius": "8px",
                    "border": "1px solid lightgrey",
                    "cursor": "pointer"
                }
            ),
            dcc.Download(id="download-ical-file")
        ],
        style={
            "marginTop": "10px"
        })

    ], style={
        "flex": "3",
        "display": "flex",
        "flexDirection": "column",
        "height": "600px"
    }),

    # Right panel
    html.Div(
        id="course-panel",
        children=make_course_boxes(),
        style={
            "flex": "1",
            "padding": "10px",
            "borderLeft": "1px solid lightgrey",
            "overflowY": "scroll"
        }
    )

], style={
    "display": "flex",
    "height": "650px"
})

# --------------------------
# Delete Course Lectures Callback
# --------------------------

@app.callback(
    Output("calendar", "events"),
    Output("course-panel", "children"),
    Input({"type": "course-delete", "semester": ALL, "course": ALL}, "n_clicks"),
    prevent_initial_call=True
)
def delete_course_lectures(n_clicks_list):
    ctx = callback_context
    if not ctx.triggered:
        return get_events(), make_course_boxes()

    triggered_id = ctx.triggered_id
    if not triggered_id:
        return get_events(), make_course_boxes()

    sem_idx = triggered_id.get("semester")
    course_idx = triggered_id.get("course")

    if sem_idx is not None and course_idx is not None:
        if 0 <= sem_idx < len(semester_list):
            if 0 <= course_idx < len(semester_list[sem_idx].courses):
                # delete lectures
                semester_list[sem_idx].courses[course_idx].lectures = []

    return get_events(), make_course_boxes()


@app.callback(
    Output("download-ical-file", "data"),
    Input("download-ical-btn", "n_clicks"),
    prevent_initial_call=True
)
def download_ical(n_clicks):

    cal = Calendar()

    for sem in semester_list:
        for course in sem.courses:
            for lec in course.lectures:

                event = Event()
                event.name = course.name
                event.begin = lec.start
                event.end = lec.end
                event.location = lec.loc

                cal.events.add(event)

    ical_string = str(cal)

    return dict(
        content=ical_string,
        filename="updated_schedule.ics"
    )

# --------------------------
# Run App
# --------------------------

if __name__ == '__main__':
    app.run(debug=True)
