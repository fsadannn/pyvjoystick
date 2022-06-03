from . import constants


def check_err(err):
    if err != constants.VIGEM_ERRORS.VIGEM_ERROR_NONE:
        raise Exception(constants.VIGEM_ERRORS(err).name)


def dummy_callback(client, target, large_motor, small_motor, led_number, user_data):
    """
    Pattern for callback functions to be registered as notifications

    :param client: vigem bus ID
    :param target: vigem device ID
    :param large_motor: integer in [0, 255] representing the state of the large motor
    :param small_motor: integer in [0, 255] representing the state of the small motor
    :param led_number: integer in [0, 255] representing the state of the LED ring
    :param user_data: placeholder, do not use
    """
    pass
