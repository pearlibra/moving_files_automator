from tkinter import *
from tkinter import ttk
from tkinterdnd2 import *

import glob
import subprocess
from subprocess import PIPE
import binascii
import shutil
import os 


def clean():
    frame4.tkraise()  # progressバーの表示

    with open('urls.txt', 'r') as urls:
        with open('target_directory.txt', 'r') as directory:
            urls_list = urls.readlines()
            to_directories = directory.readlines()

    # ディレクトリ名にスペースが入っている場合の対策
    for d in to_directories:
        d.replace(' ', '\ ')

    # ファイルごとにコマンド実行して入手先情報を得る
    for moved_file in file_list:
        pbval.set(pbval.get() + 1)  # progressバーを進める

        command = "xattr -p com.apple.metadata:kMDItemWhereFroms " + moved_file.replace(' ', '\ ')  
        out = subprocess.run(command, shell=True, stdout=PIPE, stderr=PIPE, text=True)
        hexadecimal = out.stdout

        # 16進数表示を直してstr型へ
        fixed_text = str(binascii.unhexlify(hexadecimal.replace(' ', '').replace('\n', '')))

        # ファイルごとにメタデータ(ダウンロード元)をチェックして移動
        for i, url in enumerate(urls_list):
            start_index = fixed_text.find(url)  #URLがヒットすれば0以上を返す

            # URL候補になければ次のURLへ
            if start_index == -1:
                continue

            # 候補にあれば転送する．転送先に同一名称ファイルがあった場合削除するか質問する．
            try:
                new_path = shutil.move(moved_file, to_directories[i])

            except shutil.Error:
                err_ele.append(moved_file)
                err_msg.set(err_msg.get() + '移動先に既に「' + moved_file + '」が存在しました．\n')

            except FileNotFoundError as e:
                err_msg.set(err_msg.get() + '「' + to_directories[i] + '」は存在しないパスです．設定を見直してください．\n') 

            else:
                moved_file_list.append(moved_file)

    # エラーが一つでもあればエラーフレームへ
    if (len(err_msg.get()) > 0):
        err_msg.set(err_msg.get() + '\nこれらのファイルを削除しますか？')
        frame5.tkraise()
    
    # エラーがなければ移動したファイル表示
    else:
        if (len(moved_file_list) > 0):
            suc_msg.set('\n'.join(moved_file_list) + '\nを移動しました．ウィンドウを閉じてください．')
            frame6.tkraise()
        else:
            suc_msg.set('今回移動できるファイルは見つかりませんでした．ウィンドウを閉じてください．')
            frame6.tkraise()


# エラーフレームでyesが押された場合
def respond_yes():
    for e in err_ele:
        os.remove(e)
    err_ele.clear()
    err_msg.set('')
    cleaning_clicked()


# エラーフレームでnoが押された場合
def respond_no():
    err_ele.clear()
    err_msg.set('')
    cleaning_clicked()


# ボタン1
def cleaning_clicked():
    button1.state(['pressed'])
    button2.state(['!pressed'])
    button3.state(['!pressed'])
    button4.state(['!pressed'])
    button5.state(['!pressed'])
    frame1.tkraise()


# ボタン2
def add_link_clicked():
    button1.state(['!pressed'])
    button2.state(['pressed'])
    button3.state(['!pressed'])
    button4.state(['!pressed'])
    button5.state(['!pressed'])
    frame2.tkraise()


# ボタン3
def remove_link_clicked():
    button1.state(['!pressed'])
    button2.state(['!pressed'])
    button3.state(['pressed'])
    button4.state(['!pressed'])
    button5.state(['!pressed'])
    frame3.tkraise()


# ボタン4
def add_source_clicked():
    button1.state(['!pressed'])
    button2.state(['!pressed'])
    button3.state(['!pressed'])
    button4.state(['pressed'])
    button5.state(['!pressed'])
    frame7.tkraise()


# ボタン5
def remove_source_clicked():
    button1.state(['!pressed'])
    button2.state(['!pressed'])
    button3.state(['!pressed'])
    button4.state(['!pressed'])
    button5.state(['pressed'])
    frame8.tkraise()


# addフレームのパス取得関数
def drop_link_path(event):
    added_link_path.set(event.data)


# add_sourceフレームのパス取得関数
def drop_source_path(event):
    added_source_path.set(event.data)


# パスとURLをファイルに記入する関数(addフレーム)
def write_path_and_url():
    with open('target_directory.txt', mode='a', encoding='UTF-8') as f:
        if (len(to_directories) == 0):
            f.write(added_link_path.get())
            to_directories.append(added_link_path.get())
        else:
            f.write('\n' + added_link_path.get())
            to_directories.append(added_link_path.get())
    with open('urls.txt', mode='a', encoding='UTF-8') as f:
        if (len(urls_list) == 0):
            f.write(added_url.get())
            urls_list.append(added_url.get())
        else:
            f.write('\n' + added_url.get())
            urls_list.append(added_url.get())
    tree3_1.insert(parent='', index='end', iid=len(urls_list)-1, values=(added_link_path.get(), added_url.get()))


# removeフレームで選択された要素を削除する関数
def delete_link_record(event):
    record_id = tree3_1.focus()
    record_values = tree3_1.item(record_id, 'values')
    try:
        tree3_1.delete(record_id)
    except Exception as e:
        pass
    try:
        urls_list.pop(int(record_id))
        to_directories.pop(int(record_id))
    except:
        pass
    with open('target_directory.txt', mode='w', encoding='UTF-8') as f:
        f.write('\n'.join(to_directories))
    with open('urls.txt', mode='w', encoding='UTF-8') as f:
        f.write('\n'.join(urls_list))


def write_source_path():
    with open('cleaning_directory.txt', mode='a', encoding='UTF-8') as f:
        if (len(from_directories) == 0):
            f.write(added_source_path.get())
            from_directories.append(added_source_path.get())
        else:
            f.write('\n' + added_source_path.get())
            from_directories.append(added_source_path.get())
    tree8_1.insert(parent='', index='end', iid=len(from_directories)-1, values=(added_source_path.get()))
    

def delete_source_record(event):
    record_id = tree8_1.focus()
    record_values = tree8_1.item(record_id, 'values')
    try:
        tree8_1.delete(record_id)
    except Exception as e:
        pass
    try:
        from_directories.pop(int(record_id))
    except:
        pass
    with open('cleaning_directory.txt', mode='w', encoding='UTF-8') as f:
        f.write('\n'.join(from_directories))


# ベースウィンドウ
root = TkinterDnD.Tk()
root.title('File Cleaning')
root.geometry("815x300")

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# 移動させるファイルが格納されているディレクトリのパス情報をcleaning_directoryから取得
f = open('cleaning_directory.txt', 'r')
from_directories = f.readlines()
f.close()

# 上記のディレクトリに格納されているファイルを全てfile_listへ
file_list = []
for d in from_directories:
    file_list += glob.glob(d + "/*")

# -----メニューフレーム-----
mode_frame = ttk.Frame(root)
mode_frame.grid(row=0, column=0)

button1 = ttk.Button(
    mode_frame,
    text='Cleaning',
    command=cleaning_clicked,
)
button1.pack(side=LEFT)

button2 = ttk.Button(
    mode_frame,
    text='Add link',
    command=add_link_clicked,
)
button2.pack(side=LEFT)

button3 = ttk.Button(
    mode_frame,
    text='Remove link',
    command=remove_link_clicked,
)
button3.pack(side=LEFT)

button4 = ttk.Button(
    mode_frame,
    text='Add source',
    command=add_source_clicked,
)
button4.pack(side=LEFT)

button5 = ttk.Button(
    mode_frame,
    text='Remove source',
    command=remove_source_clicked,
)
button5.pack(side=LEFT)


# -----cleaningフレーム-----
frame1 = ttk.Frame(root)
frame1.grid(row=1, column=0, sticky="nsew", pady=20)

button1_1 = ttk.Button(
    frame1,
    text="Let's clean!",
    command=clean,
)
button1_1.pack()


# -----add linkフレーム-----
frame2 = ttk.Frame(root)
frame2.grid(row=1, column=0, sticky="nsew", pady=20)

label2_1 = ttk.Label(
    frame2, 
    text='Folder Path',
)
label2_1.pack() 

added_link_path = StringVar()
entry2_1 = ttk.Entry(
    frame2,
    textvar=added_link_path,
)
entry2_1.drop_target_register(DND_FILES)
entry2_1.dnd_bind('<<Drop>>', func=drop_link_path)
entry2_1.pack() #配置の調整必要

label2_2 = ttk.Label(
    frame2, 
    text='URL',
)
label2_2.pack() 

added_url = StringVar()
entry2_2 = ttk.Entry(
    frame2,
    textvar=added_url,
)
entry2_2.pack()

button2_3 = ttk.Button(
    frame2,
    text="Add",
    command=write_path_and_url, 
)
button2_3.pack()


# -----remove linkフレーム-----
frame3 = ttk.Frame(root)
frame3.grid(row=1, column=0, sticky="nsew", pady=20)

# 列の識別名を指定
column = ('パス', 'URL')

tree3_1 = ttk.Treeview(frame3, columns=column)
tree3_1.bind("<<TreeviewSelect>>", delete_link_record)

# 列の設定
tree3_1.column('#0',width=0, stretch='no')
tree3_1.column('パス', anchor='w', width=400)
tree3_1.column('URL',anchor='w', width=400)

# 列の見出し設定
tree3_1.heading('#0',text='')
tree3_1.heading('パス', text='パス',anchor='center')
tree3_1.heading('URL', text='URL', anchor='w')

# テキストファイルからURL情報と移動先を入手
with open('urls.txt', 'r') as urls:
        with open('target_directory.txt', 'r') as directory:
            urls_list = urls.readlines()
            to_directories = directory.readlines()

# treeviewに追加
for r in range(len(urls_list)):
    tree3_1.insert(parent='', index='end', iid=r, values=(to_directories[r], urls_list[r]))  #iid=rはtree3_1.focus()で行番号を得るため

# スクロールバーの追加
scrollbar = ttk.Scrollbar(frame3, orient='vertical', command=tree3_1.yview)
tree3_1.configure(yscroll=scrollbar.set)

# ウィジェットの配置
tree3_1.pack(side='left')
scrollbar.pack(side='right', fill='y')


# -----progressフレーム(進捗状況を示す)-----
frame4 = ttk.Frame(root)
frame4.grid(row=1, column=0, sticky="nsew", pady=20)


# progressバー
pbval = IntVar()
pb4 = ttk.Progressbar(
    frame4,
    orient=HORIZONTAL,
    variable=pbval,
    maximum=len(file_list),
    length=200,
    mode='determinate')
pb4.pack()


# -----errorフレーム-----
frame5 = ttk.Frame(root)
frame5.grid(row=1, column=0, sticky="nsew", pady=20)

err_ele = []  # clean関数を走らせて移動できなかったファイル
moved_file_list = []  # 正常に移動できたファイル

err_msg = StringVar()
label5 = ttk.Label(
    frame5,
    textvariable=err_msg,
)
label5.pack()

# yesボタン
button5_1 = ttk.Button(
    frame5,
    text='Yes',
    width=5,
    command=respond_yes,
)
button5_1.pack()

# noボタン
button5_2 = ttk.Button(
    frame5,
    text='No',
     width=5,
    command=cleaning_clicked,
)
button5_2.pack()


# -----endフレーム-----
frame6 = ttk.Frame(root)
frame6.grid(row=1, column=0, sticky="nsew", pady=20)

# 正常終了メッセージ
suc_msg = StringVar()
label6 = ttk.Label(
    frame6,
    textvariable=suc_msg,
)
label6.pack()


# -----add sourceフレーム-----
frame7 = ttk.Frame(root)
frame7.grid(row=1, column=0, sticky="nsew", pady=20)

label7 = ttk.Label(
    frame7, 
    text='Folder Path',
)
label7.pack() 

added_source_path = StringVar()
entry7 = ttk.Entry(
    frame7,
    textvar=added_source_path,
)
entry7.drop_target_register(DND_FILES)
entry7.dnd_bind('<<Drop>>', func=drop_source_path)
entry7.pack()

button7 = ttk.Button(
    frame7,
    text="Add",
    command=write_source_path, 
)
button7.pack()


# -----remove sourceフレーム-----
frame8 = ttk.Frame(root)
frame8.grid(row=1, column=0, sticky="nsew", pady=20)

# 列の識別名を指定
column_source = ('パス')

tree8_1 = ttk.Treeview(frame8, columns=column_source)
tree8_1.bind("<<TreeviewSelect>>", delete_source_record)

# 列の設定
tree8_1.column('#0',width=0, stretch='no')
tree8_1.column('パス', anchor='w', width=800)

# 列の見出し設定
tree8_1.heading('#0',text='')
tree8_1.heading('パス', text='パス',anchor='center')

# treeviewに追加
for r in range(len(from_directories)):
    tree8_1.insert(parent='', index='end', iid=r, values=(from_directories[r]))  #iid=rはtree8_1.focus()で行番号を得るため

# スクロールバーの追加
scrollbar = ttk.Scrollbar(frame8, orient='vertical', command=tree8_1.yview)
tree8_1.configure(yscroll=scrollbar.set)

# ウィジェットの配置
tree8_1.pack(side='left')
scrollbar.pack(side='right', fill='y')

# cleaningフレームから開始
button1.state(['pressed'])
frame1.tkraise()

root.mainloop()