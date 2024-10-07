import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import filedialog
from PIL import Image, ImageTk
import time
from io import BytesIO
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grpc
from Server import allert_server_pb2,allert_server_pb2_grpc
import base64
root = tk.Tk()
root.title("Client-Side Simulator")
root.geometry("1600x800")
root.resizable(True, True)

label_text_vars = {}
actions = ["Sharpen Image", "Count Elements", "Unusual Events", "Accident", "Area Is Empty", "Border Control"]
buttons = []
show_results_buttons = {}
start_times = {}
label_states = {}
toggle = True

def clear_manual_results():
    for widget in lower_left_frame.winfo_children():
        widget.destroy()
    for widget in upper_left_frame.winfo_children():
            widget.destroy()

def display_one_result(result,action_name,destroy=True):
    if destroy:
        for widget in lower_left_frame.winfo_children():
            widget.destroy()
        for widget in upper_left_frame.winfo_children():
            widget.destroy()
    if isinstance(result, str) and result == "None":
                pass
    elif isinstance(result, list):
        result_list = "5 Last Unusual Events:\n " + ", ".join(result[-5:])
        result_label = tk.Label(upper_left_frame, text=result_list, font=('Helvetica', 12), bg="white", fg="black")
        result_label.pack(side='top', fill="x", padx=1)
    
    elif isinstance(result, bool):
        result_text = action_name+": True" if result else action_name+": False"
        result_label = tk.Label(upper_left_frame, text=result_text, font=('Helvetica', 12), bg="white", fg="black")
        result_label.pack(side='top', fill="x", padx=1)
    elif isinstance(result, bytes):
        image_stream = BytesIO(result)
        image = Image.open(image_stream)
        image = image.resize((350, 200), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(upper_left_frame, image=photo)
        image_label.image = photo
        image_label.pack(side='top')
    else:
        if isinstance(result, str):
            result_parts=result.split(" ")
            if result_parts[0]=="oddEvent:":
                result_list = "5 Last Unusual Events:\n " + ", ".join(list(result_parts[1])[-5:])
                result_label = tk.Label(upper_left_frame, text=result_list, font=('Helvetica', 12), bg="white", fg="black")
                result_label.pack(side='top', fill="x", padx=1) 
            elif result_parts[0]=="image":
                image_stream = BytesIO(result_parts[1])
                image = Image.open(image_stream)
                image = image.resize((350, 200), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                image_label = tk.Label(upper_left_frame, image=photo)
                image_label.image = photo
                image_label.pack(side='top')
        else:
            result_label = tk.Label(upper_left_frame, text=action_name+": "+str(result), font=('Helvetica', 12), bg="white", fg="black")
            result_label.pack(side='top', fill="x", padx=1)


def display_auto_results(results):
    for widget in upper_left_frame.winfo_children():
        widget.destroy()

    for result in results:
        display_one_result(result,destroy=False)

def display_manual_results(result):
    result_label = tk.Label(lower_left_frame, text=result, font=('Helvetica', 12), bg="black", fg="white")
    result_label.pack(side='top', fill="x", padx=1)

def periodic_function():
    clear_manual_results()
    with grpc.insecure_channel('localhost:50051') as channel:
            stub = allert_server_pb2_grpc.AlertServiceStub(channel)
            response=stub.GetOnResults(allert_server_pb2.GetOnResultsRequest())
            if response.HasField('overall_image_oneof') and response.overall_image!=b'':
                display_one_result(response.overall_image, "OverAll Display",destroy=False)
            elif response.HasField('image_oneof') and response.image!=b'':
                display_one_result(response.image,'Sharpen Image',destroy=False)
            if response.HasField('count_oneof'):
                display_one_result(response.count,"Amount of elements that were found",destroy=False)            
            if response.HasField('is_empty_oneof'):
                display_one_result(response.is_empty,'Area Is Empty',destroy=False)
            if response.HasField('is_cross_oneof'):
                display_one_result(response.is_cross,'Border Control',destroy=False)
            if response.HasField('accident_oneof'):
                display_one_result(response.accident,'Accident',destroy=False)
            if len(response.odd_event)>0:
                display_one_result(response.odd_event,'Unusual Events',destroy=False)
            
    root.after(4500, periodic_function)

def get_cross_input():
    input_dialog = simpledialog.askstring("Input", "Enter x1, y1, x2, y2 values separated by commas (e.g., 10,20,30,40):")
    input_values = input_dialog.split(",")
    if len(input_values) != 4:
        messagebox.showerror("Error", "Please enter all 4 values separated by commas.")
        return None
    try:
        x1, y1, x2, y2 = map(int, input_values)
    except ValueError:
        messagebox.showerror("Error", "Please enter valid integer values.")
        return None


    return x1, y1, x2, y2

def show_results(action_num):
    action_map = {1: "Sharpen Image",2:"Count Elements", 3: "Unusual Events", 4: "Accident", 5: "Area Is Empty", 6:"Border Control"}
    action_name = action_map.get(action_num, "Unknown Action")
    result = f"Sample result for action: {action_name}"
    with grpc.insecure_channel('localhost:50051') as channel:
            stub = allert_server_pb2_grpc.AlertServiceStub(channel)

            # Customize your request based on the action
            if action_name == "Sharpen Image":
                # Example for sending an image
                
                response = stub.GetSendImageResult(allert_server_pb2.GetSendImageResultRequest())
                display_one_result(response.image,"Sharpen Image")

            elif action_name == "Count  Elements":
                # Example for counting objects
                response = stub.GetCountResult(allert_server_pb2.GetCountResultRequest())
                display_one_result(response.count,"Amount of elements that were found")

            elif action_name == "Unusual Events":
                response = stub.GetOddEventResult(allert_server_pb2.GetOddEventResultRequest())
                display_one_result(response.odd_event,"Unusual Events")

            elif action_name == "Accident":
                response = stub.GetAccidentResult(allert_server_pb2.GetAccidentResultRequest())
                display_one_result(response.accident,"Accident")

            elif action_name == "Area Is Empty":
                response = stub.GetIsEmptyResult(allert_server_pb2.GetIsEmptyResultRequest())
                display_one_result(response.is_empty,"Area Is Empty")

            elif action_name == "Border Control":
                response = stub.GetIsCrossResult(allert_server_pb2.GetIsCrossResultRequest())
                display_one_result(response.is_cross,"Border Control")
    clear_all_button.pack(side='bottom', fill='x')

    # display_manual_results(f"Action: {actions[action_num - 1]}, Result: {result}")

def get_user_input():
    input_dialog = simpledialog.askstring("Input", "Enter x1, y1, x2, y2 values separated by commas (e.g., 10,20,30,40):")
    input_values = input_dialog.split(",")
    if len(input_values) != 4:
        messagebox.showerror("Error", "Please enter all 4 values separated by commas.")
        return None
    try:
        x1, y1, x2, y2 = map(int, input_values)
        return x1, y1, x2, y2
    except ValueError:
        messagebox.showerror("Error", "Please enter valid integer values.")
        return None


def toggle_state(label_num):
    current_state = label_states.get(label_num, False)
    new_state = not current_state
    label_states[label_num] = new_state
    button_text = "ON" if new_state else "OFF"
    buttons[label_num - 1].config(text=button_text)
    action_map = {1: "Sharpen Image",2:"Count Elements", 3: "Unusual Events", 4: "Accident", 5: "Area Is Empty", 6:"Border Control"}
    action_name = action_map[label_num]
    if new_state:
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = allert_server_pb2_grpc.AlertServiceStub(channel)
            if action_name == "Sharpen Image":
                # Example for sending an image
                
                response = stub.SendImageAlertOn(allert_server_pb2.SendImageAlertRequest())
            elif action_name == "Count Elements":
                # Example for counting objects
                x1, y1, x2, y2 = get_user_input()
                response = stub.CountAlertOn(allert_server_pb2.CountAlertRequest(
                    coordinate1_x=x1,
                    coordinate1_y=y1,
                    coordinate2_x=x2,
                    coordinate2_y=y2
                ))
            elif action_name == "Unusual Events":
                response = stub.OddEventAlertOn(allert_server_pb2.OddEventAlertRequest())

            elif action_name == "Accident":
                response = stub.AccidentAlertOn(allert_server_pb2.AccidentAlertRequest())

            elif action_name == "Area Is Empty":
                response = stub.IsEmptyAlertOn(allert_server_pb2.IsEmptyAlertRequest())   
                # if x1 is not None and y1 is not None and x2 is not None and y2 is not None:
                    # Process the input values as needed
            elif action_name == "Border Control":
                cross_input = get_cross_input()
                if cross_input:
                    x1, y1, x2, y2 = cross_input
                    response = stub.IsCrossAlertOn(allert_server_pb2.IsCrossAlertRequest(
                        coordinate1_x=x1,
                        coordinate1_y=y1,
                        coordinate2_x=x2,
                        coordinate2_y=y2,
                    ))

                    # Process the cross input values and image as needed
            start_times[label_num] = time.time()
            show_results_buttons[label_num].config(command=lambda num=label_num: show_results_or_retry(num))
            show_results_buttons[label_num].pack()
    else:
        show_results_buttons[label_num].pack_forget()
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = allert_server_pb2_grpc.AlertServiceStub(channel)

            # Customize your request based on the action
            if action_name == "Sharpen Image":
                # Example for sending an image
                
                response = stub.SendImageAlertOff(allert_server_pb2.SendImageAlertRequest())

            elif action_name == "Count Elements":
                # Example for counting objects
                response = stub.CountAlertOff(allert_server_pb2.CountAlertRequest())

            elif action_name == "Unusual Events":
                response = stub.OddEventAlertOff(allert_server_pb2.OddEventAlertRequest())

            elif action_name == "Accident":
                response = stub.AccidentAlertOff(allert_server_pb2.AccidentAlertRequest())

            elif action_name == "Area Is Empty":
                response = stub.IsEmptyAlertOff(allert_server_pb2.IsEmptyAlertRequest())

            elif action_name == "Border Control":
                response = stub.IsCrossAlertOff(allert_server_pb2.IsCrossAlertRequest())



def show_results_or_retry(label_num):
    elapsed_time = time.time() - start_times[label_num]
    if elapsed_time < 3:
        remaining_time = int(3 - elapsed_time)
        messagebox.showinfo("Retry", f"only {remaining_time} seconds  had passed from the time the alert was turned ON\nresults may not be ready yet")
    
    show_results(label_num)

right_frame = tk.Frame(root, bg="white", width=1050, height=800)
right_frame.pack(side='left', fill='both', expand=True)

left_frame = tk.Frame(root, bg="black", width=350, height=800)
left_frame.pack(side='right', fill='both', expand=True)

bg_image = Image.open("img/background.jpg")
bg_image = bg_image.resize((1400, 1000), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(right_frame, image=bg_photo)
bg_label.image = bg_photo
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

upper_left_frame = tk.Frame(left_frame, bg="white", width=350, height=root.winfo_screenheight() / 2)
upper_left_frame.pack(side='top', fill='both', expand=True)

lower_left_frame = tk.Frame(left_frame, bg="black", width=350, height=root.winfo_screenheight() / 2)
lower_left_frame.pack(side='bottom', fill='both', expand=False)
lower_left_frame.pack_propagate(0)

clear_all_button = tk.Button(left_frame, text="Clear All", bg="black", fg="white", command=clear_manual_results, font=('Helvetica', 12), highlightthickness=0)
clear_all_button.pack(side='bottom', fill='x')

for i in range(6):
    label_text_vars[i] = tk.StringVar()
    label_text_vars[i].set(f"{actions[i]}")

    frame = tk.Frame(right_frame, bg="black")
    frame.pack(side='left', padx=20)

    label = tk.Label(frame, textvariable=label_text_vars[i], font=('Helvetica', 18), highlightthickness=0, fg="white", bg="black")
    label.pack(side='top', fill='x')
    label.pack_propagate(False)

    button = tk.Button(frame, text="OFF", command=lambda i=i: toggle_state(i+1), bg="black", fg="white", font=('Helvetica', 12), highlightthickness=0, width=10)
    button.pack(side='top', padx=7, fill='x')
    button.pack_propagate(False)
    buttons.append(button)

    show_results_buttons[i + 1] = tk.Button(frame, text="Show Results", bg="black", fg="white", font=('Helvetica', 10), highlightthickness=0, command=lambda i=i: show_results(i + 1), width=10)
    show_results_buttons[i + 1].pack_forget()

root.after(4000, periodic_function)
root.mainloop()
