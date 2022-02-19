#!/bin/python3

# usage: python pdfFileMergerCustom.py <lab Mnaual Folder> <tasks Folder>

import sys
import os

try:
	from PyPDF2 import PdfFileMerger, PdfFileReader
except ImportError:
	try:
		os.system("python -m pip install PyPDF2")
	except:
		print("You have to install PyPDF2 yourself.")
		sys.exit(1)

	else:
		from PyPDF2 import PdfFileMerger, PdfFileReader

class Work:
	def __init__(self, labFolder, tasksFolder):

		self.labDir = labFolder
		self.tasksDir = tasksFolder
		self.fm = PdfFileMerger()
		
		self.taskList = list()
		self.labList = list()
		
	def clean(self, dirr):
		lis = list()
		# dirRead = sorted(os.listdir(dirr))
		# r = list()
		dirRead = list()
		for root, dirs, files in os.walk(dirr):
			for file in files:
				dirRead.append(os.path.join(root, file))
		dirRead = sorted(dirRead)
		tmp1, tmp2 = None, None
		for i in range(1, 12):
			if "10" in dirRead[i -1]:
				tmp1 = dirRead[i - 1]

			elif "11" in dirRead[i -1]:
				tmp2 = dirRead[i - 1]
			else:
				lis.append(dirRead[i - 1])

		lis.append(tmp1)
		lis.append(tmp2)
		return lis


	def make(self):
		self.labList = self.clean(self.labDir)
		self.taskList = self.clean(self.tasksDir)

		# print(self.labList)
		# print(self.taskList)

		for lab, task in zip(self.labList, self.taskList):
			print(lab + " => " + task)

		if len(self.labList) == len(self.taskList):
			for lab, task in zip(self.labList, self.taskList):

				try:
					self.fm.append(PdfFileReader(f"{lab}", 'rb'))
					self.fm.append(PdfFileReader(f"{task}", 'rb'))
				except Exception as e:
					print(f"Error on {lab}", e)

			os.chdir(self.tasksDir)
			self.fm.write("New.pdf")
			self.fm = PdfFileMerger()



			# Prepending Front Page
			# frontPage = str(input("Drag and Drop Front Page pdf File: "))
			# frontPage = frontPage.replace("'", "")
			os.chdir("..")

			self.fm.append(PdfFileReader("Front Page.pdf", 'rb'))
			os.chdir(self.tasksDir)
			self.fm.append(PdfFileReader("New.pdf", 'rb'))
			self.fm.write(os.path.join("..", "Complete DSA Lab File"))

		else:
			print("Lab or Tasks are missing.")


if __name__ == '__main__':
	args = sys.argv
	# labmanualFolder tasksFolder

	work = Work(args[1], args[2])
	work.make()