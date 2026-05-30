import reflex as rx
from reflex_erp.states.app_state import AppState, Candidate


def candidate_card(c: Candidate) -> rx.Component:
    """Card representing an individual candidate."""
    is_voted = AppState.voted_candidate_id == c["id"]

    return rx.el.div(
        # Avatar and Party info
        rx.el.div(
            rx.image(
                src=c["avatar"],
                class_name="size-16 rounded-full bg-blue-50 border border-blue-100",
            ),
            rx.el.div(
                rx.el.h3(
                    c["name"], class_name="text-lg font-bold text-gray-900"
                ),
                rx.el.span(
                    c["party"],
                    class_name="inline-block text-xs font-semibold px-2 py-0.5 rounded bg-blue-50 text-blue-600 border border-blue-100 mt-1",
                ),
                class_name="flex-1",
            ),
            class_name="flex items-start gap-4",
        ),
        # Candidate description and bio
        rx.el.div(
            rx.el.h4(
                "Biography",
                class_name="text-xs font-bold text-gray-400 uppercase tracking-wider mb-1",
            ),
            rx.el.p(
                c["bio"], class_name="text-sm text-gray-600 leading-relaxed"
            ),
            class_name="mt-4",
        ),
        # Agenda / Key Policies
        rx.el.div(
            rx.el.h4(
                "Key Proposal",
                class_name="text-xs font-bold text-gray-400 uppercase tracking-wider mb-1",
            ),
            rx.el.p(
                c["agenda"],
                class_name="text-sm text-gray-600 leading-relaxed bg-gray-50 p-3 rounded-lg border border-gray-100",
            ),
            class_name="mt-3",
        ),
        # Action voting footer inside card
        rx.el.div(
            rx.cond(
                AppState.user_voted,
                rx.cond(
                    is_voted,
                    rx.el.div(
                        rx.icon("check", class_name="h-4 w-4 mr-2"),
                        "You voted for this candidate",
                        class_name="flex items-center justify-center w-full py-2.5 px-4 bg-emerald-50 text-emerald-700 rounded-xl font-semibold border border-emerald-200 text-sm",
                    ),
                    rx.el.div(
                        "Vote Registered",
                        class_name="text-center w-full py-2.5 px-4 bg-gray-50 text-gray-400 rounded-xl font-medium border border-gray-100 text-sm cursor-not-allowed",
                    ),
                ),
                rx.el.button(
                    rx.icon("square_check", class_name="h-4 w-4 mr-2"),
                    "Cast Ballot",
                    on_click=lambda: AppState.open_vote_dialog(c["id"]),
                    class_name="w-full flex items-center justify-center py-2.5 px-4 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-semibold shadow-sm transition-all hover:shadow text-sm",
                ),
            ),
            class_name="mt-6 pt-4 border-t border-gray-100",
        ),
        class_name=rx.cond(
            is_voted,
            "bg-white border-2 border-emerald-500 rounded-2xl p-6 shadow-sm flex flex-col justify-between transition-all",
            "bg-white border border-gray-150 rounded-2xl p-6 hover:border-gray-300 transition-all flex flex-col justify-between",
        ),
    )


def security_modal() -> rx.Component:
    """Verified Voter Validation Modal overlay with clear form & validation steps."""
    return rx.cond(
        AppState.show_security_modal,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    # Header banner
                    rx.el.div(
                        rx.icon(
                            "shield-alert",
                            class_name="h-12 w-12 text-blue-600 mb-2",
                        ),
                        rx.el.h3(
                            "Security Credentials Validation",
                            class_name="text-lg font-bold text-gray-900",
                        ),
                        rx.el.p(
                            "An authorized ballot token is required to ensure authentic cast verification.",
                            class_name="text-xs text-gray-500 text-center mt-1",
                        ),
                        class_name="flex flex-col items-center border-b border-gray-100 pb-4",
                    ),
                    # Instruction block
                    rx.el.div(
                        rx.el.span(
                            "SIMULATED TEST CREDENTIALS:",
                            class_name="text-xs font-bold text-amber-800 uppercase block mb-1",
                        ),
                        rx.el.p(
                            "Input any code with at least 6 characters (e.g. SECURE123) to satisfy cryptographical checksum.",
                            class_name="text-xs text-amber-700 leading-normal",
                        ),
                        class_name="bg-amber-50 border border-amber-150 p-3 rounded-lg my-4",
                    ),
                    # TextInput Area
                    rx.el.div(
                        rx.el.label(
                            "Enter Security Ballot Passcode",
                            class_name="text-xs font-bold text-gray-700 block mb-1",
                        ),
                        rx.el.input(
                            placeholder="e.g. VOTER-TOKEN-XYZ",
                            on_change=AppState.set_token_input.debounce(100),
                            class_name="w-full px-4 py-2 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm font-medium",
                        ),
                        class_name="mb-6",
                    ),
                    # Validation status dynamic message
                    rx.el.div(
                        rx.cond(
                            AppState.is_token_valid,
                            rx.el.div(
                                rx.icon(
                                    "circle_check",
                                    class_name="h-4 w-4 text-emerald-600",
                                ),
                                rx.el.span(
                                    "Format validated successfully",
                                    class_name="text-xs text-emerald-700 font-medium",
                                ),
                                class_name="flex items-center gap-2 px-3 py-2 bg-emerald-50 rounded-lg border border-emerald-100",
                            ),
                            rx.el.div(
                                rx.icon(
                                    "message_circle_x",
                                    class_name="h-4 w-4 text-red-500",
                                ),
                                rx.el.span(
                                    "Passcode is too short (min 6 characters required)",
                                    class_name="text-xs text-red-600 font-medium",
                                ),
                                class_name="flex items-center gap-2 px-3 py-2 bg-red-50 rounded-lg border border-red-100",
                            ),
                        ),
                        class_name="mb-6",
                    ),
                    # Form Controls footer
                    rx.el.div(
                        rx.el.button(
                            "Cancel",
                            on_click=AppState.close_vote_dialog,
                            class_name="px-4 py-2 rounded-xl text-sm font-semibold border border-gray-200 hover:bg-gray-50 text-gray-700 transition-all",
                        ),
                        rx.el.button(
                            "Submit Secure Vote",
                            on_click=AppState.submit_secure_vote,
                            disabled=~AppState.is_token_valid,
                            class_name=rx.cond(
                                AppState.is_token_valid,
                                "px-4 py-2 rounded-xl text-sm font-semibold bg-blue-600 hover:bg-blue-700 text-white shadow-sm transition-all",
                                "px-4 py-2 rounded-xl text-sm font-semibold bg-gray-100 text-gray-400 cursor-not-allowed border border-gray-200",
                            ),
                        ),
                        class_name="flex justify-end gap-3 pt-4 border-t border-gray-100",
                    ),
                    class_name="bg-white rounded-2xl p-6 max-w-md w-full shadow-xl border border-gray-200 mx-4",
                ),
                class_name="flex items-center justify-center min-h-screen",
            ),
            class_name="fixed inset-0 z-50 overflow-y-auto bg-gray-900/40 backdrop-blur-sm transition-opacity",
        ),
        None,
    )


def candidate_view() -> rx.Component:
    """The main interface for casting user votes."""
    return rx.el.div(
        # Page Title Description
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "General Election Polls",
                    class_name="text-2xl font-bold text-gray-900",
                ),
                rx.el.p(
                    "Review candidate platforms carefully and submit your final secure choice below.",
                    class_name="text-sm text-gray-500 mt-1",
                ),
                class_name="flex-1",
            ),
            class_name="mb-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4",
        ),
        # Grid of candidate cards
        rx.el.div(
            rx.foreach(AppState.candidates, candidate_card),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-6",
        ),
        security_modal(),
        class_name="animate-fade-in",
    )