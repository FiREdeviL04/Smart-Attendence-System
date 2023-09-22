import time
import cv2
import pandas
import notification
import recognition as rr

stop_recognition = False
from tkinter import *

BACKGROUND_COLOR = "#B1DDC6"


def register():
    def submit():
        roll_no = roll_no_var.get()
        name = name_var.get()
        email = email_var.get()

        roll_no = int(roll_no)
        df = pandas.DataFrame({
            "rollno": [roll_no],
            "name": [name],
            "email": [email]
        })
        samplenum = 1

        df.to_csv("records.csv", mode='a', index=False, header=False)
        # data = pandas.read_csv("records.csv")
        # sorted_data = data.sort_values(by=["rollno"])
        # sorted_data.to_csv("records.csv", index=False)

        face_classifier = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        video_capture = cv2.VideoCapture(0)

        while True:
            result, video_frame = video_capture.read()

            if not result:
                print("Error: Could not load image from camera")
                break

            gray_image = cv2.cvtColor(video_frame, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))

            for (x, y, w, h) in faces:
                time.sleep(1.2)
                cv2.rectangle(video_frame, (x, y), (x + w, y + h), (0, samplenum, samplenum), 4)
                # key = cv2.waitKey(1000)

                cv2.imwrite(f"database/{roll_no}.{samplenum}.jpg", video_frame)

            cv2.imshow(
                "Image", video_frame
            )
            samplenum += 1
            print(samplenum)
            if samplenum > 7:
                break

            if cv2.waitKey(1) & 0xFF == 27:
                break

        video_capture.release()
        cv2.destroyAllWindows()
        window.destroy()

    roll_no_var = StringVar()
    name_var = StringVar()
    email_var = StringVar()

    button_2.destroy()
    button_1.destroy()
    canvas.itemconfig(card_title, text='Register for Smart Attendance')

    roll_no_label = Label(text="Roll number: ",  font=('Ariel', 10), bg=BACKGROUND_COLOR,width=10, height=1)
    roll_no_label.grid(row=1, column=0)
    Entry(textvariable=roll_no_var, bg=BACKGROUND_COLOR, width=30).grid(row=1, column=1, padx=0, pady=0, rowspan=1)

    name_label = Label(text="Name: ", font=('Ariel', 10), bg=BACKGROUND_COLOR,width=10,height=1)
    name_label.grid(row=2, column=0)
    Entry(textvariable=name_var,bg=BACKGROUND_COLOR, width=30).grid(row=2, column=1, padx=0, pady=0,rowspan=1)

    email_i_label = Label(text="Email: ",  font=('Ariel', 10), bg=BACKGROUND_COLOR,width=10,height=1)
    email_i_label.grid(row=3, column=0)
    Entry(textvariable=email_var, bg=BACKGROUND_COLOR, width=30).grid(row=3, column=1, pady=0, padx=0,rowspan=1)

    submit = Button(text="Submit", width=10, height=2, bg=BACKGROUND_COLOR, font=('Ariel', 10), command=submit)
    submit.grid(row=4, column=1)


def start_recognition():
    global stop_recognition
    stop_recognition = False
    # lbl_status.config(text="Status: Recognizing...")

    faces, labels = rr.load_training_data()
    recognizer = rr.train_model(faces, labels)
    samplecount = 0
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    video_capture = cv2.VideoCapture(0)

    while True:
        if stop_recognition:
            break
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

        for (x, y, w, h) in faces:
            face = gray[y:y + h, x:x + w]
            id_ = rr.predict(recognizer, face)
            name = rr.get_name(id_)
            samplecount = samplecount + 1

            cv2.putText(frame, name, (x, y), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)

            cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break
        if samplecount > 50:
            break

    video_capture.release()
    cv2.destroyAllWindows()
    list_of = notification.absent_students()
    # print(list_of)
    button_1.destroy()
    button_2.destroy()
    done_text = Label(text="Done!", font=('Ariel', 20))
    done_text.grid(row=2, column=1)

    email = Label(text=f"Sent Email to Absent Students: \n{list_of}", font=('Ariel', 17))
    email.grid(row=3, column=1)

    # lbl_status.config(text="Status: Done!")


def stop_recognition_process():
    global stop_recognition
    stop_recognition = True
    cv2.destroyAllWindows()


window = Tk()
window.title('Smart Attendance System')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=528, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front = PhotoImage(file='card_front.png')
card_background = canvas.create_image(400, 264, image=card_front)
card_title = canvas.create_text(400, 70, text='Smart Attendance System', font=('Ariel', 29))
canvas.grid(row=0, column=0, columnspan=3, rowspan=5)

button_1 = Button(text="Take Attendance", width=30, height=4, bg=BACKGROUND_COLOR, font=('Ariel', 13),
                  command=start_recognition)
button_1.grid(row=2, column=1)

button_2 = Button(text="Register", width=30, height=4, bg=BACKGROUND_COLOR, font=('Ariel', 13), command=register)
button_2.grid(row=3, column=1)

window.mainloop()