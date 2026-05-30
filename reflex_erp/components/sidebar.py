import reflex as rx
from reflex_erp.states.app_state import AppState

def nav_item(label: str, icon_name: str, view_value: str) -> rx.Component:
    """Helper to render sidebar navigation items."""
    is_active = AppState.current_view == view_value

    return rx.el.button(
        rx.icon(
            icon_name,
            class_name=rx.cond(
                is_active, "h-5 w-5 text-blue-600", "h-5 w-5 text-gray-500"
            ),
        ),
        rx.el.span(label, class_name="font-medium text-sm"),
        on_click=lambda: AppState.select_view(view_value),
        class_name=rx.cond(
            is_active,
            "flex items-center gap-3 w-full px-4 py-3 rounded-xl bg-blue-50 text-blue-600 border border-blue-100 transition-all",
            "flex items-center gap-3 w-full px-4 py-3 rounded-xl text-gray-600 hover:bg-gray-50 hover:text-gray-900 border border-transparent transition-all",
        ),
    )


def sidebar() -> rx.Component:
    """A beautiful, modern navigation drawer / sidebar."""
    return rx.el.aside(
        # Top branding header
        rx.el.div(
            rx.el.div(
                rx.icon("box", class_name="h-6 w-6 text-blue-600"),
                rx.el.span(
                    "Votify Hub",
                    class_name="text-lg font-bold text-gray-900 tracking-tight",
                ),
                class_name="flex items-center gap-2",
            ),
            # Close button for responsive screen drawers
            rx.el.button(
                rx.icon("x", class_name="h-5 w-5 text-gray-500"),
                on_click=AppState.toggle_sidebar,
                class_name="md:hidden p-1 rounded-lg hover:bg-gray-100",
            ),
            class_name="flex h-16 items-center justify-between border-b border-gray-100 px-6",
        ),
        # Navigation Links
        rx.el.div(
            rx.el.nav(
                rx.el.div(
                    "General",
                    class_name="px-4 text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2",
                ),
                nav_item("Cast Vote", "vote", "voting"),
                nav_item("Live Results", "bar-chart-3", "results"),
                class_name="flex flex-col gap-1 px-4 py-6",
            ),
            class_name="flex-1 overflow-y-auto",
        ),
        # Bottom decorative/footer card inside sidebar
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "shield-check",
                        class_name="h-5 w-5 text-emerald-600 mb-2",
                    ),
                    rx.el.p(
                        "Secure Voting",
                        class_name="text-xs font-semibold text-gray-900",
                    ),
                    rx.el.p(
                        "Verified blockchain-secured session. Your identity is fully protected.",
                        class_name="text-xs text-gray-500 mt-1 leading-relaxed",
                    ),
                    class_name="bg-gray-50 rounded-xl p-4 border border-gray-100",
                ),
                class_name="p-4 border-t border-gray-100",
            )
        ),
        class_name=rx.cond(
            AppState.sidebar_open,
            "fixed inset-y-0 left-0 z-40 flex flex-col w-64 bg-white border-r border-gray-100 transform translate-x-0 transition-transform duration-300 ease-in-out md:static md:translate-x-0 h-screen shrink-0",
            "fixed inset-y-0 left-0 z-40 flex flex-col w-64 bg-white border-r border-gray-100 transform -translate-x-full transition-transform duration-300 ease-in-out md:static md:translate-x-0 h-screen shrink-0 md:w-0 md:overflow-hidden md:border-r-0",
        ),
    )