import functools
import os
import platform
import socket
import subprocess
import traceback
from datetime import datetime, timedelta
from time import time
from uknockknock.function_models import FunctionModel

DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
default_model: FunctionModel = FunctionModel(
                date_format=DEFAULT_DATE_FORMAT,
                final_text_message=None
            )

def desktop_sender(title: str = "knockknock", model = default_model):   
    def show_notification(text: str, title: str):        
        if platform.system() == "Darwin":
            subprocess.run(
                [
                    "sh",
                    "-c",
                    'osascript -e \'display notification "%s" with title "%s"\''
                    % (text, title),
                ]
            )
        elif platform.system() == "Linux":
            subprocess.run(["notify-send", title, text])
        elif platform.system() == "Windows":
            try:
                # This library needs a windows system
                # The setup file fix this on windows.
                from win10toast import ToastNotifier
            except ImportError as err:
                print(err)
                print(
                    "Error: to use Windows Desktop Notifications, you need to install "
                    + "`win11toast` first. Please run `pip install win11toast==0.34`."
                )

            toaster = ToastNotifier()
            toaster.show_toast(title, text, icon_path=None, duration=5)

    def decorator_sender(func):
        @functools.wraps(func)
        def wrapper_sender(*args, **kwargs):            
            DATE_FORMAT = model.date_format
            start_time = datetime.now()
            host_name = socket.gethostname()
            func_name = func.__name__
            # Handling distributed training edge case.
            # In PyTorch, the launch of `torch.distributed.launch` sets up a RANK environment variable for each process.  # noqa
            # This can be used to detect the master process.
            # See https://github.com/pytorch/pytorch/blob/master/torch/distributed/launch.py#L211  # noqa
            # Except for errors, only the master process will send notifications.
            if "RANK" in os.environ:
                master_process = int(os.environ["RANK"]) == 0
                host_name += " - RANK: %s" % os.environ["RANK"]
            else:
                master_process = True

            if master_process:
                text = (
                    "Your function has started \n"
                    f"Machine name: {host_name}\n"
                    f"Main call: {func_name}\n"
                    f"Starting date: {start_time.strftime(DATE_FORMAT)}\n"
                )
                print(text, title)

            try:
                value = func(*args, **kwargs)
                if master_process:
                    end_time = datetime.now()                   
                    elapsed_time: timedelta = end_time - start_time
                    if not model.final_text_message:
                        text = (
                        "Your function is complete 🎉\n"
                        f"Machine name: {host_name}\n"
                        f"Main call: {func_name}\n"
                        f"Starting date: {start_time.strftime(DATE_FORMAT)}\n"
                        f"End date: {end_time.strftime(DATE_FORMAT)}\n"
                        f"Function duration: {elapsed_time.total_seconds():.1f} seconds\n\n"                    
                    )
                    else:
                        text = model.final_text_message
                    try:
                        str_value = str(value)
                        text + f" Main call returned value: {str_value}"
                    except Exception:
                        text + (
                            " Main call returned value: ERROR - "
                            "Couldn't str the returned value."
                        )
                    show_notification(text, title)

                return value
            except Exception as ex:
                end_time = datetime.now()
                elapsed_time: timedelta = end_time - start_time                
                text = (
                    "Your function has crashed ☠️\n"
                    f"Machine name: {host_name}\n"
                    f"Main call: {func_name}\n"
                    f"Starting date: {start_time.strftime(DATE_FORMAT)}\n"
                    f"Crash date: {end_time.strftime(DATE_FORMAT)}\n"
                    f"Duration: {elapsed_time.total_seconds():.1f} seconds\n\n"
                    f"Here's the error: {ex}\n\n"
                    f"Traceback: {traceback.format_exc()}\n"
                )
                print(text, title)
                show_notification(text, title)
                raise ex

        return wrapper_sender

    return decorator_sender
