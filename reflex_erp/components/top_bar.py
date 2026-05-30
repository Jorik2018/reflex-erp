import reflex as rx
from reflex_erp.states.app_state import AppState


def top_bar() -> rx.Component:
    """A responsive top navigation bar displaying session status and sidebar controls."""
    return rx.el.header(
        # Left elements
        rx.el.div(
            rx.el.button(
                rx.icon("menu", class_name="h-5 w-5 text-gray-700"),
                on_click=AppState.toggle_sidebar,
                class_name="p-2 rounded-lg hover:bg-gray-100 transition-all",
            ),
            rx.el.div(
                rx.el.h2(
                    rx.cond(
                        AppState.current_view == "voting",
                        "Cast Your Vote",
                        "Real-Time Election Analytics",
                    ),
                    class_name="text-lg font-semibold text-gray-900",
                ),
                rx.el.p(
                    rx.cond(
                        AppState.current_view == "voting",
                        "Select from current verified candidates below",
                        "Live performance charts & metrics",
                    ),
                    class_name="text-xs text-gray-500",
                ),
                class_name="hidden sm:block ml-2",
            ),
            class_name="flex items-center gap-3",
        ),
        # Right elements (User Status indicator)
        rx.el.div(
            rx.cond(
                AppState.user_voted,
                rx.el.div(
                    rx.icon(
                        "circle_check", class_name="h-4 w-4 text-emerald-600"
                    ),
                    rx.el.span(
                        "Vote Submitted",
                        class_name="text-xs font-semibold text-emerald-700",
                    ),
                    class_name="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-emerald-50 border border-emerald-100",
                ),
                rx.el.div(
                    rx.icon(
                        "circle-dot",
                        class_name="h-4 w-4 text-amber-500 animate-pulse",
                    ),
                    rx.el.span(
                        "Pending Vote",
                        class_name="text-xs font-semibold text-amber-700",
                    ),
                    class_name="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-amber-50 border border-amber-100",
                ),
            ),
            rx.image(
                src="https://api.dicebear.com/9.x/initials/svg?seed=AnonymousVoter",
                class_name="size-8 rounded-full border border-gray-200",
            ),
            class_name="flex items-center gap-4",
        ),
        class_name="flex h-16 items-center justify-between border-b border-gray-100 bg-white px-6 shrink-0",
    )