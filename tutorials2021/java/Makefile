NAME = "java"
TEX = pdflatex -shell-escape
SOL = "\def\withsol{1}"
NUM = "\def\exnum{$(EXNUM)}"

solution:
	$(TEX) $(SOL) $(NUM) "\input{$(NAME).tex}" && mv "$(NAME).pdf" "$(NAME)_solution.pdf"

questions:
	$(TEX) $(NUM) "\input{$(NAME).tex}" && mv "$(NAME).pdf" "$(NAME)_questions.pdf"

read_questions:
	evince "$(NAME)_questions.pdf"

read_solution:
	evince "$(NAME)_solution.pdf"
