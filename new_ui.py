import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def open_image(): #진로를 확인할 얼굴의 이미지를 선택하고 미리보기 함수 정의
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;")]) #이미지이므로 png, jpg, jpeg만 추가 가능하도록 함
    if file_path:
        image = Image.open(file_path)
        new_width = 200
        new_height = int(image.size[1] * (new_width / image.size[0]))
        image = image.resize((new_width, new_height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        input_image.config(image=photo)
        input_image.image = photo
        button_confirm_image.config(state="normal") #이미지가 정상적으로 추가되었다면 확인 버튼 활성화
    else:
        button_confirm_image.config(state="disabled")  #이미지가 추가되지 않았다면 확인 버튼 비활성화

def animate_gif(label, frames, index): #로딩화면에서 해당 gif가 보이게 하는 함수 정의
    frame = frames[index]
    label.config(image=frame)
    label.image = frame
    root.after(100, animate_gif, label, frames, (index + 1) % len(frames))

root = tk.Tk()
root.title("AI에게 맡겨보는 적성에 맞는 직업 찾기") #실행 창 타이틀
root.geometry("480x480") #실행 창 크기
root.resizable(False, False)# 실행 창 사이즈를 줄이거나 늘릴 수 없게 설정

def show_frame(frame): #화면에 창을 띄우는 함수 정의
    frame.tkraise()

# 시작 화면 프레임 생성
main_frame = tk.Frame(root)
main_frame.grid(row=0, column=0, sticky='nsew')

#시작 화면 배경을 이미지로 변경하기 위해 이미지 파일 주소와, 캔버스를 정의
background_image = Image.open("background.jpg")
background_image = background_image.resize((480, 480), Image.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)

canvas = tk.Canvas(main_frame, width=480, height=480)
canvas.grid(row=0, column=0, columnspan=2, rowspan=4)
canvas.create_image(0, 0, anchor='nw', image=background_photo)


label_main = tk.Label(main_frame, text="AI에게 맡겨보는 적성에 맞는 직업 찾기", font=("Arial Unicode MS", 20), bg="white") #라벨로 프로그램의 정보 제공
label_main.grid(row=0, column=0, columnspan=2, pady=20)

input_image = tk.Label(main_frame, bg="white") #앞서 정의하 이미지 미리보기 출력
input_image.grid(row=1, column=0, columnspan=2, pady=20)

button = tk.Frame(main_frame, bg="white") #main_frame에서 사용할 버튼들을 사전 정의
button.grid(row=2, column=0, columnspan=2, pady=20)

button_select_image = tk.Button(button, text="이미지 선택", command=open_image, font=("Arial Unicode MS", 20)) #버튼을 클릭 시, 이미지 선택 창 열림
button_select_image.grid(row=0, column=0, padx=10)
button_confirm_image = tk.Button(button, text="관상 확인받기", command=lambda: show_frame(loading_frame),
                                 font=("Arial Unicode MS", 20), state="disabled") #이미지를 추가하기전에는 비활성화, 이미지가 추가되면 활성화됨, 클릭 시 로딩화면으로 전환
button_confirm_image.grid(row=0, column=1, padx=10)

# 로딩 프레임 생성
loading_frame = tk.Frame(root)
loading_frame.grid(row=0, column=0, sticky='nsew')

for frame in (main_frame, loading_frame):
    frame.grid(row=0, column=0, sticky='nsew')

label_loading = tk.Label(loading_frame, text="로딩 중...", font=("Arial Unicode MS", 20)) #로딩 중이라는 라벨 출력
label_loading.grid(row=0, column=0, pady=20)

try:
    loading_gif = Image.open("loading.gif")
    frames = []
    try:
        while True:
            frame = ImageTk.PhotoImage(loading_gif.copy().resize((150, 150), Image.LANCZOS))
            frames.append(frame)
            loading_gif.seek(len(frames))
    except EOFError:
        pass

    label_loading_image = tk.Label(loading_frame) #생성한 gif를 불러와서 프레임에 출력
    label_loading_image.grid(row=1, column=0, pady=20)
    animate_gif(label_loading_image, frames, 0)
except FileNotFoundError:
    label_loading_image = tk.Label(loading_frame, text="로딩 이미지를 찾을 수 없습니다.", font=("Arial Unicode MS", 20)) #해당 경로에 gif 파일이 없는 경우 문구 출력
    label_loading_image.grid(row=1, column=0, pady=20)

#위에서 선언한 요소들이 가운데 정렬되도록 함
root.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)
loading_frame.grid_columnconfigure(0, weight=1)

show_frame(main_frame)
root.mainloop() #창 실행
