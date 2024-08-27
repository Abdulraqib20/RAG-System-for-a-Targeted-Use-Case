def printer(message, color='white'):
    """
    Prints the message in the specified color. Defaults to white if no color is specified.

    Args:
        message (str): The message to be printed.
        color (str, optional): The color to print the message in. Defaults to 'white'.

    Returns:
        None: Prints the colored message to the console.
    """

    # Define color codes
    color_codes = {
        'black': "\033[0;30m",
        'red': "\033[0;31m",
        'green': "\033[0;32m",
        'yellow': "\033[0;33m",
        'blue': "\033[0;34m",
        'magenta': "\033[0;35m",
        'cyan': "\033[0;36m",
        'white': "\033[0;37m",
        'reset': "\033[0m"  # Reset the color back to default
    }

    # Get the color code or default to white
    color_code = color_codes.get(color.lower(), color_codes['white'])
    
    # Construct the colored message
    colored_message = f"{color_code}{message}{color_codes['reset']}"

    # Print the colored message
    print(colored_message)
