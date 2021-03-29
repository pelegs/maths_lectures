PYLIB = "pythontex-files-all"
PYTEX = "pythontex"
RM = rm -rf
TEX = "pdflatex"
ALL = "all.*"
QUESTIONS = "ex$(EX)_questions"
SOLUTION = "ex$(EX)_solution"
EXSHEET = "exsheet$(EX)"

everything:
	$(RM) $(PYLIB) $(PYTEX_FILE)
	$(TEX) -shell-escape -jobname=all "\input{gen/all}"
	$(PYTEX) all.pytxcode
	$(TEX) -shell-escape -jobname=all "\input{gen/all}"
	mv all.* all

specific:
	# Questions
	$(TEX) -shell-escape -jobname=separate/$(QUESTIONS) "\def\withsol{0}\def\ex{$(EX)}\input{gen/specific}"
	$(TEX) -shell-escape -jobname=separate/$(QUESTIONS) "\def\withsol{0}\def\ex{$(EX)}\input{gen/specific}"
	# Solutions
	$(RM) separate/$(SOLUTION).pytxcode
	$(TEX) -shell-escape -jobname=$(SOLUTION) "\def\withsol{1}\def\ex{$(EX)}\input{gen/specific}"
	$(PYTEX) $(SOLUTION).pytxcode
	$(TEX) -shell-escape -jobname=$(SOLUTION) "\def\withsol{1}\def\ex{$(EX)}\input{gen/specific}"
	mv $(SOLUTION).* separate/
	$(RM) pythontex-files-$(SOLUTION)

exsheet:
	$(RM) exsheets/$(EXSHEET).pytxcode
	$(TEX) -jobname=$(EXSHEET) "\def\withsol{1}\def\ex{$(EX)}\input{gen/exsheets}"
	$(PYTEX) $(EXSHEET).pytxcode
	$(TEX) -jobname=$(EXSHEET) "\def\withsol{1}\def\ex{$(EX)}\input{gen/exsheets}"
	mv $(EXSHEET).* exsheets/
	$(RM) pythontex-files-$(EXSHEET)
