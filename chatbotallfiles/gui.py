import tkinter as tk
from chatbot import SimpleChatbot

class ChatbotGUI:
    def __init__(self, master):
        self.master = master
        master.title("Simple Chatbot")

        self.chatbot = SimpleChatbot()

        self.chat_log = tk.Text(master, state='disabled', width=80, height=20, bg="white", fg="black")
        self.chat_log.grid(row=0, column=0, columnspan=2)

        self.entry_box = tk.Entry(master, width=60, bg="white", fg="black")
        self.entry_box.grid(row=1, column=0)

        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1)

        self.master.bind("<Return>", self.send_message_event)

    def send_message_event(self, event):
        self.send_message()

    def send_message(self):
        user_input = self.entry_box.get()
        self.entry_box.delete(0, tk.END)

        self.chat_log.configure(state='normal')
        self.chat_log.insert(tk.END, "You: " + user_input + "\n")
        self.chat_log.configure(state='disabled')

        response, _ = self.chatbot.process_input(user_input, "text")
        self.chat_log.configure(state='normal')
        self.chat_log.insert(tk.END, "Chatbot: " + response + "\n")
        self.chat_log.configure(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    chatbot_gui = ChatbotGUI(root)
    root.mainloop()
