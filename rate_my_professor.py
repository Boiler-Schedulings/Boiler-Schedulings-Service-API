import ratemyprofessor

def professor(name):
    professor = ratemyprofessor.get_professor_by_school_and_name(
        ratemyprofessor.get_school_by_name("Purdue"), name)
    if professor is not None:
        text = ""
        text += ("%sworks in the %s Department of %s. \n" % (professor.name, professor.department, professor.school.name) )
        text += ("Rating: %s / 5.0 \n" % professor.rating)
        text += ("Difficulty: %s / 5.0 \n" % professor.difficulty)
        text += ("Total Ratings: %s \n" % professor.num_ratings)
        if professor.would_take_again is not None:
            text += (("Would Take Again: %s " % round(professor.would_take_again, 1)) + '%')
        else:
            text += ("Would Take Again: N/A")
    return text