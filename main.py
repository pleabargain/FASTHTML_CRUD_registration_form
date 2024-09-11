from fasthtml.common import *
from dataclasses import dataclass, field

app, rt = fast_app()

db = Database("registrations.db")

@dataclass
class Registration:
    id: int = field(default=None)
    first_name: str = ""
    last_name: str = ""
    country: str = ""
    nationality: str = ""
    company_name: str = ""
    company_type: str = ""
    department: str = ""
    industry: str = ""
    job_title: str = ""
    mobile: str = ""
    email: str = ""
    state: str = ""
    address: str = ""
    solutions: str = ""
    password: str = ""

registrations = db.create(Registration, pk="id")

def home_button():
    return A("Home", href="/", style="margin-right: 10px;")

def view_all_link():
    return A("View All Entries", href="/list")

def registration_form(registration=None):
    form_style = """
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 10px;
    max-width: 600px;
    margin: auto;
    """
    
    label_style = "text-align: right; padding-right: 10px;"
    input_style = "width: 100%; padding: 5px;"

    def field(name, id, value, type="text"):
        return (
            Div(f"{name}:", style=label_style),
            Input(id=id, value=value, type=type, placeholder=f"Enter {name.lower()}", style=input_style)
        )

    return Form(
        Div(
            field("First Name", "first_name", registration.first_name if registration else ""),
            field("Last Name", "last_name", registration.last_name if registration else ""),
            field("Country", "country", registration.country if registration else ""),
            field("Nationality", "nationality", registration.nationality if registration else ""),
            field("Company Name", "company_name", registration.company_name if registration else ""),
            field("Company Type", "company_type", registration.company_type if registration else ""),
            field("Department", "department", registration.department if registration else ""),
            field("Industry", "industry", registration.industry if registration else ""),
            field("Job Title", "job_title", registration.job_title if registration else ""),
            field("Mobile", "mobile", registration.mobile if registration else ""),
            field("Email", "email", registration.email if registration else ""),
            field("State", "state", registration.state if registration else ""),
            (Div("Address:", style=label_style),
             Textarea(id="address", placeholder="Enter address", 
                      value=registration.address if registration else "", 
                      style=input_style + "height: 60px;")),
            field("Solutions", "solutions", registration.solutions if registration else ""),
            field("Password", "password", "", type="password"),
            (Div(), Button("Submit", type="submit", style="margin-top: 10px; padding: 5px 15px;")),
            style=form_style
        ),
        method="post",
        action="/register"
    )

@rt("/")
def get():
    return Titled("Welcome to the Registration System",
        Div(home_button(), view_all_link(), style="margin-bottom: 20px;"),
        H2("Registration Form", style="text-align: center;"),
        registration_form(),
        Div(home_button(), view_all_link(), style="margin-top: 20px;")
    )

@rt("/list")
def get():
    all_registrations = registrations()  # This fetches all registrations
    return Titled("All Registrations",
        Div(home_button()),
        Ul(*[Li(f"{r.first_name} {r.last_name} - {r.email} ",
                A("Edit", href=f"/edit/{r.id}"),
                " | ",
                A("Delete", href=f"/delete/{r.id}"))
            for r in all_registrations]),
        Div(home_button())
    )



@rt("/register")
def post(registration: Registration):
    if not registration.email or not registration.password:
        return "Email and password are required."

    new_registration = registrations.insert(registration)

    return Titled("Registration Successful",
        Div(home_button(), view_all_link()),
        P(f"Thank you for registering, {new_registration.first_name}!"),
        Div(home_button(), view_all_link())
    )

@rt("/list")
def get():
    all_registrations = registrations.all()
    return Titled("All Registrations",
        Div(home_button()),
        Ul(*[Li(f"{r.first_name} {r.last_name} - {r.email} ",
                A("Edit", href=f"/edit/{r.id}"),
                " | ",
                A("Delete", href=f"/delete/{r.id}"))
            for r in all_registrations]),
        Div(home_button())
    )

@rt("/edit/{id}")
def get(id: int):
    registration = registrations[id]
    return Titled("Edit Registration",
        Div(home_button(), view_all_link()),
        registration_form(registration),
        Div(home_button(), view_all_link())
    )

@rt("/edit/{id}")
def post(id: int, registration: Registration):
    updated_registration = registrations.update(registration, id)
    return Titled("Update Successful",
        Div(home_button(), view_all_link()),
        P(f"Registration for {updated_registration.first_name} updated successfully!"),
        Div(home_button(), view_all_link())
    )

@rt("/delete/{id}")
def get(id: int):
    registration = registrations[id]
    return Titled("Confirm Deletion",
        Div(home_button(), view_all_link()),
        P(f"Are you sure you want to delete the registration for {registration.first_name} {registration.last_name}?"),
        Form(Button("Yes, Delete", type="submit"),
             method="post",
             action=f"/delete/{id}"),
        A("Cancel", href="/list"),
        Div(home_button(), view_all_link())
    )

@rt("/delete/{id}")
def post(id: int):
    registrations.delete(id)
    return Titled("Deletion Successful",
        Div(home_button(), view_all_link()),
        P("Registration deleted successfully!"),
        Div(home_button(), view_all_link())
    )

serve()