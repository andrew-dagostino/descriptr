"""
This file contains helper functions used by the Course class
"""

"""
Convert one long line of text to a bunch of lines of wrapped text at a certain max length
"""
def multi_line_repr(text, max_line_len):
	text = text.replace("\n", " ") #Replace newlines with spaces as we want control of where newlines are printed

	lines = []
	
	curr_line = ""
	curr_line_start = 0
	text_len = len(text)

	while curr_line_start < text_len:
		curr_line_end = min((curr_line_start+max_line_len), text_len)
		while curr_line_end != text_len and (text[curr_line_end] != " "):
			curr_line_end -= 1

		curr_line = text[curr_line_start:curr_line_end]
		lines.append(curr_line)
		curr_line_start = curr_line_end + 1

	return lines
	