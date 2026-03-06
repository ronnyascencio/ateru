import os

if os.getenv("ATERU_PIPELINE"):
    import ateru.integrations.nuke.menu
