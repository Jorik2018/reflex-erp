import os
import reflex as rx

config = rx.Config(
    app_name="reflex_erp",
    show_built_with_reflex=False,

    api_url=os.getenv("API_URL", "http://localhost:3000"),
    deploy_url=os.getenv("DEPLOY_URL", "http://localhost:3000"),

    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)