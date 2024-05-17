import tkinter as tk
import keyword
import re

class SyntaxHighlighter:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.text_widget.tag_configure("keyword", foreground="blue")
        self.text_widget.tag_configure("comment", foreground="green")
        self.text_widget.tag_configure("variable", foreground="orange")

    def highlight_syntax(self, event=None):
        self.text_widget.tag_remove("keyword", "1.0", "end")
        self.text_widget.tag_remove("comment", "1.0", "end")
        self.text_widget.tag_remove("variable", "1.0", "end")

        current_line = self.text_widget.get("insert linestart", "insert lineend")
        current_words = re.findall(r"\b\w+\b", current_line)

        for kw in keyword.kwlist:
            if kw in current_words:
                self.highlight_pattern(r"\b" + kw + r"\b", "keyword")

        self.highlight_pattern(r"\bif\b", "keyword")
        self.highlight_pattern(r"\bfor\b", "keyword")
        self.highlight_pattern(r"\b[A-Za-z]+\b", "variable")
        self.highlight_pattern("#.*", "comment")

    def highlight_pattern(self, pattern, tag, start="1.0", end="end"):
        start = self.text_widget.index(start)
        end = self.text_widget.index(end)
        self.text_widget.mark_set("matchStart", start)
        self.text_widget.mark_set("matchEnd", start)
        self.text_widget.mark_set("searchLimit", end)

        count = tk.IntVar()
        while True:
            index = self.text_widget.search(pattern, "matchEnd", "searchLimit", count=count, regexp=True)
            if not index:
                break
            self.text_widget.mark_set("matchStart", index)
            self.text_widget.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.text_widget.tag_add(tag, "matchStart", "matchEnd")
