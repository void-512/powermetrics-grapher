import grapher
import argReader
import logReader
import checkboxWindow

save = argReader.save

lot, dfusage, dffrequency, dfpower = checkboxWindow.get_selected(logReader.dfconstructor())
grapher.display(lot, dfusage, dffrequency, dfpower, save)