import reflex as rx

config = rx.Config(
    app_name="reflex_erp",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)