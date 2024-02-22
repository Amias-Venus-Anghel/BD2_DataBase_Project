import sys
import pandas as pd


class Parse():
    def __init__(self, from_file, to_file):
        self.f = None
        self.from_file = from_file
        self.to_file = to_file

    def add_create_tables(self):
        self.f = open(self.to_file, "w")

        self.f.write("DROP TABLE IF EXISTS Jocuri_masa;\n"
                     "DROP TABLE IF EXISTS Jocuri_pc;\n"
                     "DROP TABLE IF EXISTS Jocuri;\n"
                     "DROP TABLE IF EXISTS Producator;\n"
                     "DROP TABLE IF EXISTS Numar_jucatori;\n\n")

        self.f.write("CREATE TABLE Numar_jucatori (\n"
                     "  id_nr_jucatori INT PRIMARY KEY,\n"
                     "  min INT,\n"
                     "  max INT\n"
                     ");\n\n")

        self.f.write("CREATE TABLE Producator (\n"
                     "  id_prod INT PRIMARY KEY,\n"
                     "  nume VARCHAR(255),\n"
                     "  locatie VARCHAR(255),\n"
                     "  mail VARCHAR(255)\n"
                     ");\n\n")

        self.f.write("CREATE TABLE Jocuri (\n"
                     "  id_joc INT PRIMARY KEY,\n"
                     "  nume VARCHAR(255),\n"
                     "  id_prod INT,\n"
                     "  pret INT,\n"
                     "  rating INT,\n"
                     "  numar_vanzari INT,\n"
                     "FOREIGN KEY (id_prod) REFERENCES Producator(id_prod)\n"
                     ");\n\n")

        self.f.write("CREATE TABLE Jocuri_pc ( \n"
                     "  id_joc INT PRIMARY KEY, \n"
                     "  gen VARCHAR(255),  \n"
                     "  status VARCHAR(255)\n"
                     "); \n\n")

        self.f.write("CREATE TABLE Jocuri_masa (\n"
                     "  id_joc INT PRIMARY KEY,\n"
                     "  id_nr_jucatori INT,\n"
                     "  durata_joc INT,\n"
                     "  limba VARCHAR(255),\n"
                     "  varsta_min_rec INT,\n"
                     "  exemplare_disponibile INT,\n"
                     "  FOREIGN KEY (id_nr_jucatori) REFERENCES Numar_jucatori(id_nr_jucatori)\n"
                     ");\n\n")

        self.f.close();

    def insert_rows(self):
        self.f = open(self.to_file, "a")

        self.f.write("INSERT INTO Numar_jucatori (id_nr_jucatori, min, max)\nVALUES\n")

        dataframe = pd.read_excel(self.from_file, sheet_name=4, skiprows=1, engine='openpyxl')
        dataframe = dataframe.astype(str);
        for ind in dataframe.index:
            self.f.write("(" +

                         dataframe['id_nr_jucatori'][ind] + "," +
                         dataframe['min'][ind] + "," +
                         dataframe['max'][ind] + ")"
                         )
            if ind != dataframe.index[-1]:
                self.f.write(",\n")

        self.f.write(";\n\n")

        self.f.write("INSERT INTO Producator (id_prod, nume, locatie, mail)\nVALUES\n")

        dataframe = pd.read_excel(self.from_file, sheet_name=1, skiprows=1, engine='openpyxl')
        dataframe = dataframe.astype(str);
        for ind in dataframe.index:
            self.f.write("(" +
                         dataframe['id_prod'][ind] + ", '" +
                         dataframe['nume'][ind] + "', '" +
                         dataframe['locatie'][ind] + "' , '" +
                         dataframe['mail'][ind] + "')"
                         )
            if ind != dataframe.index[-1]:
                self.f.write(",\n")

        self.f.write(";\n\n")

        self.f.write("INSERT INTO Jocuri (id_joc, nume, id_prod, pret, rating, numar_vanzari)\nVALUES\n")

        dataframe = pd.read_excel(self.from_file, sheet_name=0, skiprows=1, engine='openpyxl')
        dataframe = dataframe.astype(str);
        for ind in dataframe.index:
            self.f.write("(" +
                         dataframe['id_joc'][ind] + ", '" +
                         dataframe['nume'][ind] + "'," +
                         dataframe['id_prod'][ind] + "," +
                         dataframe['pret'][ind] + "," +
                         dataframe['rating'][ind] + "," +
                         dataframe['numar_vanzari'][ind] + ")"
                         )
            if ind != dataframe.index[-1]:
                self.f.write(",\n")

        self.f.write(";\n\n")

        self.f.write("INSERT INTO Jocuri_pc (id_joc, gen, status)\nVALUES\n")

        dataframe = pd.read_excel(self.from_file, sheet_name=2, skiprows=1, engine='openpyxl')
        dataframe = dataframe.astype(str);
        for ind in dataframe.index:
            self.f.write("(" +
                         dataframe['id_joc'][ind] + ", '" +
                         dataframe['gen'][ind] + "', '" +
                         dataframe['status'][ind] + "')"
                         )
            if ind != dataframe.index[-1]:
                self.f.write(",\n")

        self.f.write(";\n\n")

        self.f.write(
            "INSERT INTO Jocuri_masa (id_joc, id_nr_jucatori, durata_joc, limba, varsta_min_rec, exemplare_disponibile)\nVALUES\n")

        dataframe = pd.read_excel(self.from_file, sheet_name=3, skiprows=1, engine='openpyxl')
        dataframe = dataframe.astype(str);

        for ind in dataframe.index:
            self.f.write("(" +

                         dataframe['id_joc'][ind] + "," +
                         dataframe['id_nr_jucatori'][ind] + "," +
                         dataframe['durata_joc'][ind] + ", '" +
                         dataframe['limba'][ind] + "' ," +
                         dataframe['varsta_min_rec'][ind] + "," +
                         dataframe['exemplare_disponibile'][ind] + ")"
                         )
            if ind != dataframe.index[-1]:
                self.f.write(",\n")

        self.f.write(";\n\n")

        self.f.close()


def main():
    if len(sys.argv) < 3:
        print(f"Usage: python3 {sys.argv[0]} path_to_file parced_file_name")
        print("ex: python3.9 parcer.py Date_proiect.xlsx script_prj")
        return

    parcer = Parse(sys.argv[1], sys.argv[2])

    parcer.add_create_tables()
    parcer.insert_rows()


if __name__ == "__main__":
    main()
