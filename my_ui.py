import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def show_frame(frame):
    frame.tkraise()

def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;")])  # 파일 선택 창 열기
    if file_path:  # 파일 경로가 유효한 경우
        image = Image.open(file_path)  # 이미지 열기

        new_width = 200 # 이미지 크기 조절
        new_height = int(image.size[1] * (new_width / image.size[0]))
        image = image.resize((new_width, new_height), Image.LANCZOS)  # 이미지 크기 조절 및 리샘플링 필터 적용

        photo = ImageTk.PhotoImage(image)  # Tkinter에서 사용할 수 있는 형식으로 변환
        label_image.config(image=photo)  # 라벨에 이미지 설정
        label_image.image = photo  # 참조 유지


def clear_image():
    label_image.config(image='')  # 라벨에서 이미지 제거
    label_image.image = None  # 참조 제거


def animate_gif(label, frames, index):
    frame = frames[index]
    label.config(image=frame)
    label.image = frame  # 참조 유지
    root.after(100, animate_gif, label, frames, (index + 1) % len(frames))


root = tk.Tk()  # Tkinter 창 생성
root.title("AI 서비스와 UI")  # 창 제목 설정
root.geometry("480x480")  # 창 크기 설정 (너비x높이)
root.resizable(False, False)  # 창 크기를 고정 (선택 사항)

main_frame = tk.Frame(root)
main_frame.grid(row=0, column=0, sticky='nsew')  # 메인 프레임 생성

label_main = tk.Label(main_frame, text="시작 화면", font=(20))
label_main.grid(row=0, column=0, pady=20)

button_main = tk.Button(main_frame, text="관상 확인하기", command=lambda: show_frame(image_frame), font=(20))
button_main.grid(row=1, column=0, pady=10)

image_frame = tk.Frame(root)
image_frame.grid(row=0, column=0, sticky='nsew')  # 이미지 프레임 생성

label_image = tk.Label(image_frame)
label_image.grid(row=0, column=0, pady=10)

button_select_image = tk.Button(image_frame, text="이미지 선택", command=open_image, font=(20))
button_select_image.grid(row=1, column=0, pady=5)
button_confirm_image = tk.Button(image_frame, text="관상 확인받기", command=lambda: show_frame(loading_frame), font=(20))
button_confirm_image.grid(row=2, column=0, pady=5)
button_back = tk.Button(image_frame, text="돌아가기", command=lambda: [clear_image(), show_frame(main_frame)], font=(20))
button_back.grid(row=3, column=0, pady=5)

loading_frame = tk.Frame(root)
loading_frame.grid(row=0, column=0, sticky='nsew')  # 로딩 프레임 생성
for frame in (main_frame, image_frame, loading_frame):
    frame.grid(row=0, column=0, sticky='nsew')

label_loading = tk.Label(loading_frame, text="로딩 중...", font=(20))
label_loading.grid(row=0, column=0, pady=20)

try:
    loading_gif = Image.open("loading.gif")  # 로딩 GIF 파일을 열기
    frames = []
    try:
        while True:
            frame = ImageTk.PhotoImage(loading_gif.copy().resize((150, 150), Image.LANCZOS))
            frames.append(frame)
            loading_gif.seek(len(frames))  # 다음 프레임으로 이동
    except EOFError:
        pass

    label_loading_image = tk.Label(loading_frame)
    label_loading_image.grid(row=1, column=0, pady=10)
    animate_gif(label_loading_image, frames, 0)
except FileNotFoundError:
    label_loading_image = tk.Label(loading_frame, text="로딩 이미지를 찾을 수 없습니다.", font=(20))
    label_loading_image.grid(row=1, column=0, pady=10)

root.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(0, weight=1)
image_frame.grid_columnconfigure(0, weight=1)
loading_frame.grid_columnconfigure(0, weight=1)

show_frame(main_frame)  # 초기화면 설정

root.mainloop()  # Tkinter 창 실행
