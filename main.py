import grapher
import logReader
import checkboxWindow

lot, dfusage, dffrequency, dfpower = checkboxWindow.get_selected(logReader.dfconstructor())
grapher.display(lot, dfusage, dffrequency, dfpower)