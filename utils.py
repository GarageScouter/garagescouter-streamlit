import streamlit as st

def try_parse_int(value) -> int:
    """
    Try to parse the input value as an integer.

    Parameters:
        value (any): The value to attempt to parse as an integer.

    Returns:
        int or None: If successful, returns the parsed integer value. If parsing fails,
                     returns None.

    Example:
        >>> try_parse_int("123")
        123
        >>> try_parse_int("abc")
        None
    """
    try:
        return int(value)
    except:
        return None
    
def check_if_key_is_in_session_state(key: str):
    """
    Sanity check for making sure that the `key` provided is in StreamLit's session state.
    """
    if key not in st.session_state:
        st.session_state[key] = None