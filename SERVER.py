from flask import *
import pandas as pd

SERVER = Flask(__name__)


# CREATING AN CLASS TO SAVE ALL THE METHODS THAT WE USE
class classcontrol:
    def __init__(self, teacher: str, students: str, Class: str) -> None:
        super().__init__()
        # MAKING ALL ATTRIBUTES GLOBAL
        self.students: str = students
        self.teacher: str = teacher
        self.Class: str = Class

        self.save()

    # SAVING THE GIVEN ATTRIBUTES IN A ".CSV" FILE
    def save(self) -> None:
        with open("Classes.csv", "a+") as file:
            file.write(f"{self.Class}, {self.teacher}, {self.students}\n")

    # SHOWING THE CLASSES FLOWED BY THE TEACHER NAME AND STUDENTS(in a list format) AS A TABLE
    def show(self=None) -> str:
        a: pd.DataFrame = pd.read_csv("Classes.csv")
        # CHANGING THE CLASS OF THE HTML TABLE SO BOOTSTRAP RECOGNIZES IT
        b: str = a.to_html(classes="table text-light")
        # REPLACING ALL THE EMPTY HEADERS WITH BLANK LINES
        b: str = b.replace("<th></th>", "", -1)

        # RETURNING THE TABLE IN A HTML FORMAT WITH BOOTSTRAP TO MAKE IT LOOK BETTER
        return f"""
        <head>
            <link rel="stylesheet" 
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" 
        integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" 
        crossorigin="anonymous">
            <link rel="stylesheet" href=
            "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/font/bootstrap-icons.css" />
            <title>Collage Management system</title>
            <style>width:500px;</style>    
        </head>
        <body class="bg-dark position-relative text-light">
            <nav class="container-fluid navbar navbar-dark" style="background-color: #404040;">
            <div class="container-fluid">
                <a class="navbar-brand bg-transparent" href="/"><h4 class="NavH4"><i class="bi bi-building"></i> Home</h4 class="NavH4"></a>

                <a class="navbar-brand bg-transparent" href="/AddClass"><h4 class="NavH4"><i class="bi bi-plus-square-fill"></i> Add Class</h4 class="NavH4"></a>

                <a class="navbar-brand bg-transparent" href="/DeleteClass"><h4 class="NavH4"><i class="bi bi-dash-square-fill"></i> Remove Class</h4 class="NavH4"></a>

                <a class="navbar-brand bg-transparent" href="/showclass"><h4 class="NavH4"><i class="bi bi-table"></i> Show Class</h4 class="NavH4"></a>

                <a class="navbar-brand bg-transparent" href="/EditClass"><h4 class="NavH4"><i class="bi bi-pen"></i> Edit Class</h4 class="NavH4"></a>
            </div>
        </nav>
        {b}
    </body>"""

    # REMOVING THE GIVEN CLASS, FINDING IT IN THE CSV FILE, REMOVING IT
    def DeleteClass(self=None, classname=str) -> None:
        a: pd.DataFrame = pd.read_csv("Classes.csv")
        # REMOVING THE GIVEN CLASS AND IT'S LINE THEN TURNING IT TO CSV TO SAVE IT AGAIN
        # ( THE RESULT WILL BE A CSV FILE WITHOUT THE LINE OF CLASS NAME GIVEN )
        b: str = (a.drop(labels=[f"{classname}"], axis="rows").to_csv()
                  .replace(",,,,,", "", -1).replace("\n", "", -1))

        with open("Classes.csv", "w+") as file:
            file.write(f"{b}")


# HOME PAGE
@SERVER.route("/")
def Home() -> str:
    return render_template("index.html")


# ADD CLASS PAGE ( HTML FILE )
@SERVER.route("/AddClass", methods=["GET", "POST"])
def AddClassPage() -> str:
    return render_template("AddClass.html")


# ADDING THE CLASS TO CSV FILE ( FUNCTIONALITY )
@SERVER.route("/addclass", methods=["GET", "POST"])
def AddClass() -> Response:
    teacher: str = request.form.get("Teacher")
    classname: str = request.form.get("ClassName")
    a: list[str] = request.form.get("Students").split("\n", -1)
    # TURNING THE "a" VARIABLE WHICH IS A LIST TO A STR FORMAT
    students: str = str(''.join(a).split('\r'))

    classcontrol(teacher, students, classname)

    return redirect("/AddClass")


# SHOWING THE CLASS ( HTML / FUNCTIONALITY )
@SERVER.route("/showclass", methods=["GET", "POST"])
def ShowClass() -> str:
    return classcontrol.show()


# DELETE CLASS PAGE ( HTML )
@SERVER.route("/DeleteClass", methods=['GET', 'POST'])
def DeleteClassPage() -> str:
    return render_template("DeleteClass.html")


# DELETING THE CLASS ( FUNCTIONALITY )
@SERVER.route("/deleteClass", methods=['GET', 'POST'])
def DeleteClass() -> Response:
    classname: str = request.form.get("ClassName")
    classcontrol.DeleteClass(classname=f"{classname}")

    return redirect("/DeleteClass")


# EDIT THE CLASS PAGE ( HTML ) [ ADD OR EDIT AN STUDENT'S GRADE ]
@SERVER.route("/EditClass", methods=["GET", "POST"])
def EditClassPage() -> str:
    return render_template("EditClass.html")


# EDITING THE CLASS ( FUNCTIONALITY ) [ ADD OR EDIT AN STUDENT'S GRADE ]
@SERVER.route("/editclass", methods=["GET", "POST"])
def editClass() -> Response:
    StudentName: str = request.form.get("StudentName")
    ClassName: str = request.form.get("ClassName")
    Score: int = int(request.form.get("Score"))

    a: pd.DataFrame = pd.read_csv("StudentScores.csv")
    b = a.get("Class")
    d = a.get("StudentName")
    # LOOPING THROUGH THE CLASSES AND STUDENT NAMES ...
    for i in range(len(b)):
        for k in range(len(d)):
            # ... SO WHEN WE DETECT A CLASS THAT IS IDENTICAL TO THE GIVEN CLASS IN THE HTML SIDE
            # ( OR AN STUDENT NAME IDENTICAL TO THE GIVEN STUDENT NAME IN THE HTML SIDE ) AND THEN REMOVING IT
            # (AND IT'S LINE) FROM THE DATAFRAME AND THEN CSV FILE
            if b[i] == ClassName and d[k] == StudentName:
                c: str = (a.drop(index=i).to_csv(index=False, columns=["Class", "StudentName", "Score"],
                                                 index_label=None, doublequote=False)
                          .replace("\n", "", -1))

                with open("StudentScores.csv", "w+") as file:
                    file.write(f"{c}")
                    file.write(f"{ClassName},{StudentName},{Score}")

            else:
                # IF THERE WASN'T ANY IDENTICAL STUDENT OR CLASS NAMES THEN WRITE THINGS AS NORMAL
                with open("StudentScores.csv", "a+") as file2:
                    file2.write(f"{ClassName},{StudentName},{Score} \n")
            break
        break

    return redirect("/EditClass")


if __name__ == "__main__":
    SERVER.run(debug=True, port=5000, host="127.3.8.2")
