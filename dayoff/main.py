import reflex as rx
import bcrypt

from rxconfig import config
from models import init_db, SessionLocal, User, Role
from utils import chek_password, hash_password

init_db()

class State(rx.State):
    """The app state."""
    name: str
    l_name: str
    start_date: str
    end_date: str
    reson: str = ""

    def submit(self):
        print(f"Leave request from {self.name}{self.l_name} ({self.start_date} to {self.end_date}): {self.reson}.")

        self.name = ""
        self.l_name = ""
        self.start_date = ""
        self.end_date = ""
        self.reson = ""

class SignUpState(rx.State):
    username: str = ""
    first_name: str = ""
    last_name: str = ""
    password: str = ""
    role: str = "employee"

    def submit(self):
        session = SessionLocal()

        existing = session.query(User).filter(User.username == self.username).first()
        if existing:
            print("ERROR.")
            session.close()
            return rx.toast.error("Error", description = " you cant sign up", duration = 4000, position = "bot-right")

        hashed = hash_password(self.password)

        user = User(
            username = self.username,
            first_name = self.first_name,
            last_name = self.last_name,
            role = Role(self.role),
            password = hashed,
        )
        session.add(user)
        session.commit()
        session.close()

        

        print("Done!!")

        self.username = ""
        self.first_name = ""
        self.last_name = ""
        self.role = "employee"
        
        return rx.toast.success("Successful", description = " now log in", duration = 4000, position = "bottom-right")

class LoginSate(rx.State):
    username: str = ""
    password: str = ""

    n = False
    def notif():
        return rx.toast.success("Login successful", position = "top-center")

    def login(self):
        session = SessionLocal()
        user = session.query(User).filter_by(username=self.username).first()

        if user is None:
            session.close()
            return rx.toast.error("User not fonud!!", position = "top-center")

        if not chek_password(self.password, user.password):
            session.close()
            return rx.toast.error("Incorrect password!!", position = "top-center")

        if self.n is True:
            session.close()
            return rx.toast.success("Login successful", position = "top-center")
        session.close()
        return rx.redirect("/")

#rx.toast.success( title = "Login successful", status = "success", position = "top")


def submit_form() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.heading("Submit a Leave Request.", size="7"),
        rx.text("Fill out the form."),

        rx.vstack(
            rx.input(
                placeholder="First Name:",
                value = State.name,
                on_change = State.set_name,
            ),

            rx.input(
                placeholder="Last Name:",
                value = State.l_name,
                on_change = State.set_l_name,
            ),

            rx.input(
                placeholder = "Start Date:", 
                value = State.start_date,
                on_change = State.set_start_date,
            ),

            rx.input(
                placeholder = "End Date:", 
                value = State.end_date,
                on_change = State.set_end_date,
            ),

            rx.text_area(
                placeholder = "Reason for leave (optional):",
                value = State.reson,
                on_change = State.set_reson,
            ),


        ),

        spacing = "4",
        padding = "5",
    )

def singup_form() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Sign Up:", size = "7"),
            rx.text("Fill out the form."),
            rx.input(
                placeholder = "Username:", 
                on_change = SignUpState.set_username
            ),

            rx.input(
                placeholder = "First Name:", 
                on_change = SignUpState.set_first_name
            ),

            rx.input(
                placeholder = "Last Name:",
                on_change = SignUpState.set_last_name
            ),

            rx.input(
                placeholder = "Password:", 
                on_change = SignUpState.set_password
            ),

            rx.select(["admin", "employee"], on_change = SignUpState.set_role, value=SignUpState.role),
            rx.button("Submit", on_click = SignUpState.submit),
            rx.button("Done", on_click = rx.redirect("/")),
            spacing = "4",
            width = "300px"
        ),
        padding = "5rem"
    )

def login_form():
    return rx.center(
        rx.vstack(
            rx.heading("Enter"),
            rx.input(placeholder = "username:", on_change = LoginSate.set_username),
            rx.input(placeholder = "password:", type = "password", on_change = LoginSate.set_password),
            rx.button("Login", on_click = LoginSate.login), 
            spacing = "4",
            width= "300px"  
        ),
        padding = "5rem"
    )

def profile() -> rx.Component:
    

def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Welcome to DayOff!", size="9"),
            rx.text(
                "Get started by submitting and tracking employee leave requests effortlessly. ",
                #rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
                align = "center",
            ),
            rx.hstack(
                rx.button("Log in", on_click = rx.redirect("/login")),
                rx.button("Sign in", on_click= rx.redirect("/signup")),
                #rx.button("Submit Leave Request", on_click=rx.redirect("/submit")),
                #rx.button("View Request", on_click=rx.redirect("/view")),
                spacing = "4",
            ),
            spacing = "5",
            justify = "center",
            min_height = "85vh",
            
        ),
        rx.box(
            rx.link(
                rx.button("Check!"),
                href="https://github.com/alawaki/dayoff.git",
                is_external=True,
            ),
            position="absolute",
            bottom="1em",
            right="1em",
        ),
    )

app = rx.App()
app.add_page(singup_form, route="/signup")
app.add_page(login_form, route = "/login")
app.add_page(index, route="/")
add.app_page(profile, route = "/profile")
app.add_page(submit_form, route="/submit")
app.add_page(view_req, route = "/view")
