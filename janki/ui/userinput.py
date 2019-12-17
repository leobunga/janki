import readline

def dinput(string, default=None, choices=None, quitbutton='q'):
    """
    Get user input with possible default values and choices (POSIX only?)
    
    Will preprint the `default` string, if provided.
    Will print the `choices` in brackets after the `string`, if provided.
    Will additionally check, if input matches the `choices` or is empty, and prompt
    until a valid value is provided or the `quitbutton` is pressed.
    """

    if choices:
        choices = [choices] if not isinstance(choices, (list,tuple)) else choices
        if default and (default not in choices):
            raise ValueError(f'Default {default} not in choices.')
        if len(choices) == 1:
            default = choices[0]
            choices = None
    msg = string
    if choices:
        msg += f' ({"/".join(str(i) for i in choices)})'
    msg += ': '

    readline.set_startup_hook(lambda: readline.insert_text(default)) # https://stackoverflow.com/questions/2533120/show-default-value-for-editing-on-python-input-possible
    ret = input(msg)
    readline.set_startup_hook()

    if ret == quitbutton:
        return None
    if ret=='' or (choices and ret not in choices):
        print(f'Enter a valid value or press ({quitbutton}) to quit.')
        ret = dinput(string, default, choices, quitbutton)
    return ret
