import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from DrissionPage import ChromiumPage
import pandas as pd
from datetime import datetime
import threading
import queue
import time
import json
import os


class SettingsManager:
    def __init__(self, filename="post2_config.json"):
        self.filename = filename
        self.settings = {
            "mode": "1",
            "email_numbers": "",
            "save_path": "./"
        }

    def load_settings(self):
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.settings = json.load(f)
            return self.settings
        except Exception as e:
            messagebox.showwarning("设置加载错误", f"无法加载设置文件: {str(e)}")
            return self.settings

    def save_settings(self, settings):
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4)
            return True
        except Exception as e:
            messagebox.showerror("设置保存错误", f"无法保存设置: {str(e)}")
            return False


class MailQueryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("邮件查询工具")
        self.root.geometry("700x500")

        # 控制变量
        self.running = False
        self.paused = False
        self.stop_flag = False
        self.log_queue = queue.Queue()

        self.create_widgets()
        self.check_log_queue()

        self.settings_manager = SettingsManager()
        self.load_settings()

        # 在窗口关闭时保存设置
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_settings(self):
        settings = self.settings_manager.load_settings()
        self.mode_var.set(settings.get("mode", "2"))
        self.email_text.delete("1.0", tk.END)
        self.email_text.insert(tk.END, settings.get("email_numbers", ""))
        self.path_var.set(settings.get("save_path", "./"))

    def save_current_settings(self):
        current_settings = {
            "mode": self.mode_var.get(),
            "email_numbers": self.email_text.get("1.0", tk.END).strip(),
            "save_path": self.path_var.get()
        }
        return self.settings_manager.save_settings(current_settings)

    def on_closing(self):
        self.save_current_settings()
        self.root.destroy()

    def create_widgets(self):
        # 顶部框架 - 参数设置
        top_frame = ttk.LabelFrame(self.root, text="查询参数", padding=10)
        top_frame.pack(fill=tk.X, padx=10, pady=5)

        # 模式选择
        ttk.Label(top_frame, text="模式选择:").grid(row=0, column=0, sticky=tk.W)
        self.mode_var = tk.StringVar(value="2")
        ttk.Radiobutton(top_frame, text="模式1", variable=self.mode_var, value="1").grid(row=0, column=1, sticky=tk.W)
        ttk.Radiobutton(top_frame, text="模式2", variable=self.mode_var, value="2").grid(row=0, column=2, sticky=tk.W)

        # 邮件号输入
        ttk.Label(top_frame, text="邮件号(每行一个):").grid(row=1, column=0, sticky=tk.NW)
        self.email_text = scrolledtext.ScrolledText(top_frame, width=40, height=6)
        self.email_text.grid(row=1, column=1, columnspan=3, sticky=tk.W)
        self.email_text.insert(tk.END,
                               "9808763539503\n9808763925267\n9808764271236\n9808765579183\n9808765581036\n9879632669958")

        # 保存路径
        ttk.Label(top_frame, text="保存路径:").grid(row=2, column=0, sticky=tk.W)
        self.path_var = tk.StringVar()
        ttk.Entry(top_frame, textvariable=self.path_var, width=40).grid(row=2, column=1, sticky=tk.W)
        ttk.Button(top_frame, text="浏览...", command=self.select_path).grid(row=2, column=2, sticky=tk.W)

        # 控制按钮框架
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=5)

        self.start_button = ttk.Button(button_frame, text="开始查询", command=self.start_query)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = ttk.Button(button_frame, text="暂停", command=self.pause_query, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=5)

        ttk.Button(button_frame, text="清空日志", command=self.clear_log).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="退出", command=self.root.quit).pack(side=tk.RIGHT, padx=5)

        # 进度条
        self.progress = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, length=880, mode='determinate')
        self.progress.pack(padx=10, pady=5)

        # 日志输出
        log_frame = ttk.LabelFrame(self.root, text="日志输出", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.log_text = scrolledtext.ScrolledText(log_frame, width=100, height=20)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def select_path(self):
        path = filedialog.askdirectory()
        if path:
            self.path_var.set(path)

    def start_query(self):
        if self.running:
            return

        email_num = self.email_text.get("1.0", tk.END).strip()
        if not email_num:
            messagebox.showerror("错误", "请输入邮件号！")
            return

        self.running = True
        self.paused = False
        self.stop_flag = False

        self.start_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)

        # 启动查询线程
        query_thread = threading.Thread(target=self.run_query, daemon=True)
        query_thread.start()

    def pause_query(self):
        if not self.running:
            return

        self.paused = not self.paused
        if self.paused:
            self.pause_button.config(text="继续")
            self.log_message("查询已暂停")
        else:
            self.pause_button.config(text="暂停")
            self.log_message("查询已继续")

    def stop_query(self):
        self.stop_flag = True
        if self.paused:
            self.paused = False
            self.pause_button.config(text="暂停")

    def clear_log(self):
        self.log_text.delete("1.0", tk.END)

    def log_message(self, message):
        self.log_queue.put(message)

    def check_log_queue(self):
        while not self.log_queue.empty():
            message = self.log_queue.get_nowait()
            self.log_text.insert(tk.END, message + "\n")
            self.log_text.see(tk.END)
        self.root.after(100, self.check_log_queue)

    def update_progress(self, value):
        self.progress["value"] = value
        self.root.update_idletasks()

    def run_query(self):
        try:
            mode = int(self.mode_var.get())
            email_num = self.email_text.get("1.0", tk.END).strip()
            file_path = self.path_var.get() or "./"

            if not file_path.endswith('/') and not file_path.endswith('\\'):
                file_path += '/'

            # 准备数据结构
            mode1_data = {
                '序号': [], '邮件号': [], '日期': [],
                '当前处理动作': [], '当前处理机构': [],
            }

            mode2_data = {
                '序号': [], '邮件号': [], '时间': [], '处理机构': [],
                '处理动作': [], '详细说明': [], '操作员': [], '来源': [],
                '备注': [], '信息采集点': [], '采集方式': [], '采集工具': [],
            }

            def find_ele_safe(page, xpath):
                try:
                    return page.ele(f'xpath:{xpath}', timeout=3)
                except:
                    self.log_message(f'未找到{xpath}')
                    return None

            # 创建页面对象
            self.log_message("正在启动浏览器...")
            page = ChromiumPage()
            page.get('https://10.4.188.1/cas/login?service=https://10.4.188.1/portal/a/cas&t=')
            self.log_message("浏览器已启动，正在加载页面...")

            # 弹出提示框让用户手动操作
            messagebox.showinfo("提示", "请在浏览器中完成登录操作后点击确定继续")

            page.get('https://10.4.188.1/querypush-web/a/qps/qpswaybilltraceinternal/traceList')

            self.log_message("正在输入邮件号并提交查询...")
            page.ele('xpath://*[@id="traceNo"]').clear()
            page.ele('xpath://*[@id="traceNo"]').input(email_num)
            page.ele('xpath://*[@id="btnSubmit"]').click()

            find_ele_safe(page, '//tr[contains(@id,"trace")]')
            result_1 = page.eles('xpath://tr[contains(@id,"trace")]')

            total_items = len(result_1)
            self.log_message(f"找到 {total_items} 条邮件记录，正在处理...")

            for num in range(len(result_1)):
                while self.paused and not self.stop_flag:
                    time.sleep(0.5)
                    continue

                if self.stop_flag:
                    self.log_message("查询已停止")
                    break

                progress = (num + 1) / total_items * 100
                self.update_progress(progress)

                number = page.ele(f'xpath://*[@id="trace{num}"]//td[1]').text
                email_number = page.ele(f'xpath://*[@id="trace{num}"]//td[2]').text

                if mode == 1:
                    r1_date = page.ele(f'xpath://*[@id="trace{num}"]//td[3]').text
                    current_processing_action = page.ele(f'xpath://*[@id="trace{num}"]//td[4]').text
                    current_processing_organization = page.ele(f'xpath://*[@id="trace{num}"]//td[5]').text

                    self.log_message(
                        f"{number} {email_number} {r1_date} {current_processing_action} {current_processing_organization}")

                    mode1_data['序号'].append(number)
                    mode1_data['邮件号'].append(email_number)
                    mode1_data['日期'].append(r1_date)
                    mode1_data['当前处理动作'].append(current_processing_action)
                    mode1_data['当前处理机构'].append(current_processing_organization)

                if mode == 2:
                    page.ele(f'xpath://*[@id="trace{num}"]//td[2]').click()
                    find_ele_safe(page, f'//*[@class="trtrace{num}"]')
                    result_2 = page.eles(f'xpath://*[@class="trtrace{num}"]//*[@class="detail_table"]//tbody/tr')

                    for r2 in result_2:
                        r2_date = r2.ele('xpath://td[1]').text
                        processing_organization = r2.ele('xpath://td[2]').text
                        processing_action = r2.ele('xpath://td[3]').text
                        detailed_description = r2.ele('xpath://td[4]').text.replace('\n', ' ')
                        operator = r2.ele('xpath://td[5]').text
                        source = r2.ele('xpath://td[6]').text
                        remark = r2.ele('xpath://td[7]').text.replace('\n', ' ')
                        information_collection_point = r2.ele('xpath://td[8]').text
                        collection_method = r2.ele('xpath://td[9]').text
                        collection_tools = r2.ele('xpath://td[10]').text

                        self.log_message(
                            f"{number} {email_number} {r2_date} {processing_organization} {processing_action} {detailed_description} {operator} {source} {remark} {information_collection_point} {collection_method} {collection_tools}")

                        mode2_data['序号'].append(number)
                        mode2_data['邮件号'].append(email_number)
                        mode2_data['时间'].append(r2_date)
                        mode2_data['处理机构'].append(processing_organization)
                        mode2_data['处理动作'].append(processing_action)
                        mode2_data['详细说明'].append(detailed_description)
                        mode2_data['操作员'].append(operator)
                        mode2_data['来源'].append(source)
                        mode2_data['备注'].append(remark)
                        mode2_data['信息采集点'].append(information_collection_point)
                        mode2_data['采集方式'].append(collection_method)
                        mode2_data['采集工具'].append(collection_tools)

            if not self.stop_flag:
                current_time = datetime.now().strftime("%Y%m%d%H%M%S")
                if mode == 1:
                    df = pd.DataFrame(mode1_data)
                    output_file = f'{file_path}模式{str(mode)}_{current_time}.xlsx'
                    df.to_excel(output_file, index=False)
                elif mode == 2:
                    df = pd.DataFrame(mode2_data)
                    output_file = f'{file_path}模式{str(mode)}_{current_time}.xlsx'
                    df.to_excel(output_file, index=False)

                self.log_message(f"文件已经保存至 {output_file}")
                self.log_message("爬取完成")
                messagebox.showinfo("完成", f"查询完成！结果已保存至:\n{output_file}")

        except Exception as e:
            self.log_message(f"发生错误: {str(e)}")
            messagebox.showerror("错误", f"发生错误: {str(e)}")

        finally:
            self.running = False
            self.paused = False
            self.stop_flag = False
            self.start_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED, text="暂停")
            self.update_progress(0)


if __name__ == "__main__":
    root = tk.Tk()
    app = MailQueryApp(root)
    root.mainloop()