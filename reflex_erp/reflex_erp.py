"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from rxconfig import config
from reflex_erp.states.app_state import AppState
from reflex_erp.components.sidebar import sidebar
from reflex_erp.components.top_bar import top_bar
from reflex_erp.components.candidate_view import candidate_view
from reflex_erp.components.results_view import results_view
from reflex_erp.controllers.people_controller import fastapi_app

def drawer():
    return rx.drawer.root(
        rx.drawer.trigger(rx.button("Open Drawer")),
        rx.drawer.overlay(z_index="5"),
        rx.drawer.portal(
            rx.drawer.content(
                rx.flex(
                    rx.drawer.close(rx.box(rx.button("Close"))),
                    align_items="start",
                    direction="column",
                ),
                top="auto",
                right="auto",
                height="100%",
                width="20em",
                padding="2em",
                background_color="#FFF",
                # background_color=rx.color("green", 3)
            )
        ),
        direction="left",
    )
    
    
    # rx.drawer(
    #     rx.drawer_overlay(
    #         rx.drawer_content(
    #             rx.vstack(
    #                 rx.heading("Menúmm"),
    #                 #rx.button("Listar", on_click=State.load_items),
    #                 #rx.button("Crear"),
    #             )
    #         )
    #     )
    # )

def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.el.main(
        rx.el.div(
            sidebar(),
            rx.el.div(
                top_bar(),
                rx.el.div(
                    rx.match(
                        AppState.current_view,
                        ("voting", candidate_view()),
                        ("results", results_view()),
                        candidate_view(),  # default fallback
                    ),
                    # rx.text(
                    #     f"Get started by editing {AppState.current_view}",
                    #     rx.code(f"{config.app_name}/{config.app_name}.py"),
                    #     size="5",
                    # ),
                    class_name="flex-1 p-6 md:p-8 overflow-y-auto",
                ),
                class_name="flex-1 flex flex-col h-screen overflow-hidden",
            ),
            class_name="flex min-h-screen w-screen bg-gray-50/50",
        ),
        class_name="font-['Inter'] antialiased",
    )


app = rx.App(
    api_transformer=[fastapi_app],
    theme=rx.theme(appearance="light"),
    # head_components=[
    #     rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
    #     rx.el.link(
    #         rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""
    #     ),
    #     rx.el.link(
    #         href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
    #         rel="stylesheet",
    #     ),
    # ],
)
app.add_page(index, route="/")
app.add_page(rx.text("Hi" ), route="/hi")
# Create a Reflex app with the FastAPI app as the API transformer
