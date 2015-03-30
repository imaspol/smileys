import os,re

class SmileyAction(object):
    def __init__(self,filename,path="smileys.txt"):
        """ Initialise le dictionnaire de smileys et de dialogues + création des fichiers"""
        # Sauvegarde du prefixe de fichiers
        self.filename=filename
        #création du dictionnaire de dialogue
        self.dialogue=dict()
        # Création de l'élément racine
        self.smileys = dict()
        # Ouverture du fichier
        with open(path,encoding="utf-8-sig") as _file : 
            for _n,_line in enumerate(_file) : 
                _data = _line.rstrip().split("\t")
                # On ajoute la ligne courante dans de dico de smileys
                _sm = _data[1].strip() # Smiley
                _occ = _data[2] # Occurences
                if _sm not in self.smileys.keys() and len(_sm):
                    self.smileys[_sm]=_occ
        # Création du dictionnaire de résultats
        self.results = dict.fromkeys(self.smileys.keys(),0)
        # Création et ouverture du fichier de log
        self.logFile = open("{}_log_smiley.txt".format(self.filename),"w")
        
    def findall(self,line,smiley):
        """ La fonction renvoie la liste des positions du smiley"""
        resultat=[]
        precedent=0
        index=line.find(smiley)
        while index!=-1:
            resultat.append(precedent+index)
            precedent=precedent+index+len(smiley)
            index=line[precedent:].find(smiley)
        return resultat
        
    def do(self,line,index):
        # pour chaque smiley du dico, on cherche si il est dans la ligne
        for _sm in self.results.keys() : 
            _pos = self.findall(line,_sm)
            if len(_pos):
                self.logFile.write("{}\t\t - #{}:{}\n".format(_sm,len(_pos),line))
                #Le smiley est dans la ligne
                self.results[_sm] += len(_pos)
                if index not in self.dialogue.keys() : self.dialogue[index]=0
                self.dialogue[index]+=len(_pos)
                
    def finalize(self):
        """ Création du fichier de résultat """
        self.logFile.close()
        # Création du fichier de smileys
        _filePath1 = "{}_smiley.csv".format(self.filename)
        with open(_filePath1,"w", encoding="utf-8-sig") as file: 
            for _k,_c in self.results.items() : 
                if _c > 0 :
                    _output = "{}\t{}\n".format(_k,_c)
                    file.write(_output)

        # Création du fichier de dialogues
        _filePath2 = "{}_dialog_smiley.csv".format(self.filename)
        with open(_filePath2,"w", encoding="utf-8-sig") as file: 
            for _k,_c in self.dialogue.items() : 
                if _c > 0 :
                    _output = "{};{}\n".format(_k,_c)
                    file.write(_output)
        # Test d'existence
        return os.path.exists(_filePath1) and os.path.exists(_filePath2)
        
    def saveUnique(smileydata):
        with open("smileyfinal.txt",'w') as file :
            for _k,_v in smileydata.iteritems() : 
                _line = _k+'\t'+_v+'\n'
                file.write(_line)
