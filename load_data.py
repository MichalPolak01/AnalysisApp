import glob
import pandas as pd

def load_data(selected_cities, chart_title):
    print(selected_cities)
    print(len(selected_cities))
    # print(selected_cities.pop)
    if (len(selected_cities) == 1):
        # Utwórz nazwę pliku
        file_pattern_1 = f"results/{selected_cities[0]}/*--{chart_title}.csv"
        
        # Uzyskaj listę plików pasujących do wzorca
        matching_files_1 = glob.glob(file_pattern_1)

        # Sprawdź, czy znaleziono pasujące pliki
        if not matching_files_1:
            print(f"Nie znaleziono pasującego pliku w katalogu: {file_pattern_1}")
            return

        # Wybierz pierwszy pasujący plik (w razie gdyby było więcej)
        selected_file_1 = matching_files_1[0]
        print("Selected file:" + selected_file_1)

        # Odczytaj dane z wybranego pliku CSV
        try:
            df1 = pd.read_csv(selected_file_1, encoding='ISO-8859-1')
        except UnicodeDecodeError:
            print("Nieudana próba odczytu pliku CSV.")

        return df1
    
    elif (len(selected_cities) == 2):
        # Utwórz nazwy plików
        file_pattern_1 = f"results/{selected_cities[0]}/*--{chart_title}.csv"
        file_pattern_2 = f"results/{selected_cities[1]}/*--{chart_title}.csv"
        
        # Uzyskaj listę plików pasujących do wzorca
        matching_files_1 = glob.glob(file_pattern_1)
        matching_files_2 = glob.glob(file_pattern_2)

        # Sprawdź, czy znaleziono pasujące pliki
        if not matching_files_1:
            print(f"Nie znaleziono pasującego pliku w katalogu: {file_pattern_1}")
            return
        if not matching_files_2:
            print(f"Nie znaleziono pasującego pliku w katalogu: {file_pattern_2}")
            return

        # Wybierz pierwszy pasujący plik (w razie gdyby było więcej)
        selected_file_1 = matching_files_1[0]
        selected_file_2 = matching_files_2[0]
        print("Selected file:" + selected_file_1)
        print("Selected file:" + selected_file_2)

        # Odczytaj dane z wybranego pliku CSV
        try:
            df1 = pd.read_csv(selected_file_1, encoding='ISO-8859-1')
            df2 = pd.read_csv(selected_file_2, encoding='ISO-8859-1')
        except UnicodeDecodeError:
            print("Nieudana próba odczytu pliku CSV.")

        return df1, df2
    
    elif (len(selected_cities) == 3):
        # Utwórz nazwy plików
        file_pattern_1 = f"results/{selected_cities[0]}/*--{chart_title}.csv"
        file_pattern_2 = f"results/{selected_cities[1]}/*--{chart_title}.csv"
        file_pattern_3 = f"results/{selected_cities[2]}/*--{chart_title}.csv"
        
        # Uzyskaj listę plików pasujących do wzorca
        matching_files_1 = glob.glob(file_pattern_1)
        matching_files_2 = glob.glob(file_pattern_2)
        matching_files_3 = glob.glob(file_pattern_3)

        # Sprawdź, czy znaleziono pasujące pliki
        if not matching_files_1:
            print(f"Nie znaleziono pasującego pliku w katalogu: {file_pattern_1}")
            return
        if not matching_files_2:
            print(f"Nie znaleziono pasującego pliku w katalogu: {file_pattern_2}")
            return
        if not matching_files_3:
            print(f"Nie znaleziono pasującego pliku w katalogu: {file_pattern_3}")
            return

        # Wybierz pierwszy pasujący plik (w razie gdyby było więcej)
        selected_file_1 = matching_files_1[0]
        selected_file_2 = matching_files_2[0]
        selected_file_3 = matching_files_3[0]
        print("Selected file:" + selected_file_1)
        print("Selected file:" + selected_file_2)
        print("Selected file:" + selected_file_3)

        # Odczytaj dane z wybranego pliku CSV
        try:
            df1 = pd.read_csv(selected_file_1, encoding='ISO-8859-1')
            df2 = pd.read_csv(selected_file_2, encoding='ISO-8859-1')
            df3 = pd.read_csv(selected_file_3, encoding='ISO-8859-1')
        except UnicodeDecodeError:
            print("Nieudana próba odczytu pliku CSV.")

        return df1, df2, df3