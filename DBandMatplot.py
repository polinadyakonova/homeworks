import sqlite3, os, matplotlib.pyplot as plt
conn = sqlite3.connect('hittite.db')
c = conn.cursor()
c.execute("SELECT Lemma FROM wordforms")
lemma = list(c.fetchall())
c.execute("SELECT Wordform FROM wordforms")
wordform = list(c.fetchall())
c.execute("SELECT Glosses FROM wordforms")
glosses = list(c.fetchall())
for i in range (0, len(lemma)):
    lemma[i] = str(lemma[i])[2:-3]
    wordform[i] = str(wordform[i])[2:-3]
    glosses[i] = str(glosses[i])[2:-3]
    
conn.commit()
conn.close()


if os.path.isfile('mybase.db'):
    os.remove('mybase.db')
conn = sqlite3.connect('mybase.db')
c = conn.cursor()
c.execute("CREATE TABLE words(id text, Lemma text, Wordform text, Glosses text)") #ïåðâàÿ òàáëèöà
for i in range (0, len(lemma)):
    c.execute("INSERT INTO words VALUES ('{}', '{}', '{}', '{}')".format('id' + str(i + 1) + 'w', lemma[i], wordform[i], glosses[i]))

c.execute("CREATE TABLE glosses(id text, Abbreviation text, Meaning text)") #âòîðàÿ òàáëèöà
abbreviation = ['ADJ', 'ADV', 'AUX', 'COMP', 'CONJ', 'CONN', 'DEM', 'INDEF', 'N', 'NEG', 'NUM', 'P', 'PART', 'POSS', 'PRON', 'PRV', 'PTCP', 'REL', 'Q', 'V', 'NOM', 'ACC', 'DAT', 'ABL', 'GEN', 'VOC', 'LOC', 'DAT-LOC', 'SG', '1SG', '2SG', '3SG', 'PL', '1PL', '2PL', '3PL', 'C', 'I', 'PST', 'MED', 'INF', 'IMF', 'IMP', 'PRS', 'PRT', 'ENLC', 'EMPH', 'INSTR', 'IMPF', 'ENCL', 'PERS']
meaning = ['adjective', 'adverb', 'auxiliary', 'complementizer', 'conjunction', 'connective', 'demonstrative pronoun', 'indefinite pronoun', 'noun', 'negative', 'cardinal', 'preposition (postposition)', 'particle', 'possessive pronoun', 'pronoun', 'preverb', 'participle', 'relative pronoun', 'question word', 'verb', 'Nominative', 'Accusative', 'Dative', 'Ablative', 'Genitive', 'Vocative', 'Locative', 'Dat-Loc', 'SG', '1SG', '2SG', '3SG', 'PL', '1PL', '2PL', '3PL', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-']
for i in range (0, len(abbreviation)):
    c.execute("INSERT INTO glosses VALUES ('{}', '{}', '{}')".format('id' + str(i + 1) + 'g', abbreviation[i], meaning[i]))

c.execute("CREATE TABLE w_to_g(Word text,  Glosses text)") #òðåòüÿ òàáëèöà
gl = []
for i in range(0, len(glosses)):
    a = glosses[i].find('.')
    if a > -1:
        arr = glosses[i].split('.')
        for j in range(0, len(arr)):
            if arr[j][:2].isupper() == True:
                a = arr[j].find(' ')
                if a > -1:
                    arr[j] = arr[j][:a]
                gl.append(arr[j])
                c.execute("SELECT id FROM glosses WHERE Abbreviation = '{}'".format(arr[j]))
                m = str(c.fetchall())[3:-4]
                c.execute("INSERT INTO w_to_g VALUES ('{}', '{}')".format('id' + str(i + 1) + 'w', m))
gl = set(gl)#ìíîæåñòâî âñåõ ãëîññ

X = [] 
Y = [] #ñêîëüêî øòóê êàæäîé ãëîññû
for i in range(0, len(abbreviation)):
    c.execute("SELECT Word FROM w_to_g WHERE Glosses = '{}'".format('id' + str(i + 1) + 'g'))
    a = len(c.fetchall())
    
    if a > 0:
        Y.append(a)
        X.append(i + 1)
        
#ïî ãîðèçîíòàëè id êàæäîé ãëîññû, ïî âåðòèêàëè - êîëè÷åñòâî
plt.subplot(131)        
plt.bar(X, Y)
plt.title('all')
plt.subplot(132)
plt.bar(X[9:17], Y[9:17])
plt.title('cases')
plt.subplot(133)
plt.bar(X[17:24], Y[17:24])
plt.title('number')
plt.show()
conn.commit()
conn.close()
