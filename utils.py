# Utility methods


def get_input():
    """
    Get input from the user.
    """
    user_input = input("> \b")
    return user_input.strip()


class any:
    """A class that represents any type."""

    def __eq__(self, _):
        return True


def is_any(value):
    """Check if a value is of type any."""
    return isinstance(value, any)


# SQL QUERY STRING GENERATORS #
def select_query_string(
    table_name: str,
    active_status: bool | any = any(),
    completed_status: bool | any = any(),
) -> str:
    """
    Generate a select query string for task selection.
    """

    if is_any(active_status) and is_any(completed_status):
        return f"SELECT * FROM {table_name}"
    
    elif not is_any(active_status) and is_any(completed_status):
        return f"SELECT * FROM {table_name} WHERE task_is_active = {1 if active_status else 0}"
    
    elif is_any(active_status) and not is_any(completed_status):
        return f"SELECT * FROM {table_name} WHERE task_is_completed = {1 if completed_status else 0}"
    
    else:
        return f"SELECT * FROM {table_name} WHERE task_is_active = {1 if active_status else 0} AND task_is_completed = {1 if completed_status else 0}"