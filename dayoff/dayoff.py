import reflex as rx

from rxconfig import config


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
                rx.button("Submit Leave Request", on_click=rx.redirect("/submit")),
                rx.button("View Request", on_click=rx.redirect("/view")),
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
app.add_page(index, route="/")
app.add_page(submit_form, route="/submit")
