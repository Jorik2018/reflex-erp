import reflex as rx
from reflex_erp.states.app_state import AppState


def stat_card(
    label: str, value_str: str, icon_name: str, bg_color: str, icon_color: str
) -> rx.Component:
    """Helper for rendering nice statistical dashboard blocks."""
    return rx.el.div(
        rx.el.div(
            rx.icon(icon_name, class_name=f"h-5 w-5 {icon_color}"),
            class_name=f"p-2 rounded-lg {bg_color}",
        ),
        rx.el.div(
            rx.el.p(
                label,
                class_name="text-xs font-semibold text-gray-400 uppercase tracking-wider",
            ),
            rx.el.h3(
                value_str, class_name="text-2xl font-bold text-gray-900 mt-0.5"
            ),
            class_name="flex-1",
        ),
        class_name="bg-white border border-gray-100 rounded-xl p-5 flex items-center gap-4",
    )


def candidate_progress_row(c: dict, total: int) -> rx.Component:
    """A beautiful horizontal status row for results statistics."""
    # Handle division by zero nicely in formatting
    pct = rx.cond(total > 0, (c["votes"] / total) * 100, 0.0)

    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.image(
                    src=c["avatar"],
                    class_name="size-10 rounded-full border border-gray-100 bg-gray-50",
                ),
                rx.el.div(
                    rx.el.h4(
                        c["name"],
                        class_name="text-sm font-semibold text-gray-900",
                    ),
                    rx.el.p(c["party"], class_name="text-xs text-gray-500"),
                ),
                class_name="flex items-center gap-3",
            ),
            rx.el.div(
                rx.el.span(
                    f"{c['votes']} votes",
                    class_name="text-sm font-bold text-gray-900",
                ),
                rx.el.span(
                    f" ({pct:.1f}%)", class_name="text-xs text-gray-500 ml-1"
                ),
                class_name="text-right",
            ),
            class_name="flex justify-between items-center",
        ),
        # Modern animated look progress bar
        rx.el.div(
            rx.el.div(
                class_name="h-full bg-blue-600 rounded-full transition-all duration-500",
                style={"width": f"{pct:.1f}%"},
            ),
            class_name="w-full h-2.5 bg-gray-100 rounded-full mt-3 overflow-hidden",
        ),
        class_name="p-4 border border-gray-100 rounded-xl bg-white hover:border-gray-200 transition-all",
    )


TOOLTIP_PROPS = {
    "content_style": {
        "background": "white",
        "borderColor": "#E8E8E8",
        "borderRadius": "0.75rem",
        "boxShadow": "0px 8px 16px rgba(0, 0, 0, 0.05)",
        "fontFamily": "sans-serif",
        "fontSize": "0.875rem",
    },
    "item_style": {
        "display": "flex",
        "paddingTop": "2px",
    },
    "label_style": {
        "color": "black",
        "fontWeight": "600",
    },
    "separator": "",
}


def chart_legend() -> rx.Component:
    """Custom HTML legend for the visual vote distribution."""
    return rx.el.div(
        rx.foreach(
            AppState.candidates,
            lambda c: rx.el.div(
                rx.el.span(
                    class_name="w-3 h-3 inline-block rounded-sm mr-2",
                    style={"backgroundColor": "#2B79D1"},
                ),
                rx.el.span(
                    c["name"],
                    class_name="text-xs font-semibold text-gray-700",
                ),
                class_name="flex items-center",
            ),
        ),
        class_name="flex flex-wrap gap-4 mt-4 bg-gray-50/50 p-3 rounded-xl border border-gray-100",
    )


def results_view() -> rx.Component:
    """The Analytics and results presentation dashboard with interactive metrics & charts."""
    return rx.el.div(
        # Summary stats section
        rx.el.div(
            stat_card(
                "Total Ballots Cast",
                AppState.total_votes.to_string(),
                "square_check",
                "bg-blue-50",
                "text-blue-600",
            ),
            stat_card(
                "Current Leader",
                AppState.leading_candidate,
                "award",
                "bg-emerald-50",
                "text-emerald-600",
            ),
            stat_card(
                "System Integrity",
                "99.99%",
                "shield-check",
                "bg-purple-50",
                "text-purple-600",
            ),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8",
        ),
        # Detail grid structure
        rx.el.div(
            # Left Column: Progress Rows list
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Live Distribution",
                        class_name="text-lg font-bold text-gray-900 mb-2",
                    ),
                    rx.el.p(
                        "Real-time distribution of verified anonymous voter tallies.",
                        class_name="text-xs text-gray-500 mb-6",
                    ),
                    rx.el.div(
                        rx.foreach(
                            AppState.candidates,
                            lambda c: candidate_progress_row(
                                c, AppState.total_votes
                            ),
                        ),
                        class_name="flex flex-col gap-4",
                    ),
                    class_name="bg-white border border-gray-150 rounded-2xl p-6",
                ),
                class_name="space-y-6",
            ),
            # Right Column: Visual Chart
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Votes Tally Chart",
                        class_name="text-lg font-bold text-gray-900 mb-2",
                    ),
                    rx.el.p(
                        "Visual representation of vote allocations across candidates.",
                        class_name="text-xs text-gray-500 mb-6",
                    ),
                    rx.el.div(
                        # rx.recharts.line_chart(
                        #     rx.recharts.line(
                        #         data_key="pv",
                        #     ),
                        #     rx.recharts.line(
                        #         data_key="uv",
                        #     ),
                        #     rx.recharts.x_axis(data_key="name"),
                        #     rx.recharts.y_axis(),
                        #     data=[
                        #         {"name": "Page A", "uv": 4000, "pv": 2400, "amt": 2400},
                        #         {"name": "Page B", "uv": 3000, "pv": 1398, "amt": 2210},
                        #         {"name": "Page C", "uv": 2000, "pv": 9800, "amt": 2290},
                        #         {"name": "Page D", "uv": 2780, "pv": 3908, "amt": 2000},
                        #         {"name": "Page E", "uv": 1890, "pv": 4800, "amt": 2181},
                        #         {"name": "Page F", "uv": 2390, "pv": 3800, "amt": 2500},
                        #         {"name": "Page G", "uv": 3490, "pv": 4300, "amt": 2100},
                        #     ],
                        #     width="100%",
                        #     height=300,
                        # ),
                        # rx.recharts.bar_chart(
                        #     rx.recharts.cartesian_grid(
                        #         horizontal=True,
                        #         vertical=False,
                        #         class_name="opacity-25",
                        #     ),
                        #     rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
                        #     rx.recharts.bar(
                        #         data_key="votes",
                        #         name="Votes",
                        #         fill="#2B79D1",
                        #         radius=[6, 6, 0, 0],
                        #         bar_size=35,
                        #     ),
                        #     rx.recharts.x_axis(
                        #         data_key="name",
                        #         height=45,
                        #         axis_line=False,
                        #         tick_size=10,
                        #         tick_line=False,
                        #         custom_attrs={
                        #             "fontSize": "11px",
                        #             "fontWeight": "600",
                        #         },
                        #         interval="preserveStartEnd",
                        #         type_="category",
                        #     ),
                        #     rx.recharts.y_axis(
                        #         data_key="votes",
                        #         custom_attrs={"fontSize": "11px"},
                        #         axis_line=False,
                        #         tick_line=False,
                        #         tick_size=10,
                        #     ),
                        #     data=AppState.candidates,
                        #     width="100%",
                        #     height=240,
                        #     margin={"left": -20, "right": 10, "top": 10},
                        #     class_name="[&_.recharts-tooltip-item-unit]:text-gray-600 [&_.recharts-tooltip-item-value]:!text-gray-900 [&_.recharts-tooltip-item-name]:text-gray-600 [&_.recharts-tooltip-wrapper]:z-[1]",
                        # ),
                        class_name="relative",
                    ),
                    chart_legend(),
                    class_name="bg-white border border-gray-150 rounded-2xl p-6",
                ),
                class_name="w-full",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start",
        ),
        class_name="animate-fade-in",
    )