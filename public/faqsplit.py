def process_question(qtxt):
    question = ''
    skip = False
    for letter in qtxt:
        if letter == '<':
            skip = True
        if letter == '>':
            skip = False
        if skip:
            continue
        if letter.isalnum() or letter == ' ':
            if letter == ' ':
                letter = '_'
            question += letter.lower()
    return question

def process_h3(h3, l):
    endh3 = l.find("</h3>")
    qtxt = l[h3+4:endh3].strip()
    question = ''
    skip = False
    for letter in qtxt:
        if letter == '<':
            skip = True
        if letter == '>':
            skip = False
        if skip:
            continue
        if letter.isalnum() or letter == ' ':
            if letter == ' ':
                letter = '_'
            question += letter.lower()
    return question

f = open("FAQ.html")
q = open("questions.txt", "w")

def write_answer(q, question, answer):
    q.write("%s\n" % question)
    question = process_question(question)
    ans = open("answers/%s.html" % question, "w")
    ans.write(answer)
    ans.close()

finding_h3 = True
reading_answer = False
read_already = False
while 1:
    if not read_already:
        l = f.readline()
        print "read line", l
        if not l or l.find("</body>") != -1:
            if reading_answer:
                write_answer(q, question, answer)
            break
    read_already = False
    if finding_h3:
        h3 = l.find("<h3>")
        if h3 == -1:
            continue
        print "about to question", h3
        endh3 = l.find("</h3>")
        question = l[h3+4:endh3].strip()
        reading_answer = True
        finding_h3 = False
        answer = ''
        print "found question"
        continue
    elif reading_answer:
        h3 = l.find("<h3>")
        if h3 == -1:
            answer += l
        else:
            read_already = True
            reading_answer = False
            finding_h3 = True
            write_answer(q, question, answer)

