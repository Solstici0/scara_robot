"""
demo_umas_scara.py
    script for testing UMAS in scara
"""
import inspect
import logging

from scara.logger import logger
import scara


def detect_methods(robot: scara.Robot, skip: list = []):
    """
    Parameters
    ----------
    robot : Robot type
    skipt : list
            list with skipped methods

    Returns
    -------
    method_dict : dict
                dictionary with available methods
    """
    # automatically inspect all method of FlakeFeeder
    method_dict = {}
    for method_name, method in inspect.getmembers(robot, inspect.ismethod):
        # avoid _ methods
        if not method_name.startswith('_') and method is not None:
            # skip umas
            if method_name in skip:
                continue

            # include method in dict
            method_dict[method_name] = method
    return method_dict


# TODO: move method below to utils/automatic_inspect.py
def force_type(param: str, param_type: str):
    """
    force parameter to be the same type as the one defined
    in method's annotations

    Parameters
    ----------
    param : str
        string with param value
    param_type : str
        parameter type given by method annotation

    Returns
    -------
    param_w_type :
        return param with param_type type
    """
    if str(param_type) == "<class 'int'>":
        param_w_type = int(param)
    elif str(param_type) == "<class 'float'>":
        param_w_type = float(param)
    elif str(param_type) == "<class 'bool'>":
        param_w_type = bool(param)
    # string
    else:
        param_w_type = param
    return param_w_type


# TODO: move method below to utils/automatic_inspect.py
def ask_params_and_apply_method(methods, idx):
    """
    get method's signature and automatically ask parameters values.
    Then applies the method

    Parameters
    ----------
    method : robot's methods
            available methods to be applied
    idx : int
        method index
    Returns
    -------
    None
    """
    # get method from index
    method_name = list(methods.keys())[idx]
    method = methods[method_name]
    # ask for extra help
    h = input("print method docstring? [y/n]\n")
    if h == "y":
        help(method)
    # get method signature
    sig = inspect.signature(method)
    params = sig.parameters
    params_items_dict = dict(params.items())
    params_info = inspect.getfullargspec(method)
    logger.debug("parameters info for method %s \n %s", method, params_info)
    params_type = params_info.annotations
    logger.debug("parameters types for method %s \n %s", method, params_type)
    # define empy list for rewritting new parameters values
    new_params = []

    # check how many params (more than 0?)
    if len(params) > 0:
        for param in params:
            logger.debug("asking for parameter: %s (%s)", params[param],
                         params_type[param])
            # ask new parameter value
            new_param = input(f"New value for {param} ({params_type[param]})? "
                              "(press ENTER to use defautl value) \n")
            if (new_param == '' and
                    params_items_dict[param].default is not inspect._empty):
                new_param_w_type = params_items_dict[param].default
            else:
                new_param_w_type = force_type(new_param, params_type[param])
            new_params.append(new_param_w_type)
        # apply method with new parameters values
        method(*new_params)
    else:
        # 0 param case
        method()


def print_help_table(methods_dict: dict):
    """

    Parameters
    ----------
    methods_dict : dict
        dictionary with all available methods

    Returns
    -------
    None
    """
    h_str = ""
    for idx, method_name in enumerate(methods_dict.keys()):
        h_str += f"for method '{method_name}' --> type: {idx}. \n"
    print(h_str)

if __name__ == "__main__":
    # TODO: include option to create and start socket client
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="defines logger level",
                        type=int, choices=[10, 20, 30, 40, 50], default=10)
    # 10 -> DEBUG
    # 20 -> INFO
    # 30 -> WARNING
    # 40 -> ERROR
    # 50 -> CRITICAL
    parser.add_argument("-c", "--communication",
                        help="l-ocal or r-emote communication",
                        type=str, default="l", choices=["l", "r"])
    args = parser.parse_args()

    if args.communication == "r":
        pass
        # Server.start()

    logger.setLevel(args.verbose)
    nelen = scara.Robot()
    # skip umas or otyher functions
    skip = []
    # detect all Robot methods (except skiped ones)
    methods_dict = detect_methods(robot=nelen, skip=skip)

    # Infinite loop for sending instructions
    while True:
        input_command = input('\nType method index value.\n'
                            'Type "-h", "--help" or "help" for help. \nType'
                            '"-e", "--exit" or "exit" to exit program. \n')
        if input_command in ['-e', '--exit', 'exit']:
            break
        elif input_command in ['-h', '--help', 'help']:
            print_help_table(methods_dict=methods_dict)
        else:
            try:
                while int(input_command) >= len(methods_dict):
                    logger.error("input command index out of bounds")
                    #print("input command index out of bounds")
                    input_command = input('\nType method index value.\n'
                                        'Type "-h", "--help" or "help" for help. '
                                        '\nType "-e", "--exit" or "exit" to exit '
                                        'program. \n')
                input_command_int = int(input_command)
                ask_params_and_apply_method(methods_dict,
                                            input_command_int)
            except Exception as e:
                logger.error("%s", e)
                print("The error is: ",e)
