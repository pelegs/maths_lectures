lectures_folder="lecture_notes"
CHAPTERS = preface intro vectors linear_trans matrices linear_systems eigenvectors uses integrals general quantum
$(eval CHPTRNM=$(shell echo $$(($(NUM)+1))))
CHAPTER = $(word $(CHPTRNM), $(CHAPTERS))

do:
	rm -rf pythontex-files-* *.pytxcode
	pdflatex -shell-escape lectures
	biber lectures
	pythontex lectures.pytxcode
	pdflatex -shell-escape lectures

quick:
	pdflatex -shell-escape lectures

presentation:
	pdflatex -shell-escape --jobname '$(CHAPTER)' "\def\chnum{$(NUM)} \input{presentations}"
	mv "$(CHAPTER).pdf" presentation_chapters
	rm -f $(CHAPTER).*
	rm -f ../$(CHAPTER).*

fullpresent:
	rm -rf pythontex-files-* *.pytxcode
	pdflatex -shell-escape "\def\full{1} \input{presentations}"
	biber lectures
	pythontex presentations.pytxcode
	pdflatex -shell-escape presentations
